# MCMC diagnostics with [Arviz](https://python.arviz.org/)

This tutorial shows how to evaluate the quality of MCMC samples generated via `sbi` using the `arviz` package.

Outline:

1. Train MNLE to approximate the likelihood underlying the simulator
2. Run MCMC using `pyro` MCMC samplers via `sbi` interface
3. Use `arviz` to visualize the posterior, predictive distributions and MCMC diagnostics.



```python
import arviz as az
import torch
from pyro.distributions import InverseGamma
from torch.distributions import Beta, Binomial, Gamma

from sbi.inference import MNLE, MCMCPosterior, likelihood_estimator_based_potential
from sbi.utils import MultipleIndependent

# Seeding
torch.manual_seed(1);
```


```python
# Toy simulator for mixed data
def mixed_simulator(theta):
    beta, ps = theta[:, :1], theta[:, 1:]

    choices = Binomial(probs=ps).sample()
    rts = InverseGamma(concentration=2 * torch.ones_like(beta), rate=beta).sample()

    return torch.cat((rts, choices), dim=1)


# Define independent priors for each dimension.
prior = MultipleIndependent(
    [
        Gamma(torch.tensor([1.0]), torch.tensor([0.5])),
        Beta(torch.tensor([2.0]), torch.tensor([2.0])),
    ],
    validate_args=False,
)
```

## Train MNLE to approximate the likelihood

