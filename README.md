# Privacy-Preserving Expectation Maximization for Gaussian Mixture Models  
*Prof. Adi Akavia's Secure Cloud Computing Laboratory, Fall 2022-2023*

## Gaussian Mixture Model (GMM) 
A Gaussian mixture model is a probabilistic model that assumes all the data points are generated from a mixture of a finite number of Gaussian distributions with unknown parameters.  
Gaussian mixture models are very useful clustering models. Note that in traditional clustering algorithms such as k-means or DBSCAN, each data point belongs to exactly one cluster (**hard clustering**). Gaussian mixture models, on the other hand, use **soft clustering** where each data point may belong to several clusters with a fractional degree of membership in each.  
In the GMM framework, each Gaussian component is characterized by its mean $\mu$, covariance matrix $\Sigma$, and mixture coefficient (weights) $\beta$.  
<img src="https://user-images.githubusercontent.com/100927079/220479823-2a37ddcf-bf37-40e5-af98-a3d6da368320.png" alt="Alt text" style="width:300px;height:300px;"> 
<img src="https://user-images.githubusercontent.com/100927079/220480649-b9bf4a5e-34b3-4ef8-bcb1-8db540f01e33.png" alt="Alt text" style="width:300px;height:300px;"> 
<img src="https://user-images.githubusercontent.com/100927079/220480758-d2949090-f2ae-42c7-8ae4-a7cace12a9ef.png" alt="Alt text" style="width:300px;height:300px;">  
  
## Expectation Maximization (EM)  
Expectation maximization is a clustering-based machine learning algorithm that is widely used in many areas of science, such as bio-informatics and computer vision, to perform maximum likelihood estimation (MLE) estimation for models with latent (hidden, unobserved) variables.  
It is an iterative algorithm that starts with an initial guess of the model's parameters (All the parameters are collectively denoted as $\theta$), and then proceeds to iteratively update $\theta_i$ until convergence:  
$\boldsymbol{E-Step:}$ For the $i^{th}$ step, we calculate how likely it is to observe the data, as a function of $\theta$.  
The equation for this calculation is: **$E[l(\theta; X, \Delta )|X, \theta_i]$**, such that X is the data, $\Delta$ is the latent data, $\theta_i$ are the parameter-estimates of the previous iteration (or initial guess), and we define $l$ as the log-likelihood function.  
$\boldsymbol{M-Step:}$ We compute parameters maximizing the expected log-likelihood found on the expectation step and call the result $\theta_{i+1}$, this is the new estimate which will be used in the next iteration of the algorithm.  
The equation for this calculation is: **$\theta_{i+1}=argmax_\theta(E[l(\theta; X, \Delta )|X, \theta_i])$**.  
  
## Expectation-Maximization for the Gaussian Mixture Model  
The expectation maximization algorithm can be applied to estimate the parameters of a Gaussian mixture model given a set of observed data.  
In the case of a GMM, the E-step involves computing the posterior probabilities of each data point belonging to each of the Gaussian components. These probabilities are used to update the estimates of the mixture weights and the means and covariances of each Gaussian component in the M-step.  
  
## Distributed Expectation-Maximization for the Gaussian Mixture Model  
We consider the scenario where $n$ parties each has its own data $x_i$ and these parties would like to collaborate to learn a GMM based on the full dataset {$\{x_1, x_2, ..., x_n\}$}. Assume there are in total $c$ Gaussian models and denote $C = \{1, ..., c\}$. Specifically, the GMM density is given by\\
$$
p(x)=\sum_{j \in C} \beta_j p(x| \mu_j, \Sigma_j)
$$
$\boldsymbol{E-Step:}$ $$P(x_i|N_j^t) = \frac{p(x_i|\mu_j, \Sigma_j) \beta_j^t}{\sum_{k=1}^{c} p(x_i|\mu_k, \Sigma_k)\beta_k^t}$$  
where $p(x_i|\mu_j, \Sigma_j)$ is the pdf for a Gaussian distribution with mean $\mu_j$ and covariance matrix $\Sigma_j$.  
$\boldsymbol{M-Step:}$  
\[\beta_j ^{t+1} = \frac{\sum_{i=1}^n P(x_i|N_j^t)}{n}\]  
  
\[\mu_j^{t+1} = \frac{\sum_{i=1}^n P(x_i|N_j^t)x_i}{\sum_{i=1}^n P(x_i|N_j^t)}\]  
  
\[\Sigma_j^{t+1} = \frac{\sum_{i=1}^n P(x_i|N_j^t)(x_i - \mu_j^t)(x_i - \mu_j^t)^\top}{\sum_{i=1}^n P(x_i|N_j^t)}\]  
  
## Privacy-Preserving Expectation Maximization (PPEM)
  








