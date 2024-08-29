# Getting started with `sbi`

Note, you can find the original version of this notebook at [https://github.com/sbi-dev/sbi/blob/main/tutorials/00_getting_started.ipynb](https://github.com/sbi-dev/sbi/blob/main/tutorials/00_getting_started.ipynb) in the `sbi` repository.


```python
import torch

from sbi import analysis as analysis
from sbi import utils as utils
from sbi.inference.base import infer
```

## Running the inference procedure

`sbi` provides a simple interface to run state-of-the-art algorithms for simulation-based inference.

For inference, you need to provide two ingredients:

1) a prior distribution that allows to sample parameter sets.  
2) a simulator that takes parameter sets and produces simulation outputs.

For example, we can have a 3-dimensional parameter space with a uniform prior between [-1,1] and a simple simulator that for the sake of example adds 1.0 and some Gaussian noise to the parameter set:


```python
num_dim = 3
prior = utils.BoxUniform(low=-2 * torch.ones(num_dim), high=2 * torch.ones(num_dim))

def simulator(parameter_set):
    return 1.0 + parameter_set + torch.randn(parameter_set.shape) * 0.1
```

`sbi` can then run inference:


```python
# Other methods are "SNLE" or "SNRE".
posterior = infer(simulator, prior, method="SNPE", num_simulations=1000)
# Using `init_kwargs`, `train_kwargs` and `build_posterior_kwargs`, you can also pass additional keyword arguments to `__init__`, `train` and `build_posterior` of the inference method. But we recommend to use the flexible interface which is introduced in a later tutorial.
```


    Running 1000 simulations.:   0%|          | 0/1000 [00:00<?, ?it/s]


     Neural network successfully converged after 119 epochs.

Let's say we have made some observation $x$:


```python
observation = torch.zeros(3)
```

 Given this observation, we can then sample from the posterior $p(\theta|x)$, evaluate its log-probability, or plot it.


```python
samples = posterior.sample((10000,), x=observation)
log_probability = posterior.log_prob(samples, x=observation)
_ = analysis.pairplot(samples, limits=[[-2, 2], [-2, 2], [-2, 2]], figsize=(6, 6))
```


    Drawing 10000 posterior samples:   0%|          | 0/10000 [00:00<?, ?it/s]



    
![png](00_getting_started_files/00_getting_started_11_1.png)
    


## Next steps

The single-line interface described above provides an easy entry for using `sbi`. However, on almost any real-world problem that goes beyond a simple demonstration, we strongly recommend using the [flexible interface](https://sbi-dev.github.io/sbi/tutorial/02_flexible_interface/).
