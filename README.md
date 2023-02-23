# Privacy-Preserving Distributed Expectation Maximization for Gaussian Mixture Models  
*Prof. Adi Akavia's Secure Cloud Computing Laboratory, Fall 2022-2023*

## Gaussian Mixture Model (GMM) 
A Gaussian mixture model is a probabilistic model that assumes all the data points are generated from a mixture of a finite number of Gaussian distributions with unknown parameters.  
Gaussian mixture models are very useful clustering models. Note that in traditional clustering algorithms such as k-means or DBSCAN, each data point belongs to exactly one cluster (**hard clustering**). Gaussian mixture models, on the other hand, use **soft clustering** where each data point may belong to several clusters with a fractional degree of membership in each.  
In the GMM framework, each Gaussian component is characterized by its mean $\mu$, covariance matrix $\Sigma$, and mixture coefficient (weight) $\beta$.  
<img src="https://user-images.githubusercontent.com/100927079/220479823-2a37ddcf-bf37-40e5-af98-a3d6da368320.png" alt="Alt text" style="width:200px;height:200px;"> 
<img src="https://user-images.githubusercontent.com/100927079/220480649-b9bf4a5e-34b3-4ef8-bcb1-8db540f01e33.png" alt="Alt text" style="width:200px;height:200px;"> 
<img src="https://user-images.githubusercontent.com/100927079/220480758-d2949090-f2ae-42c7-8ae4-a7cace12a9ef.png" alt="Alt text" style="width:200px;height:200px;">  
  
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
<img src="https://user-images.githubusercontent.com/100927079/221018152-9f641493-9db4-42f6-a7d6-4ec30a03dc50.gif" width="200" height="200" />


## Distributed Expectation-Maximization for the Gaussian Mixture Model  
Consider the scenario where $n$ parties each has its own data $x_i$ and these parties would like to collaborate to learn a GMM based on the full dataset { $x_1, x_2, ..., x_n$ }. Assuming there are $c$ Gaussian components, the GMM density is given by: $p(x)=\Sigma_{j=1}^c \beta_j p(x| \mu_j, \Sigma_j)$, where $\beta_j$ is the mixing coefficient of the $j^{th}$ Gaussian component, and $\mu_j$ and $\Sigma_j$ are the mean and covariance, respectively, of the $j^{th}$ Gaussian component.
  

The EM algorithm is iterative and for each iteration $t$, the following steps are taken for all Gaussian components:  
  
$\boldsymbol{E-Step:}$  
$$P(x_i|N_j^t) = \frac{p(x_i|\mu_j, \Sigma_j) \beta_j^t}{ \Sigma_{k=1}^c p(x_i|\mu_k, \Sigma_k)\beta_k^t}$$  
where $p(x_i|\mu_k, \Sigma_k)$ is the pdf for a Gaussian distribution with mean $\mu_k$ and covariance matrix $\Sigma_k$, and $\beta_k$ is the mixing coefficient of the $k^{th}$ Gaussian component.  
  
$\boldsymbol{M-Step:}$    

$$\beta_j^{t+1} = \frac{\Sigma_{i=1}^n P(x_i|N_j^t)}{n}$$   
  
$$\mu_j^{t+1} = \frac{\Sigma_{i=1}^n P(x_i|N_j^t) x_i}{\Sigma_{i=1}^n P(x_i|N_j^t)}$$  
  
$$\Sigma_j^{t+1} = \frac{\Sigma_{i=1}^n P(x_i|N_j^t) (x_i-μ_j^t) (x_i-μ_j^t)^\top}{\Sigma_{i=1}^n P(x_i|N_j^t)}$$  
  
where $P(x_i|N_j^t)$ denotes the conditional probability that data $x_i$ belongs to Gaussian model $j$ (result of the E-Step).  
  
  
## Privacy-Preserving Expectation Maximization (PPEM)  
To deploy such an algorithm in cloud environments, security and privacy issues need be considered to avoid data breaches or abuses by external malicious parties or even by cloud service providers.  
  
**Existing approaches for PPEM:**  
- *Differential Privacy (DP) based PPEM*: The DP-based PPEM approaches perturb the data to prevent sensitive information from being leaked. One such approach is the DP-EM algorithm that adds noise to the EM algorithm's update steps to ensure differential privacy.  
- *Homomorphic Encryption (HE) based PPEM*: Homomorphic encryption allows computation on encrypted data without decryption, enabling privacy-preserving computation. The HE-based PPEM approaches encrypt the data before using the EM algorithm, ensuring that sensitive information is not leaked.
- *Federated Learning based PPEM*: Federated Learning is a machine learning technique that enables training on decentralized data. The Federated EM algorithm is a variant of the EM algorithm that uses Federated Learning to train a model on multiple devices without centralizing the data.  
- *Secure Multi-Party Computation (SMPC) based PPEM*: Secure Multi-Party Computation (SMPC) is a cryptographic protocol that allows multiple parties to compute a function while keeping their inputs private. SMPC-based PPEM approaches enable multiple parties to run the EM algorithm on their local data without sharing it, ensuring privacy.


## Proposed Approach  
We aim to find a privacy-preserving solution for distributed expectation maximization for Gaussian mixture models. Our method involves utilizing fully homomorphic encryption to facilitate a privacy-preserving centralized federated learning approach.  
  
We address the following scenario:  
- Data is distributed among many parties: there are $n$ parties, each holding its own private data $x_i$ (a point) and we wish to fit a GMM to the full dataset.  
- We propose a client-server model, where the cloud service is an untrusted third party and acts as the central server, providing a service to the clients who are the owners of the private data.  
- We assume an Honest-but-Curious adversary and do not consider the Malicious case, thus we can assume that the server (the untrusted third party, the "cloud") is not mailcious.  
  
It's worth noting that in the distributed version of the Expectation Maximization algorithm, the $\{E-Step}$ can be computed locally. This means that each party can perform the E-step on its own data, thus preserving data privacy. However, the $\{M-Step}$ requires data aggregation to compute global updates of the Gaussian components' parameters, which raises privacy concerns. To address this, we simplify the M-step by breaking it down into intermediate updates that are also computed locally and will periodically be communicated with the central server.  
Each party computes the following:  
$$a_{ij}^t = P(x_i|N_j^t)$$ 
$$b_{ij}^t = P(x_i|N_j^t)x_i$$
$$c_{ij}^t = P(x_i|N_j^t)(x_i - \mu_j^t)(x_i - \mu_j^t)^\top$$  
  
where $P(x_i|N_j^t)$ is the result of the E-Step, $x_i$ is the private data of the $i^{th}$ party, and $\mu_j$ is the mean of the $j^{th}$ Gaussian component.  
  
For each Gaussian component $j_0$, each party $i$ computes the intermediate updates vector $v^i$ = [ $a_{ij_0}, b_{ij_0}, c_{ij_0}$ ] locally, encrypts it using the Fully Homomorphic Encryption (FHE) scheme CKKS, and sends Enc(v) to the server which then computes the sum of the ve

Potential drawbacks:  
Advantages:  
  
### The Algorithm  
  
### Implementation  
We implemented our algorithm in **Python** using the **TenSEAL** library by OpenMined, which is a convenient Python wrapper around Microsoft SEAL. (https://github.com/OpenMined/TenSEAL.git)  
Data is encrypted under the Fully Homomorphic Encryption (FHE) scheme CKKS, which is a variant of the homomorphic encryption scheme that supports computations on real numbers.  
 
