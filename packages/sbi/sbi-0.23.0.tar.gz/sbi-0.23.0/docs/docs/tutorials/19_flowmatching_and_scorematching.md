# Flow-Matching Posterior Estimation (FMPE) and Neural Posterior Score Estimation (NPSE)

`sbi` also incorporates recent algorithms based on Flow Matching and Score Matching generative models, which are also referred to as Continuous Normalizing Flows (CNF) and Denoising Diffusion Probabilistic Models (DDPM), respectively.

At the highest level, you can conceptualize FMPE and NPSE as tackling the exact same problem as NPE, i.e., estimating the posterior from simulations, but replacing Normalizing Flows with different conditional density estimators. 

Flow Matching and Score Matching, as generative models, are also quite similar to Normalizing Flows, where a deep neural network parameterizes the transformation from a base distribution (e.g., Gaussian) to a more complex one that approximates the target density, but they differ in what this transformation looks like (more on that below). 

Beyond that, Flow Matching and Score Matching offer different benefits and drawbacks compared to Normalizing Flows, which make them better (or worse) choices for some problems. For examples, Score Matching (Diffusion Models) are known to be very flexible and can model high-dimensional distributions, but are comparatively slow during sampling.

In this tutorial, we take a brief look at the API for `FMPE` and `NPSE`, their pros and cons, as well as highlight some notable options.

For more information, see:

**Score Matching**:
- Hyvärinen, A. "Estimation of Non-Normalized Statistical Models by Score Matching." JMLR 2005.
- Song, Y., et al. "Score-Based Generative Modeling through Stochastic Differential Equations." ICLR 2021.
- Geffner, T., Papamakarios, G., and Mnih, A. "Score modeling for simulation-based inference." NeurIPS 2022 Workshop on Score-Based Methods. 2022.
- Sharrock, L., Simons, J., et al. "Sequential neural score estimation: Likelihood-free inference with conditional score based diffusion models." ICML 2024.

**Flow Matching**:
- Lipman, Y., et al. "Flow Matching for Generative Modeling." ICLR 2023
- Wildberger, J.B.,  Buchholz, S., et al. "Flow Matching for Scalable Simulation-Based Inference." NeurIPS 2023.


```python
import torch

from sbi.inference import NPSE
from sbi.utils import BoxUniform
from sbi.analysis import pairplot
```

    WARNING (pytensor.tensor.blas): Using NumPy C-API based implementation for BLAS functions.



```python
# Example toy simulator
# Define the prior
num_dims = 3
num_sims = 5000
prior = BoxUniform(low=-torch.ones(num_dims), high=torch.ones(num_dims))

def simulator(theta):
    """Linear gaussian simulator."""
    return theta + 1.0 + torch.randn_like(theta) * 0.1

# Produce simulations
theta = prior.sample((num_sims,))
x = simulator(theta)

theta_o = torch.zeros(num_dims)
x_o = simulator(theta_o)
```

## FMPE

Flow-Matching Posterior Estimation (FMPE) is an approach to Simulation-Based Inference
(SBI) that leverages Flow Matching, a generative modeling technique where the
transformation from a simple base distribution (like a Gaussian) to the target
distribution is learned through matching the flow of probability densities.

### Key Concept:
- **Flow Matching**: The core idea is to model the probability flow between the base
  distribution and the target distribution by minimizing a discrepancy between their
  "flows" or "dynamics" in the latent space. This is typically done by training a neural
  network to parameterize a vector field that defines how samples should be moved or
  transformed in order to follow the target distribution.

### Step-by-Step Process:
1. **Base Distribution**: Start with a simple base distribution (e.g., Gaussian).
2. **Neural Network Parameterization**: Use a neural network to learn a vector field
   that describes the flow from the base distribution to the target distribution.
3. **Flow Matching Objective**: Optimize the neural network to minimize a loss function
   that captures the difference between the flow of the base distribution and the target
   distribution.
4. **Sampling**: Once trained, draw samples from the base distribution and apply the
   learned flow transformation to obtain samples from the approximate posterior
   distribution.

