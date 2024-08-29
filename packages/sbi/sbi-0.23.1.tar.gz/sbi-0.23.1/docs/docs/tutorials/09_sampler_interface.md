# Sampling algorithms in `sbi`

`sbi` implements three methods: SNPE, SNLE, and SNRE. When using SNPE, the trained neural network directly approximates the posterior. Thus, sampling from the posterior can be done by sampling from the trained neural network. The neural networks trained in SNLE and SNRE approximate the likelihood(-ratio). Thus, in order to draw samples from the posterior, one has to perform additional sampling steps, e.g. Markov-chain Monte-Carlo (MCMC). In `sbi`, the implemented samplers are:

- Markov-chain Monte-Carlo (MCMC)

- Rejection sampling

- Variational inference (VI)

Below, we will demonstrate how these samplers can be used in `sbi`. First, we train the neural network as always:



```python
import torch

from sbi.inference import SNLE

# dummy Gaussian simulator for demonstration
num_dim = 2
prior = torch.distributions.MultivariateNormal(torch.zeros(num_dim), torch.eye(num_dim))
theta = prior.sample((1000,))
x = theta + torch.randn((1000, num_dim))
x_o = torch.randn((1, num_dim))

inference = SNLE(prior=prior, show_progress_bars=False)
likelihood_estimator = inference.append_simulations(theta, x).train()
```

    WARNING (pytensor.tensor.blas): Using NumPy C-API based implementation for BLAS functions.


     Neural network successfully converged after 104 epochs.

And then we pass the options for which sampling method to use to the `build_posterior()` method:



```python
# Sampling with MCMC
sampling_algorithm = "mcmc"
mcmc_method = "slice_np"  # or nuts, or hmc
posterior = inference.build_posterior(sample_with=sampling_algorithm,
                                      mcmc_method=mcmc_method)

# Sampling with variational inference
sampling_algorithm = "vi"
vi_method = "rKL"  # or fKL
posterior = inference.build_posterior(sample_with=sampling_algorithm,
                                      vi_method=vi_method)
# Unlike other methods, vi needs a training step for every observation.
posterior = posterior.set_default_x(x_o).train()

# Sampling with rejection sampling
sampling_algorithm = "rejection"
posterior = inference.build_posterior(sample_with=sampling_algorithm)
```

# More flexibility in adjusting the sampler

With the above syntax, you can easily try out different sampling algorithms. However, in many cases, you might want to customize your sampler. Below, we demonstrate how you can change hyperparameters of the samplers (e.g. number of warm-up steps of MCMC) or how you can write your own sampler from scratch.


## Main syntax (for SNLE and SNRE)

As above, we begin by training the neural network as always:


Then, for full flexibility on using the sampler, we do not use the `.build_posterior()` method, but instead we explicitly define the potential function and the sampling algorithm (see below for explanation):



```python
from sbi.inference import MCMCPosterior, likelihood_estimator_based_potential

potential_fn, parameter_transform = likelihood_estimator_based_potential(
    likelihood_estimator, prior, x_o
)
posterior = MCMCPosterior(
    potential_fn, proposal=prior, theta_transform=parameter_transform, warmup_steps=10
)
```

If you want to use variational inference or rejection sampling, you have to replace the last line with `VIPosterior` or `RejectionPosterior`:



```python
from sbi.inference import RejectionPosterior, VIPosterior

# For VI, we have to train.
posterior = VIPosterior(
    potential_fn, prior=prior, theta_transform=parameter_transform
).train()

posterior = RejectionPosterior(
    potential_fn, proposal=prior, theta_transform=parameter_transform
)
```


      0%|          | 0/2000 [00:00<?, ?it/s]


    
    Converged with loss: 3.11
    Quality Score: -0.029 	 Good: Smaller than 0.5  Bad: Larger than 1.0 	         NOTE: Less sensitive to mode collapse.


At this point, you could also plug the `potential_fn` into any sampler of your choice and not rely on any of the in-built `sbi`-samplers.


## Further explanation

The first lines are the same as for the flexible interface:



```python
inference = SNLE()
likelihood_estimator = inference.append_simulations(theta, x).train()
```

     Neural network successfully converged after 72 epochs.

Next, we obtain the potential function. A potential function is a function of the parameter $f(\theta)$. The posterior is proportional to the product of likelihood and prior: $p(\theta | x_o) \propto p(x_o | \theta)p(\theta)$. The potential function is the logarithm of the right-hand side of this equation: $f(\theta) = \log(p(x_o | \theta)p(\theta))$



```python
potential_fn, parameter_transform = likelihood_estimator_based_potential(
    likelihood_estimator, prior, x_o
)
```

By calling the `potential_fn`, you can evaluate the potential:



```python
# Assuming that your parameters are 1D.
potential = potential_fn(
    torch.zeros(1, num_dim)
)  # -> returns f(0) = log( p(x_o|0) p(0) )
```

The other object that is returned by `likelihood_estimator_based_potential` is a `parameter_transform`. The `parameter_transform` is a [pytorch transform](https://github.com/pytorch/pytorch/blob/master/torch/distributions/transforms.py). The `parameter_transform` is a fixed transform that is can be applied to parameter `theta`. It transforms the parameters into unconstrained space (if the prior is bounded, e.g. `BoxUniform`), and standardizes the parameters (i.e. zero mean, one std). Using `parameter_transform` during sampling is optional, but it usually improves the performance of MCMC.



```python
theta_tf = parameter_transform(torch.zeros(1, num_dim))
theta_original = parameter_transform.inv(theta_tf)
print(theta_original)  # -> tensor([[0.0]])
```

    tensor([[0., 0.]])


After having obtained the `potential_fn`, we can sample from the posterior with MCMC or rejection sampling:



```python
posterior = MCMCPosterior(
    potential_fn, proposal=prior, theta_transform=parameter_transform
)
posterior = RejectionPosterior(potential_fn, proposal=prior)
```

## Main syntax for SNPE

SNPE usually does not require MCMC or rejection sampling (if you still need it, you can use the same syntax as above with the `posterior_estimator_based_potential` function). Instead, SNPE samples from the neural network. If the support of the prior is bounded, some samples can lie outside of the support of the prior. The `DirectPosterior` class automatically rejects these samples:



```python
from sbi.inference import SNPE, DirectPosterior

inference = SNPE()
posterior_estimator = inference.append_simulations(theta, x).train()

posterior = DirectPosterior(posterior_estimator, prior=prior)
```

     Neural network successfully converged after 98 epochs.