For this tutorial, we will use a simple simulator with two parameters. For details see the [example on the decision making model](https://sbi-dev.github.io/sbi/examples/01_decision_making_model/).

Here, we pass `mcmc_method="nuts"` in order to use the underlying [`pyro` No-U-turn sampler](https://docs.pyro.ai/en/1.8.1/mcmc.html#nuts), but it would work as well with other samplers (e.g. "slice_np_vectorized", "hmc").

Additionally, when calling `posterior.sample(...)` we pass `return_arviz=True` so that the [`Arviz InferenceData`](https://arviz-devs.github.io/arviz/api/generated/arviz.InferenceData.html#arviz.InferenceData) object is returned. This object gives us access to the wealth of MCMC diagnostics tool provided by `arviz`.



```python
# Generate training data and train MNLE.
num_simulations = 10000
theta = prior.sample((num_simulations,))
x = mixed_simulator(theta)

trainer = MNLE(prior)
likelihood_estimator = trainer.append_simulations(theta, x).train()
```

    /Users/janteusen/qode/sbi/sbi/neural_nets/mnle.py:60: UserWarning: The mixed neural likelihood estimator assumes that x contains
            continuous data in the first n-1 columns (e.g., reaction times) and
            categorical data in the last column (e.g., corresponding choices). If
            this is not the case for the passed `x` do not use this function.
      warnings.warn(


     Neural network successfully converged after 65 epochs.

## Run Pyro NUTS MCMC and obtain `arviz InferenceData` object



```python
# Simulate "observed" data x_o
torch.manual_seed(42)
num_trials = 100
theta_o = prior.sample((1,))
x_o = mixed_simulator(theta_o.repeat(num_trials, 1))

# Set MCMC parameters and run Pyro NUTS.
mcmc_parameters = dict(
    num_chains=4,
    thin=5,
    warmup_steps=50,
    init_strategy="proposal",
    method="nuts",
)
num_samples = 1000

# get the potential function and parameter transform for constructing the posterior
potential_fn, parameter_transform = likelihood_estimator_based_potential(
    likelihood_estimator, prior, x_o
)
mnle_posterior = MCMCPosterior(
    potential_fn, proposal=prior, theta_transform=parameter_transform, **mcmc_parameters
)

mnle_samples = mnle_posterior.sample(
    (num_samples,), x=x_o, show_progress_bars=False
)
# get arviz InferenceData object from posterior
inference_data = mnle_posterior.get_arviz_inference_data()

```

    /Users/janteusen/qode/sbi/sbi/utils/sbiutils.py:341: UserWarning: An x with a batch size of 100 was passed. It will be interpreted as a batch of independent and identically
                distributed data X={x_1, ..., x_n}, i.e., data generated based on the
                same underlying (unknown) parameter. The resulting posterior will be with
                respect to entire batch, i.e,. p(theta | X).
      warnings.warn(
    /Users/janteusen/miniconda3/envs/sbi/lib/python3.8/site-packages/torch/__init__.py:690: UserWarning: torch.set_default_tensor_type() is deprecated as of PyTorch 2.1, please use torch.set_default_dtype() and torch.set_default_device() as alternatives. (Triggered internally at /Users/runner/work/pytorch/pytorch/pytorch/torch/csrc/tensor/python_tensor.cpp:453.)
      _C._set_default_tensor_type(t)
    /Users/janteusen/miniconda3/envs/sbi/lib/python3.8/site-packages/torch/__init__.py:690: UserWarning: torch.set_default_tensor_type() is deprecated as of PyTorch 2.1, please use torch.set_default_dtype() and torch.set_default_device() as alternatives. (Triggered internally at /Users/runner/work/pytorch/pytorch/pytorch/torch/csrc/tensor/python_tensor.cpp:453.)
      _C._set_default_tensor_type(t)
    /Users/janteusen/miniconda3/envs/sbi/lib/python3.8/site-packages/torch/__init__.py:690: UserWarning: torch.set_default_tensor_type() is deprecated as of PyTorch 2.1, please use torch.set_default_dtype() and torch.set_default_device() as alternatives. (Triggered internally at /Users/runner/work/pytorch/pytorch/pytorch/torch/csrc/tensor/python_tensor.cpp:453.)
      _C._set_default_tensor_type(t)
    /Users/janteusen/miniconda3/envs/sbi/lib/python3.8/site-packages/torch/__init__.py:690: UserWarning: torch.set_default_tensor_type() is deprecated as of PyTorch 2.1, please use torch.set_default_dtype() and torch.set_default_device() as alternatives. (Triggered internally at /Users/runner/work/pytorch/pytorch/pytorch/torch/csrc/tensor/python_tensor.cpp:453.)
      _C._set_default_tensor_type(t)


## Generate `arviz` plots

The resulting `InferenceData` object can be passed to most `arviz` plotting functions, and there are plenty see [here](https://arviz-devs.github.io/arviz/examples/index.html#) for an overview.

To get a better understanding of the `InferenceData` object see [here](https://arviz-devs.github.io/arviz/schema/schema.html).

Below and overview of common MCMC diagnostics plot, see the corresponding `arviz` documentation for interpretation of the plots.

We will a full use-case using the SBI-MCMC-arviz workflow soon.



```python
print(inference_data.posterior)
```

    <xarray.Dataset>
    Dimensions:      (chain: 4, draw: 1254, theta_dim_0: 2)
    Coordinates:
      * chain        (chain) int64 0 1 2 3
      * draw         (draw) int64 0 1 2 3 4 5 6 ... 1248 1249 1250 1251 1252 1253
      * theta_dim_0  (theta_dim_0) int64 0 1
    Data variables:
        theta        (chain, draw, theta_dim_0) float32 2.195 0.8838 ... 2.593 0.806
    Attributes:
        created_at:     2024-03-06T13:33:00.426835
        arviz_version:  0.15.1


### Diagnostic plots



```python
az.style.use("arviz-darkgrid")
az.plot_rank(inference_data)
```




    array([<Axes: title={'center': 'theta\n0'}, xlabel='Rank (all chains)', ylabel='Chain'>,
           <Axes: title={'center': 'theta\n1'}, xlabel='Rank (all chains)', ylabel='Chain'>],
          dtype=object)




    
![png](15_mcmc_diagnostics_with_arviz_files/15_mcmc_diagnostics_with_arviz_10_1.png)
    



```python
az.plot_autocorr(inference_data);
```


    
![png](15_mcmc_diagnostics_with_arviz_files/15_mcmc_diagnostics_with_arviz_11_0.png)
    



```python
az.plot_trace(inference_data, compact=False);
```


    
![png](15_mcmc_diagnostics_with_arviz_files/15_mcmc_diagnostics_with_arviz_12_0.png)
    



```python
az.plot_ess(inference_data, kind="evolution");
```


    
![png](15_mcmc_diagnostics_with_arviz_files/15_mcmc_diagnostics_with_arviz_13_0.png)
    


### Posterior density plots



```python
az.plot_posterior(inference_data)
```




    array([<Axes: title={'center': 'theta\n0'}>,
           <Axes: title={'center': 'theta\n1'}>], dtype=object)




    
![png](15_mcmc_diagnostics_with_arviz_files/15_mcmc_diagnostics_with_arviz_15_1.png)
    



```python
print(
    f"""Given the {num_trials} we observed, the posterior is centered around
    true underlying parameters theta_o: {theta_o}"""
)
```

    Given the 100 we observed, the posterior is centered around
        true underlying parameters theta_o: tensor([[1.9622, 0.7550]])



```python
az.plot_pair(inference_data)
```




    <Axes: xlabel='theta\n0', ylabel='theta\n1'>




    
![png](15_mcmc_diagnostics_with_arviz_files/15_mcmc_diagnostics_with_arviz_17_1.png)
    



```python
az.plot_pair(
    inference_data,
    var_names=["theta"],
    kind="hexbin",
    marginals=True,
    figsize=(10, 10),
)
```




    array([[<Axes: >, None],
           [<Axes: xlabel='theta\n0', ylabel='theta\n1'>, <Axes: >]],
          dtype=object)




    
![png](15_mcmc_diagnostics_with_arviz_files/15_mcmc_diagnostics_with_arviz_18_1.png)
    



```python

```
