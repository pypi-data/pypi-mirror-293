# API of implemented methods

This notebook spells out the API for all algorithms implemented in the `sbi` toolbox:

- Posterior estimation (SNPE)

- Likelihood estimation (SNLE)

- Likelihood-ratio estimation (SNRE)

- Utilities


## Posterior estimation (SNPE)


**Fast ε-free Inference of Simulation Models with Bayesian Conditional Density Estimation**<br> by Papamakarios & Murray (NeurIPS 2016) <br>[[PDF]](https://papers.nips.cc/paper/6084-fast-free-inference-of-simulation-models-with-bayesian-conditional-density-estimation.pdf) [[BibTeX]](https://papers.nips.cc/paper/6084-fast-free-inference-of-simulation-models-with-bayesian-conditional-density-estimation/bibtex)



```python
# Example setup
import torch

from sbi.utils import BoxUniform

# Define the prior
num_dims = 2
num_sims = 1000
num_rounds = 2
prior = BoxUniform(low=torch.zeros(num_dims), high=torch.ones(num_dims))
simulator = lambda theta: theta + torch.randn_like(theta) * 0.1
x_o = torch.tensor([0.5, 0.5])
```


```python
from sbi.inference import SNPE_A

inference = SNPE_A(prior)
proposal = prior
for _ in range(num_rounds):
    theta = proposal.sample((num_sims,))
    x = simulator(theta)
    _ = inference.append_simulations(theta, x, proposal=proposal).train()
    posterior = inference.build_posterior().set_default_x(x_o)
    proposal = posterior
```

**Automatic posterior transformation for likelihood-free inference**<br>by Greenberg, Nonnenmacher & Macke (ICML 2019) <br>[[PDF]](http://proceedings.mlr.press/v97/greenberg19a/greenberg19a.pdf)



```python
from sbi.inference import SNPE

inference = SNPE(prior)
proposal = prior
for _ in range(num_rounds):
    theta = proposal.sample((num_sims,))
    x = simulator(theta)
    _ = inference.append_simulations(theta, x, proposal=proposal).train()
    posterior = inference.build_posterior().set_default_x(x_o)
    proposal = posterior
```

**Truncated proposals for scalable and hassle-free simulation-based inference** <br> by Deistler, Goncalves & Macke (NeurIPS 2022) <br>[[Paper]](https://arxiv.org/abs/2210.04815)



```python
from sbi.inference import SNPE
from sbi.utils import RestrictedPrior, get_density_thresholder

inference = SNPE(prior)
proposal = prior
for _ in range(num_rounds):
    theta = proposal.sample((num_sims,))
    x = simulator(theta)
    _ = inference.append_simulations(theta, x).train(force_first_round_loss=True)
    posterior = inference.build_posterior().set_default_x(x_o)

    accept_reject_fn = get_density_thresholder(posterior, quantile=1e-4)
    proposal = RestrictedPrior(prior, accept_reject_fn, sample_with="rejection")
```

## Likelihood estimation (SNLE)


**Sequential neural likelihood: Fast likelihood-free inference with autoregressive flows**<br>by Papamakarios, Sterratt & Murray (AISTATS 2019) <br>[[PDF]](http://proceedings.mlr.press/v89/papamakarios19a/papamakarios19a.pdf) [[BibTeX]](https://gpapamak.github.io/bibtex/snl.bib)



```python
from sbi.inference import SNLE

inference = SNLE(prior)
proposal = prior
for _ in range(num_rounds):
    theta = proposal.sample((num_sims,))
    x = simulator(theta)
    _ = inference.append_simulations(theta, x).train()
    posterior = inference.build_posterior(mcmc_method="slice_np_vectorized",
                                          mcmc_parameters={"num_chains": 20,
                                                           "thin": 5})
    proposal = posterior.set_default_x(x_o)
```

**Variational methods for simulation-based inference** <br> by Glöckler, Deistler, Macke (ICLR 2022) <br>[[Paper]](https://arxiv.org/abs/2203.04176)



```python
from sbi.inference import SNLE

inference = SNLE(prior)
proposal = prior
for _ in range(num_rounds):
    theta = proposal.sample((num_sims,))
    x = simulator(theta)
    _ = inference.append_simulations(theta, x).train()
    posterior = inference.build_posterior(sample_with="vi",
                                          vi_method="fKL").set_default_x(x_o)
    proposal = posterior.train()  # Train VI posterior on given x_o.
```

**Flexible and efficient simulation-based inference for models of decision-making** <br> by Boelts, Lueckmann, Gao, Macke (Elife 2022) <br>[[Paper]](https://elifesciences.org/articles/77220)



```python
from sbi.inference import MNLE

inference = MNLE(prior)
theta = prior.sample((num_sims,))
x = simulator(theta)
_ = inference.append_simulations(theta, x).train()
posterior = inference.build_posterior().set_default_x(x_o)
```

## Likelihood-ratio estimation (SNRE)


**Likelihood-free MCMC with Amortized Approximate Likelihood Ratios**<br>by Hermans, Begy & Louppe (ICML 2020) <br>[[PDF]](http://proceedings.mlr.press/v119/hermans20a/hermans20a.pdf)



```python
from sbi.inference import SNRE_A

inference = SNRE_A(prior)
theta = prior.sample((num_sims,))
x = simulator(theta)
_ = inference.append_simulations(theta, x).train()
posterior = inference.build_posterior().set_default_x(x_o)
```

**On Contrastive Learning for Likelihood-free Inference**<br>Durkan, Murray & Papamakarios (ICML 2020) <br>[[PDF]](http://proceedings.mlr.press/v119/durkan20a/durkan20a.pdf).



```python
from sbi.inference import SNRE

inference = SNRE(prior)
proposal = prior
for _ in range(num_rounds):
    theta = proposal.sample((num_sims,))
    x = simulator(theta)
    _ = inference.append_simulations(theta, x).train()
    posterior = inference.build_posterior(mcmc_method="slice_np_vectorized",
                                          mcmc_parameters={"num_chains": 20,
                                                           "thin": 5})
    proposal = posterior.set_default_x(x_o)
```

**Towards Reliable Simulation-Based Inference with Balanced Neural Ratio Estimation**<br>by Delaunoy, Hermans, Rozet, Wehenkel & Louppe (NeurIPS 2022) <br>[[PDF]](https://arxiv.org/pdf/2208.13624.pdf)



```python
from sbi.inference import BNRE

inference = BNRE(prior)
theta = prior.sample((num_sims,))
x = simulator(theta)
_ = inference.append_simulations(theta, x).train(regularization_strength=100.)
posterior = inference.build_posterior().set_default_x(x_o)
```

**Contrastive Neural Ratio Estimation**<br>Benjamin Kurt Miller, Christoph Weniger, Patrick Forré (NeurIPS 2022) <br>[[PDF]](https://arxiv.org/pdf/2210.06170.pdf)



```python
# The main feature of NRE-C is producing an exact ratio of densities at optimum,
# even when using multiple contrastive pairs (classes).

from sbi.inference import SNRE_C

# Amortized inference
inference = SNRE_C(prior)
proposal = prior
theta = proposal.sample((num_sims,))
x = simulator(theta)
_ = inference.append_simulations(theta, x).train(
    num_classes=5,  # sees `2 * num_classes - 1` marginally drawn contrastive pairs.
    gamma=1.0,  # controls the weight between terms in its loss function.
)
posterior = inference.build_posterior().set_default_x(x_o)
```

## Utilities


**Simulation-based calibration**<br>by Talts, Betancourt, Simpson, Vehtari, Gelman (arxiv 2018) <br>[[Paper]](https://arxiv.org/abs/1804.06788))



```python
from sbi.analysis import run_sbc, sbc_rank_plot

thetas = prior.sample((1000,))
xs = simulator(thetas)

# SBC is fast for fully amortized NPE.
inference = SNPE(prior)
theta = prior.sample((num_sims,))
x = simulator(theta)
inference.append_simulations(theta, x).train()
posterior = inference.build_posterior()

ranks, dap_samples = run_sbc(
    thetas, xs, posterior, num_posterior_samples=1_000
)

_ = sbc_rank_plot(
    ranks=ranks,
    num_posterior_samples=1000,
    plot_type="hist",
    num_bins=None,
)
```

**Restriction estimator**<br>by Deistler, Macke & Goncalves (PNAS 2022) <br>[[Paper]](https://www.pnas.org/doi/10.1073/pnas.2207632119)



```python
from sbi.inference import SNPE
from sbi.utils import RestrictionEstimator

restriction_estimator = RestrictionEstimator(prior=prior)
proposal = prior

for _ in range(num_rounds):
    theta = proposal.sample((num_sims,))
    x = simulator(theta)
    restriction_estimator.append_simulations(theta, x)
    classifier = restriction_estimator.train()
    proposal = restriction_estimator.restrict_prior()

all_theta, all_x, _ = restriction_estimator.get_simulations()

inference = SNPE(prior)
density_estimator = inference.append_simulations(all_theta, all_x).train()
posterior = inference.build_posterior()
```

**Expected coverage (sample-based)**<br>as computed in Deistler, Goncalves, Macke (Neurips 2022) [[Paper]](https://arxiv.org/abs/2210.04815) and in Rozet, Louppe (2021) [[Paper]](https://matheo.uliege.be/handle/2268.2/12993)



```python
from sbi.diagnostics import run_sbc, sbc_rank_plot

thetas = prior.sample((1_000,))
xs = simulator(thetas)

ranks, dap_samples = run_sbc(
    thetas, xs, posterior, num_posterior_samples=1_000, reduce_fns=posterior.log_prob
)

_ = sbc_rank_plot(
    ranks=ranks,
    num_posterior_samples=1000,
    plot_type="hist",
    num_bins=None,
)
```