FMPE can be more efficient than traditional normalizing flows in some settings,
especially when the target distribution has complex structures or when high-dimensional
data is involved (see Dax et al., 2023, https://arxiv.org/abs/2305.17161 for an
example). However, compared to (discrete time) normalizing flows, flow matching is
usually slower at inference time because sampling and evaluation of the target
distribution requires solving the underlying ODE (compared to just doing a NN forward
pass for normalizing flows). 

In the next cell, we'll show how to use FMPE using the `sbi` package.




```python
from sbi.inference import FMPE
from sbi.neural_nets import flowmatching_nn

# the quick way
trainer = FMPE(prior)
trainer.append_simulations(theta, x).train()
posterior = trainer.build_posterior()
```

     Neural network successfully converged after 61 epochs.


```python
# Set up a custom vector field neural network
net_builder = flowmatching_nn(
    model="resnet",
    num_blocks=3,
    hidden_features=24,
    # embedding_net=CNNEmbedding  # e.g., for image data.
)
trainer = FMPE(prior, density_estimator=net_builder)
trainer.append_simulations(theta, x).train(training_batch_size=200, learning_rate=5e-4)
posterior = trainer.build_posterior()
posterior_samples = posterior.sample((10000,), x_o)
```

     Neural network successfully converged after 125 epochs.


    Drawing 10000 posterior samples:   0%|          | 0/10000 [00:00<?, ?it/s]



```python
# plot posterior samples
fig, ax = pairplot(
    posterior_samples, limits=[[-2, 2], [-2, 2], [-2, 2]], figsize=(5, 5),
    labels=[r"$\theta_1$", r"$\theta_2$", r"$\theta_3$"],
    points=theta_o # add ground truth thetas
)
```


    
![png](19_flowmatching_and_scorematching_files/19_flowmatching_and_scorematching_6_0.png)
    


---

# NPSE
NPSE approximates the posterior distribution by learning its score function, i.e., gradient of the log-density, using the denoising score matching loss. The class of generative models is referred to as score-based generative models, with close links to diffusion models.

- Score-based generative models have been shown to scale well to very high dimensions (e.g., high-resolutions images), which is particularly useful when the parameter space (and hence, the target posterior) is high-dimensional.
- On the other hand, sampling can be slower as it involves solving many steps of the stochastic differential equation for reversing the diffusion process.

Note that only the single-round version of NPSE is implemented currently.

For more details on score-based generative models, see [Song et al., 2020](https://arxiv.org/abs/2011.13456) (in particular, Figure 1 and 2).


```python
# Instantiate NPSE and append simulations
inference = NPSE(prior=prior, sde_type="ve")
inference.append_simulations(theta, x)
```

Note the argument `sde_type`, which defines whether the forward diffusion process has a noising schedule that is Variance Exploding (`ve`, i.e., [SMLD](https://proceedings.neurips.cc/paper/2019/hash/3001ef257407d5a371a96dcd947c7d93-Abstract.html?ref=https://githubhelp.com)), Variance Preserving (`vp`, i.e., [DDPM](https://proceedings.neurips.cc/paper/2020/hash/4c5bcfec8584af0d967f1ab10179ca4b-Abstract.html)), or sub-Variance Preserving (`subvp`) in the limit.


```python
# Train the score estimator
score_estimator = inference.train()
```

     Neural network successfully converged after 365 epochs.


```python
# Build the posterior using the trained score estimator, and sample
posterior = inference.build_posterior(score_estimator)
posterior_samples = posterior.sample((10000,), x=x_o)
```


    Drawing 10000 posterior samples:   0%|          | 0/499 [00:00<?, ?it/s]



```python
# plot posterior samples
fig, ax = pairplot(
    posterior_samples, limits=[[-2, 2], [-2, 2], [-2, 2]], figsize=(5, 5),
    labels=[r"$\theta_1$", r"$\theta_2$", r"$\theta_3$"],
    points=theta_o # add ground truth thetas
)
```


    
![png](19_flowmatching_and_scorematching_files/19_flowmatching_and_scorematching_13_0.png)
    

