# Local Classifier Two-Sample Tests ($\ell$-C2ST)


 After a density estimator has been trained with simulated data to obtain a posterior, the estimator should be made subject to several diagnostic tests. This diagnostic should be performed before the posterior is used for inference given the actual observed data. 
    
*Posterior Predictive Checks* (see [tutorial 10](10_diagnostics_posterior_predictive_checks.md)) provide one way to "critique" a trained estimator via its predictive performance. 
    
Another approach is *Simulation-Based Calibration* (SBC, see [tutorial 11](11_diagnostics_simulation_based_calibration.md)). SBC evaluates whether the estimated posterior is balanced, i.e., neither over-confident nor under-confident. These checks are performed ***in expectation (on average) over the observation space***, i.e. they are performed on a set of $(\theta,x)$ pairs sampled from the joint distribution over simulator parameters $\theta$ and corresponding observations $x$. As such, SBC is a ***global validation method*** that can be viewed as a necessary condition (but not sufficient) for a valid inference algorithm: If SBC checks fail, this tells you that your inference is invalid. If SBC checks pass, *this is no guarantee that the posterior estimation is working*.

**Local Classifier Two-Sample Tests** ($\ell$-C2ST) as developed by [Linhart et al, 2023](https://arxiv.org/abs/2306.03580) present a new ***local validation method*** that allows to evaluate the correctness of the posterior estimator ***at a fixed observation***, i.e. they work on a single $(\theta,x)$ pair. They provide necessary *and sufficient* conditions for the validity of the SBI algorithm, as well as easy-to-interpret qualitative and quantitative diagnostics. 
    
If global checks (like SBC) fail, $\ell$-C2ST allows to further investigate where (for which observation) and why (bias, overdispersion, etc.) the posterior estimator fails. If global validation checks pass, $\ell$-C2ST allows to guarantee whether the inference is correct for a specific observation.

## In a nutshell

Suppose you have an "amortized" posterior estimator $q_\phi(\theta\mid x)$, meaning that we can quickly get samples for any new observation $x$. The goal is to test the *local consistency* of our estimator at a fixed observation $x_\mathrm{o}$, i.e. whether the following null hypothesis holds about $q_\phi(\theta\mid x)$ and the true posterior $p(\theta\mid x)$:

$$\mathcal{H}_0(x_\mathrm{o}) := q_\phi(\theta\mid x_\mathrm{o}) = p(\theta \mid x_\mathrm{o}), \quad \forall \theta \in \mathbb{R}^m$$

To run $\ell$-C2ST, 

1. we sample **new** parameters from the prior of the problem at hand: $\Theta_i \sim p(\theta)$
2. we simulate corresponding "observations": $X_i = \mathrm{Simulator}(\Theta_i) \sim p(x\mid \Theta_i)$
3. we sample the estimated posterior at each observation: $Q_i \sim q_\phi(\theta \mid X_i)$

This creates a calibration dataset of samples from the "estimated" and true joint distributions on which we train a binary classifier $d(\theta, x)$ to distinguish between the estimated joint $q(\theta \mid x)p(x)$ (class $C=0$) and the true joint distribution $p(\theta)p(x\mid\theta)$ (class $C=1$):

$$\mathcal{D}_\mathrm{cal} = \left \{\underbrace{(Q_i, X_i)}_{(C=0)} \cup \underbrace{(\Theta_i, X_i)}_{(C=1)} \right \}_{i=1}^{N_\mathrm{cal}}$$

> Note: $D_\mathrm{cal}$ contains data from the joint distribution (over prior and simulator) that have to be **different from the data used to train the posterior estimator**. $N_\mathrm{cal}$ is typically smaller than $N_\mathrm{train}$, the number of training samples for the posterior estimator, but has to be sufficiently large to allow the convergence of the classifier. For a fixed simulation budget, a rule of thumb is to use $90\%$ for the posterior estimation and $10\%$ for the calibration.

Once the classifier is trained, we evaluate it for a given observation $x^\star$ and multiple samples $Q^\star_i \sim q_\phi(\theta \mid x^\star)$. This gives us a set of predicted probabilities $\left\{d(Q^\star_i, x^\star)\right\}_{i=1}^{N_\mathrm{eval}}$ that are then used to compute the different diagnostics. This proceedure can be repeated for several different observations, without having to retrain the classifiers, which allows to perform an efficient and thorough analysis of the failure modes of the posterior estimator.

> Note: The number of evaluation samples can be arbitrarily large (typically we use $N_\mathrm{eval} = 10\,000$), because we suppose our posterior estimator to be amortized. 

### Key ideas behind $\ell$-C2ST

$\ell$-C2ST allows to evaluate the correctness your posterior estimator *without requiring access to samples from the true posterior*. It is built on the following two key ideas:

1. **Train the classifier on the joint:** this allows to implicitly learn the distance between the true and estimated posterior for any observation (we could call this step "amortized" C2ST training). 

2. **Local evaluation on data from one class only:** we use a metric that, as opposed to the accuracy (used in C2ST) does not require samples from the true posterior, only the estimator. It consists in the Mean Squared Error (MSE) between the predicted probabilities for samples from the estimator evaluated at the given observation and one half.

> Note: A predicted probability of one half corresponds to the chance level or total uncertainty of the classifier, that is unable to distinguish between the two data classes.

The MSE metric is used as a test statistic for a hypothesis test that gives us theoretical guarantees on the correctness of the posterior estimator (at the considered observation), as well as easy-to-interpret diagnostics that allow to investigate its failure modes.

>**Quick reminder on hypothesis tests.** Additionaly to the observed test statistic $T^\star$, evaluating the test requires to
>1. compute the test statistics $T_h$ under the null hyposthesis (H0) of equal (true and estimated) distributions over multiple trials $h$.
>2. compute the p-value $p_v = \frac{1}{H}\sum_{h=1}^H \mathbb{I}(T_h > T^\star)$: *"How many times is the observed test statistic "better" (i.e. below) the test statistic computed under H0?"*
>3. choose a significance level $\alpha$ (typically $0.05$) that defines the rejection threshold and evaluate the test:
>- **quantitatively:** a p-value below this level indicates the rejection of the null hypothesis, meaning the detection of significant differences between the true and the estimated posterior. 
>- **qualitatively:** P-P plots: visually check whether the distribution of $T^\star$ falls into the $1-\alpha$ confidence region, computed by taking the corresponding quantiles of $(T_1,\dots, T_H)$.

### What can $\ell$-C2ST diagnose?

- **Quantitatively:** the MSE metric (or test statistic) gives us a distance measure between the estimated and true posterior that can be quickly evaluated for any new observation $x^\star$. Comparing it to the values of the null-distribution gives us the p-values that are used to check how significant their differences are. If the check passes (no significant differences), this tells us that we can be confident about the correctness of the estimator, but only upto to a certain confidence level (typically $95\%$). 

- **Qualitatively:** we can choose to look at the predicted probabilities used to compute the MSE metric. P-P plots allow to evaluate a general trend of over or under confidence, by comparing theire distribution to the confidence region (obtained for probabilities predicted under H0). We can go further and map these predicted probabilities to a pairplot of the samples they were evaluated on, shows us the regions of over and underconfidence of the estimator. This allows us to investigate the nature of the inconsistencies, such as positive/negative bias or under/over dispersion.

> Note: High (resp. low) predicted probability indicates that the classifier is confident about the fact that the sample belongs to the estimated posterior (resp. to the true posterior). This means that the estimator associates too much (resp. not enough) mass to this sample. In other words it is "over-confident" (resp. "under-confident"). 



To summarize $\ell$-C2ST can:

- tell you whether your posterior estimator is valid for a given observation (with a guaranteed confidence)
- show you where (for which observation) and why (bais, overdispersion, etc.) it fails 

## Illustration on a benchmark SBI example

We consider the Gaussian Mixture SBI task from [Lueckmann et al, 2021](https://arxiv.org/abs/2101.04653). It consists of inferring the common mean of a mixture of two 2D Gaussian distributions, one with much broader covariance than the other:
- Prior: $p(\theta) = \mathcal{U}(-10,10)$
- Simulator: $p(x|\theta) = 0.5 \mathcal{N}(\theta, \mathbf{I}_2)+ 0.5 \mathcal{N}(\theta, 0.1 \times \mathbf{I}_2)$
- Dimensionality: $\theta \in \mathbb{R}^2$, $x \in \mathbb{R}^2$


```python
import matplotlib.pyplot as plt
import numpy as np
import torch
```

### SBI Task


```python
from sbi.simulators.gaussian_mixture import (
    gaussian_mixture,
    uniform_prior_gaussian_mixture,
)

# SBI task: prior and simualtor
dim = 2
prior = uniform_prior_gaussian_mixture(dim=dim)
simulator = gaussian_mixture

# Number of samples for training, calibration and evaluation
NUM_TRAIN = 10_000
NUM_CAL = int(0.1 * NUM_TRAIN) # 10% of the training data
NUM_EVAL = 10_000
```

### Posterior Inference

We use neural posterior estimation as our SBI-algorithm with a MAF as underlying density estimator. 

> Note: Here you could use any other SBI algorithm of your own choosing (e.g. NRE, NLE, etc.). IMPORTANT: make sure it is amortized (which corresponds to sequential methods with a signle round), so sampling the posterior can be performed quickly.

We train the estimator on a small training set (`small_num_train=1000`) over a small number of epochs (`max_num_epochs=10`), which means that it doesn't converge. Therefore the diagnostics should detect major differences between the estimated and the true posterior, i.e. the null hypothesis is rejected.

> Note: You can play with the number of training samples or epochs to see whether this influences the quality of the posterior estimator and how it is reflected in the diagnostics.


```python
from sbi.inference import SNPE

torch.manual_seed(42) # seed for reproducibility

# Sample training data for the density estimator
small_num_train = 1000
theta_train = prior.sample((NUM_TRAIN,))[:small_num_train]
x_train = simulator(theta_train)[:small_num_train]

# Train the neural posterior estimators
torch.manual_seed(42) # seed for reproducibility
inference = SNPE(prior, density_estimator='maf', device='cpu')
inference = inference.append_simulations(theta=theta_train, x=x_train)
npe = inference.train(training_batch_size=256, max_num_epochs=10)
```

    WARNING (pytensor.tensor.blas): Using NumPy C-API based implementation for BLAS functions.


     Training neural network. Epochs trained: 1 Training neural network. Epochs trained: 2 Training neural network. Epochs trained: 3 Training neural network. Epochs trained: 4 Training neural network. Epochs trained: 5 Training neural network. Epochs trained: 6 Training neural network. Epochs trained: 7 Training neural network. Epochs trained: 8 Training neural network. Epochs trained: 9 Training neural network. Epochs trained: 10 Training neural network. Epochs trained: 11

### Evaluate the posterior estimator

We choose to evaluate the posterior estimator at three different observations, simulated from parameters independently sampled from the prior: 
$$\theta^\star_i \sim p(\theta) \quad \rightarrow \quad x^\star_i \sim p(x\mid \theta_i), \quad i=1,2,3~.$$


```python
from sbi.simulators.gaussian_mixture import (
    samples_true_posterior_gaussian_mixture_uniform_prior,
)

# get reference observations
torch.manual_seed(0) # seed for reproducibility
thetas_star = prior.sample((3,))
xs_star = simulator(thetas_star)

# Sample from the true and estimated posterior
post_samples_star = {}
ref_samples_star = {}
for i,x in enumerate(xs_star):
    post_samples_star[i] = npe.sample(
        (NUM_EVAL,), condition=x[None,:]
    ).reshape(-1, thetas_star.shape[-1]).detach()
    ref_samples_star[i] = samples_true_posterior_gaussian_mixture_uniform_prior(
        x_o=x[None,:],
        num_samples=1000,
    )
```

#### Set-up $\ell$-C2ST

To setup the hypothesis test, we train the classifiers on the calibration dataset in two settings:
- `train_under_null_hypothesis`: uses the permutation method to train the classifiers under the nulll hypothesis over several trials
- `train_on_observed_data`: train the the classifier once on the observed data.

For any new observation `x_o`, this allows to quickly compute (without having to retrain the classifiers) the test statistics `T_null` under the null hypothesis and `T_data` on the observed data. They will be used to compute the diagnostics (p-value or P-P plots).

>Note: we choose the default configuration with a MLP classifier (`classifier='mlp'`). You can also choose to use the default Random Forest classifier (`classifier='random_forest'`) or use your own custom `sklearn` classifier by specifying `clf_class` and `clf_kwargs` during the initialization of the `LC2ST` class. You can also use an ensemble classifier by setting `num_ensemble` > 1 for more stable classifier predictions (see the `EnsembleClassifier` class in `sbi/diagnostics/lc2st.py`).


```python
from sbi.diagnostics.lc2st import LC2ST

torch.manual_seed(42) # seed for reproducibility

# sample calibration data
theta_cal = prior.sample((NUM_CAL,))
x_cal = simulator(theta_cal)
post_samples_cal = npe.sample((1,), x_cal).reshape(-1, theta_cal.shape[-1]).detach()

# set up the LC2ST: train the classifiers
lc2st = LC2ST(
    thetas=theta_cal,
    xs=x_cal,
    posterior_samples=post_samples_cal,
    classifier="mlp",
    num_ensemble=1, # number of classifiers for the ensemble
)
_ = lc2st.train_under_null_hypothesis() # over 100 trials under (H0)
_ = lc2st.train_on_observed_data() # on observed data
```

    Training the classifiers under H0, permutation = True: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 100/100 [00:10<00:00,  9.58it/s]



```python
# Define significance level for diagnostics
conf_alpha = 0.05
```

#### Quantitative diagnostics
We here compute the test statistics and p-values for three different observations `x_o` (as mentioned above, this is done in an amortized way without having to retrain the classifiers). 

> Note: The p-value associated to the test corresponds to the proportion of times the L-C2ST statistic under the null hypothesis $\{T_h\}_{h=1}^H$ is greater than the L-C2ST statistic $T_\mathrm{o}$ at the observation `x_o`. It is computed by taking the empirical mean over statistics computed on several trials under the null hypothesis: $$\text{p-value}(x_\mathrm{o}) = \frac{1}{H} \sum_{h=1}^{H} I(T_h < T_o)~.$$


```python
fig, axes = plt.subplots(1,len(thetas_star), figsize=(12,3))
for i in range(len(thetas_star)):
    probs, scores = lc2st.get_scores(
        theta_o=post_samples_star[i],
        x_o=xs_star[i],
        return_probs=True,
        trained_clfs=lc2st.trained_clfs
    )
    T_data = lc2st.get_statistic_on_observed_data(
        theta_o=post_samples_star[i],
        x_o=xs_star[i]
    )
    T_null = lc2st.get_statistics_under_null_hypothesis(
        theta_o=post_samples_star[i],
        x_o=xs_star[i]
    )
    p_value = lc2st.p_value(post_samples_star[i], xs_star[i])
    reject = lc2st.reject_test(post_samples_star[i], xs_star[i], alpha=conf_alpha)

    # plot 95% confidence interval
    quantiles = np.quantile(T_null, [0, 1-conf_alpha])
    axes[i].hist(T_null, bins=50, density=True, alpha=0.5, label="Null")
    axes[i].axvline(T_data, color="red", label="Observed")
    axes[i].axvline(quantiles[0], color="black", linestyle="--", label="95% CI")
    axes[i].axvline(quantiles[1], color="black", linestyle="--")
    axes[i].set_xlabel("Test statistic")
    axes[i].set_ylabel("Density")
    axes[i].set_xlim(-0.01,0.25)
    axes[i].set_title(
        f"observation {i+1} \n p-value = {p_value:.3f}, reject = {reject}"
    )
axes[-1].legend(bbox_to_anchor=(1.1, .5), loc='center left')
plt.show()
```


    
![png](13_diagnostics_lc2st_files/13_diagnostics_lc2st_14_0.png)
    


**Results:** the plots show the test statistics under the null hypothesis `T_null` (in blue) defining the $95\%$ (`1 - conf_alpha`) confidence region (black dotted lines). The test statistic correponding to the observed data `T_data` (red) is outside of the confidence region, indicating the **rejection of the null hypothesis** and therefore a **"bad" posterior estimator**.

#### Qualitative diagnostics

##### P-P plots

P-P plots allow to evaluate a general trend of over- or under- confidence, by comparing the predicted probabilities of belonging to the estimated posterior (class 0). If the red curve is not fully contained in the gray confidence region, this means that the test rejects the null hypothesis and that a significant discrepancy from the true posterior is detected. Here two scenarios are possible:
- **over-confidence**: the red curve is mostly on the **right side** of the gray CR (high probabilities are predominant)
- **under-confidence**: the red curve is mostly on the **left side** of the gray CR (low probabilities are predominant)

> Note: The predominance of high (resp. low) probabilities indicates a classifier that is mostly confident about predicting the class corresponding to the estimated (resp. true) posterior. This in turn means that the estimator associates too much (resp. not enough) mass to the evaluation space, i.e. is overall over confident (resp. under confident).


```python
# P-P plots
from sbi.analysis.plot import pp_plot_lc2st

fig, axes = plt.subplots(1,len(thetas_star), figsize=(12,3))
for i in range(len(thetas_star)):
    probs_data, _ = lc2st.get_scores(
        theta_o=post_samples_star[i],
        x_o=xs_star[i],
        return_probs=True,
        trained_clfs=lc2st.trained_clfs
    )
    probs_null, _ = lc2st.get_statistics_under_null_hypothesis(
        theta_o=post_samples_star[i],
        x_o=xs_star[i],
        return_probs=True
    )

    pp_plot_lc2st(
        probs=[probs_data],
        probs_null=probs_null,
        conf_alpha=conf_alpha,
        labels=["Classifier probabilities \n on observed data"],
        colors=["red"],
        ax=axes[i],
    )
    axes[i].set_title(f"PP-plot for observation {i+1}")
axes[-1].legend(bbox_to_anchor=(1.1, .5), loc='center left')
plt.show()
```


    
![png](13_diagnostics_lc2st_files/13_diagnostics_lc2st_18_0.png)
    


**Results:** the plots below show a general trend of overconfident behavior (red curves on the right side of the black dots).

##### Pairplot with heatmap of classifier probabilities

We can go further and map these predicted probabilities to a pairplot of the samples they were evaluated on, which shows us the regions of over and underconfidence of the estimator. This allows us to investigate the nature of the inconsistencies, such as positive/negative bias or under/over dispersion.

> Note: High (resp. low) predicted probability indicates that the classifier is confident about the fact that the sample belongs to the estimated posterior (resp. to the true posterior). This means that the estimator associates too much (resp. not enough) mass to this sample. In other words it is "over-confident" (resp. "under-confident"). 


```python
from sbi.analysis.plot import marginal_plot_with_probs_intensity
from sbi.utils.analysis_utils import get_probs_per_marginal

label = "Probabilities (class 0)"
# label = r"$\hat{p}(\Theta\sim q_{\phi}(\theta \mid x_0) \mid x_0)$"

fig, axes = plt.subplots(len(thetas_star), 3, figsize=(9,6), constrained_layout=True)
for i in range(len(thetas_star)):
    probs_data, _ = lc2st.get_scores(
        theta_o=post_samples_star[i][:1000],
        x_o=xs_star[i],
        return_probs=True,
        trained_clfs=lc2st.trained_clfs
    )
    dict_probs_marginals = get_probs_per_marginal(
        probs_data[0],
        post_samples_star[i][:1000].numpy()
    )
    # 2d histogram
    marginal_plot_with_probs_intensity(
        dict_probs_marginals['0_1'],
        marginal_dim=2,
        ax=axes[i][0],
        n_bins=50,
        label=label
    )
    axes[i][0].scatter(
        ref_samples_star[i][:,0],
        ref_samples_star[i][:,1],
        alpha=0.2,
        color="gray",
        label="True posterior"
    )

    # marginal 1
    marginal_plot_with_probs_intensity(
        dict_probs_marginals['0'],
        marginal_dim=1,
        ax=axes[i][1],
        n_bins=50,
        label=label,
    )
    axes[i][1].hist(
        ref_samples_star[i][:,0],
        density=True,
        bins=10,
        alpha=0.5,
        label="True Posterior",
        color="gray"
    )

    # marginal 2
    marginal_plot_with_probs_intensity(
        dict_probs_marginals['1'],
        marginal_dim=1,
        ax=axes[i][2],
        n_bins=50,
        label=label,
    )
    axes[i][2].hist(
        ref_samples_star[i][:,1],
        density=True,
        bins=10,
        alpha=0.5,
        label="True posterior",
        color="gray"
    )

axes[0][1].set_title("marginal 1")
axes[0][2].set_title("marginal 2")

for j in range(3):
    axes[j][0].set_ylabel(f"observation {j + 1}")
axes[0][2].legend()
plt.show()
```


    
![png](13_diagnostics_lc2st_files/13_diagnostics_lc2st_21_0.png)
    


**Results**: the plots below indicate **over dispersion** of our estimator at all three considered observations. Indeed, the 2D histograms display a small blue-green region at the center where the estimator is "underconfident", surrounded by a yellow region of "equal probability", and the rest of the estimated posterior samlpes correspond to the red regions of "overconfidence". 

**Validation** of the diagnostic tool: we verify the statement of over dispersion by plotting the true posterior samples (in grey) and are happy to see that they fall into the underconfident region of the estimator. 

## Classifier choice and calibration data size: how to ensure meaningful test results

### Choice of the classifier
If you are not sure about which classifier architecture is best for your data, you can do a quick check by looking at the variance of the results over different random state initializations of the classifier: For `i=1,2,...` 
1. train the ith classifier: run `lc2st.train_on_observed_data(seed=i)` 
2. compute the corresponding test statistic for a dataset `theta_o, x_o`: `T_i = lc2st.get_statistic_on_observed_data(theta_o, x_o)`

For different classifier architectures, you should choose the one with the smallest variance. 

### Number of calibration samples
A similar check can also be performed via cross-validation: set the `num_folds` parameter of your `LC2ST` object, train on observed data and call `lc2st.get_scores(theta_o, x_o, lc2st.trained_clfs)`. This outputs the test statistics obtained for each cv-fold. You should choose the smallest calibration set size that gives you a small enough variance over the test statistics. 

> Note: Ideally, these checks should be performed in a **separable data setting**, i.e. for a dataset `theta_o, x_o` coming from a sub-optimal estimator: the classifier is supposed to be able to discriminate between the two classes; the test is supposed to be rejected; the variance is supposed to be small. In other words, we are ensuring a **high statistical power** (our true positive rate) of our test. If you want to be really rigurous, you should also check the type I error (or false positive rate), that should be controlled by the significance level of your test (cf. Figure 2 in [[Linhart et al., 2023]](https://arxiv.org/abs/2306.03580)).

### Reducing the variance of the test results
To ensure more stable results, you can play with the following `LC2ST` parameters:
- `num_ensemble`: number of classifiers used for ensembling. An ensemble classifier is a set of classifiers initialized with different `random_state`s and whose predicted class probalility is the mean probability over all classifiers. It reduces the variance coming from the classifier itself.
- `num_folds`: number of folds used for cross-validation. It reduces the variance coming from the data.

As these numbers increase the results become more stable (less variance) and the test becomes more disciminative (smaller confidence region).
Both can be combined (i.e. you can perform cross-validation on an ensemble classifier). 

> Note: Be careful, you don't want your test to be too discriminative!

## The case of Normalizing Flows ($\ell$-C2ST-NF)

$\ell$-C2ST can also be specialized for normalizing flows,leading to improved test performance. The idea is to train and evaluate the classifiers in the space of the base distribution of the normalizing flow, instead of the parameter space that can be highly structured. 
Following Theorem 4 of [[Linhart et al., 2023]](https://arxiv.org/abs/2306.03580), the null hypothesis $\mathcal{H}_0(x_\mathrm{o}) := q_\phi(\theta\mid x_\mathrm{o}) = p(\theta \mid x_\mathrm{o})$ of *local consistency* holds if, and only if, the inverse flow transformation applied to the target distribution recovers the base distribution. This gives us the following new null hypothesis for posterior estimators based on normalizing flows (cf. Eq. 17 in [[Linhart et al., 2023]](https://arxiv.org/abs/2306.03580)):

$$\mathcal{H}_0(x_\mathrm{o}) := p(T_\phi^{-1}(\theta ; x_\mathrm{o}) \mid x_\mathrm{o}) = \mathcal{N}(0, \mathbf{I}_m), \quad \forall \theta \in \mathbb{R}^m~,$$

which leads to a new binary classification framework to discriminate between the joint distributions $\mathcal{N}(0, \mathbf{I}_m)p(x)$ (class $C=0$) and $p(T_\phi^{-1}(\theta ; x_\mathrm{o}), x_\mathrm{o})$ (class $C=1$).

This results in two main advantages leading to a statistically more performant and flexible test: 
- **easier classification task:** it is easier to discriminate samples w.r.t. a simple Gaussian than a complex (e.g. multimodal) posterior. 
- **an analytically known null distribution:** it consists of the base distribution of the flow, which is **independant of $x$ and the posterior estimator**. This also allows to pre-compute the null distribution and re-use it for any new posterior estimator you whish to evaluate. 

>Remember that the original $\ell$-C2ST relies on a permutation method to approximate the null distribution.

The new method is implemented within the `LC2ST_NF` class, built on the `LC2ST` class with following major changes:
- no evaluation samples `theta_o` have to be passed to the evaluation methods (e.g. `get_scores_on_observed_data`, `get_statistic_on_observed_data`, `p_value`, etc.)
- the precomputed `trained_clfs_null` can be passed at initialization
- no permutation method is used inside `train_under_null_hypothesis`


> Note: **Quick reminder on Normalizing Flows.** We consider a **conditional Normalizing Flow** $q_{\phi}(\theta \mid x)$ with base distribution $p(z) = \mathcal{N}(0,\mathbf{1}_m)$ and bijective transormation $T_{\phi}(.; x)$ defined on $\mathbb{R}^2$ and for all $x \in \mathbb{R}^2$ for our example problem in 2D. Sampling from the normalizing flow consists of applying the forward transformation $T_\phi$:
>$$\theta = T_{\phi}(z; x) \sim q_{\phi}(\theta \mid x), \quad z\sim p(z)~.$$
>**Characterization of the null hypothesis.** Comparing the estimated and true posterior distributions is equivalent to comparing the base distribution to the inversely transformed prior samples: 
>$$ p(\theta \mid x) = q_{\phi}(\theta \mid x) \iff p(T_{\phi}^{-1}(\theta; x)\mid x) = p(T_{\phi}^{-1}(T_{\phi}(z; x); x)) = p(z) = \mathcal{N}(0,\mathbf{1}_m)$$

### Set up $\ell$-C2ST-NF

The setup of the NF version is the same as for the original $\ell$-C2ST, but the trained classifiers can be used to compute test results and diagnostics for any new observation **and new posterior estimator**.


```python
from sbi.diagnostics.lc2st import LC2ST_NF

flow_inverse_transform = lambda theta, x: npe.net._transform(theta, context=x)[0]
flow_base_dist = torch.distributions.MultivariateNormal(
    torch.zeros(2), torch.eye(2)
) # same as npe.net._distribution

lc2st_nf = LC2ST_NF(
    thetas=theta_cal,
    xs=x_cal,
    posterior_samples=post_samples_cal,
    flow_inverse_transform=flow_inverse_transform,
    flow_base_dist=flow_base_dist,
    num_ensemble=1,
)
_ = lc2st_nf.train_under_null_hypothesis()
_ = lc2st_nf.train_on_observed_data()
```

    Training the classifiers under H0, permutation = False: 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 100/100 [00:08<00:00, 11.83it/s]



```python
# Define significance level
conf_alpha = 0.05
```

#### Quantitative diagnostics
Same as before: we compute test statistics, confidence regions and p-values.


```python
fig, axes = plt.subplots(1,len(thetas_star), figsize=(12,3))
for i in range(len(thetas_star)):
    probs, scores = lc2st_nf.get_scores(
        x_o=xs_star[i],
        return_probs=True,
        trained_clfs=lc2st_nf.trained_clfs
    )
    T_data = lc2st_nf.get_statistic_on_observed_data(x_o=xs_star[i])
    T_null = lc2st_nf.get_statistics_under_null_hypothesis(x_o=xs_star[i])
    p_value = lc2st_nf.p_value(xs_star[i])
    reject = lc2st_nf.reject_test(xs_star[i], alpha=conf_alpha)

    # plot 95% confidence interval
    quantiles = np.quantile(T_null, [0, 1-conf_alpha])
    axes[i].hist(T_null, bins=50, density=True, alpha=0.5, label="Null")
    axes[i].axvline(T_data, color="red", label="Observed")
    axes[i].axvline(quantiles[0], color="black", linestyle="--", label="95% CI")
    axes[i].axvline(quantiles[1], color="black", linestyle="--")
    axes[i].set_xlabel("Test statistic")
    axes[i].set_ylabel("Density")
    axes[i].set_xlim(-0.01,0.25)
    axes[i].set_title(
        f"observation {i+1} \n p-value = {p_value:.3f}, reject = {reject}"
    )
axes[-1].legend(bbox_to_anchor=(1.1, .5), loc='center left')
plt.show()
```


    
![png](13_diagnostics_lc2st_files/13_diagnostics_lc2st_29_0.png)
    


**Results:** Again the test hypothesis is rejected for all three observations.

#### Qualitative diagnostics

##### P-P plots

**Results:** As before, the plots below show a general trend of overconfident behavior (red curves on the right side of the black dots).


```python
# P-P plots
from sbi.analysis.plot import pp_plot_lc2st

fig, axes = plt.subplots(1,len(thetas_star), figsize=(12,3))
for i in range(len(thetas_star)):
    probs_data, _ = lc2st_nf.get_scores(
        x_o=xs_star[i],
        return_probs=True,
        trained_clfs=lc2st_nf.trained_clfs
    )
    probs_null, _ = lc2st_nf.get_statistics_under_null_hypothesis(
        x_o=xs_star[i],
        return_probs=True
    )

    pp_plot_lc2st(
        probs=[probs_data],
        probs_null=probs_null,
        conf_alpha=conf_alpha,
        labels=["Classifier probabilities \n on observed data"],
        colors=["red"],
        ax=axes[i],
    )
    axes[i].set_title(f"PP-plot for observation {i+1}")
axes[-1].legend(bbox_to_anchor=(1.1, .5), loc='center left')
plt.show()
```


    
![png](13_diagnostics_lc2st_files/13_diagnostics_lc2st_33_0.png)
    


##### Heatmap of classifier probabilities

For the NF case and as displayed in the plots below, we can choose to plot the heatmap of predicted classifier probabilities in the base distribution space, instead of the parameter space, which can be easier to interpret if the posterior space is highly structured.


```python
from sbi.analysis.plot import marginal_plot_with_probs_intensity
from sbi.utils.analysis_utils import get_probs_per_marginal

label = "Probabilities (class 0)"
# label = r"$\hat{p}(Z\sim\mathcal{N}(0,1)\mid x_0)$"

fig, axes = plt.subplots(len(thetas_star), 3, figsize=(9,6), constrained_layout=True)
for i in range(len(thetas_star)):
    inv_ref_samples = lc2st_nf.flow_inverse_transform(
        ref_samples_star[i], xs_star[i]
    ).detach()
    probs_data, _ = lc2st_nf.get_scores(
        x_o=xs_star[i],
        return_probs=True,
        trained_clfs=lc2st_nf.trained_clfs
    )
    marginal_probs = get_probs_per_marginal(
        probs_data[0],
        lc2st_nf.theta_o.numpy()
    )
    # 2d histogram
    marginal_plot_with_probs_intensity(
        marginal_probs['0_1'],
        marginal_dim=2,
        ax=axes[i][0],
        n_bins=50,
        label=label
    )
    axes[i][0].scatter(
        inv_ref_samples[:,0],
        inv_ref_samples[:,1],
        alpha=0.2, color="gray",
        label="True posterior"
    )

    # marginal 1
    marginal_plot_with_probs_intensity(
        marginal_probs['0'],
        marginal_dim=1,
        ax=axes[i][1],
        n_bins=50,
        label=label
    )
    axes[i][1].hist(
        inv_ref_samples[:,0],
        density=True,
        bins=10,
        alpha=0.5,
        label="True Posterior",
        color="gray"
    )

    # marginal 2
    marginal_plot_with_probs_intensity(
        marginal_probs['1'],
        marginal_dim=1,
        ax=axes[i][2],
        n_bins=50,
        label=label
    )
    axes[i][2].hist(
        inv_ref_samples[:,1],
        density=True,
        bins=10,
        alpha=0.5,
        label="True posterior",
        color="gray"
    )

axes[0][1].set_title("marginal 1")
axes[0][2].set_title("marginal 2")

for j in range(3):
    axes[j][0].set_ylabel(f"observation {j + 1}")
axes[0][2].legend()
plt.show()
```


    
![png](13_diagnostics_lc2st_files/13_diagnostics_lc2st_35_0.png)
    


**Results:** Again, the plots below confirm that the true posterior samples (in grey) correspond to regions of "underconfidence" (blue-green) or "equal probability" (yellow), indicating over dispersion of our posterior esimator.
