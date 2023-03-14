# Background
Welcome to our project's background materials!  
This document serves as our preliminaries and problem setup, where we will introduce and explain the key concepts of Gaussian mixture models, 
the expectation maximization algorithm, and fully homomorphic encryption.


   
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
Consider the scenario where $n$ parties each has its own data $x_i$ and these parties would like to collaborate to learn a GMM based on the full dataset { $x_1, x_2, ..., x_n$ }.  
Assuming there are $c$ Gaussian components, the GMM density is given by:  
$$p(x)=\Sigma_{j=1}^c \beta_j p(x| \mu_j, \Sigma_j)$$ 
where $\beta_j$ is the mixing coefficient of the $j^{th}$ Gaussian component, and $\mu_j$ and $\Sigma_j$ are the mean and covariance, respectively, of the $j^{th}$ Gaussian component.  
  
  
**The EM algorithm is iterative and for each iteration $t$, the following steps are taken for all Gaussian components:**  
  
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
     
## Fully Homomorphic Encryption (FHE) and the CKKS scheme  
**Acknowledgement**:  
Our project uses the TenSEAL library, which is an open-source library for homomorphic encryption in Python. We thank the developers of TenSEAL for providing this resource, which has been instrumental in achieving our project goals.  
The images used in this section are from the TenSEAL tutorials!  
  
### Fully Homomorphic Encryption (FHE)
**Definition**: Fully Homomorphic Encryption (FHE) is an encryption technique that allows computations to be made on ciphertexts and generates results that when decrypted, correspond to the results of the same computations made on plaintexts.  
  
In practice, for an application that needs to perform some computation F on data that is encrypted, the FHE scheme would provide some alternative computation F' which when applied directly over the encrypted data will result in the encryption of the application of F over the data in the clear. More formally: F(unencrypted_data) = Decrypt(F'(encrypted_data)).  
  
 <img src="https://user-images.githubusercontent.com/100927079/225030946-c4f2add6-833b-4624-9183-59b8b57a67cb.png" alt="Alt text" style="width:370px;height:400px;">   
  
Formally, an FHE scheme is a tuple of four algorithms $(Gen, Enc, Dec, Eval)$ that satisfy the following properties:  
- **Gen**: The key generation algorithm takes a security parameter k as input and outputs a public key pk and a secret key sk.  
- **Enc**: The encryption algorithm takes a public key pk and a message m as input and outputs a ciphertext c.  
- **Dec**: The decryption algorithm takes a secret key sk and a ciphertext c as input and outputs the original message m.  
- **Eval**: The evaluation algorithm takes a function f and a set of ciphertexts { $c_1, c_2, ..., c_n$ } as input and outputs a new ciphertext $c_f$ that represents the result of applying the function f to the plaintexts corresponding to the input ciphertexts.

For an FHE scheme to be fully homomorphic, the Eval algorithm must satisfy two additional properties:  
- **Correctness**: For any function f and any set of ciphertexts { $c_1, c_2, ..., c_n$ } corresponding to plaintexts { $m_1, m_2, ..., m_n$ }, the ciphertext $c_f$ output by $Eval(pk, f, {c_1, c_2, ..., c_n})$ must decrypt to the correct result $f(m_1, m_2, ..., m_n)$.  
- **Security**: The scheme must provide a level of security that makes it infeasible for an attacker to learn any information about the plaintexts from the ciphertexts or the public key. 
   
 ### CKKS scheme
**Definition**: Cheon-Kim-Kim-Song(CKKS) is a scheme for Leveled Homomorphic Encryption that supports approximate arithmetics over complex numbers (hence, real numbers).  
![image](https://user-images.githubusercontent.com/100927079/225034137-7208f005-25a6-4396-965a-43b2954afd97.png)  
  
 **CKKS keys**:  
- **The secret key**: The secret key is used for decryption. DO NOT SHARE IT.  
- **The public encryption key**: The key is used for encryption in the public key encryption setup.
- **The relinearization keys**: Every new ciphertext has a size of 2, and multiplying ciphertexts of sizes $K$ and $L$ 
results in a ciphertext of size $K+L-1$. Unfortunately, this growth in size slows down further multiplications and increases noise growth.  
Relinearization is the operation that reduces the size of ciphertexts back to 2. This operation requires another type of public keys, the relinearization keys created by the secret key owner.  
The operation is needed for encrypted multiplications. The plain multiplication is fundamentally different from normal multiplication and does not result in ciphertext size growth.  
- **The Galois Keys(optional)**:
Galois keys are another type of public keys needed to perform encrypted vector rotation operations on batched ciphertexts. One use case for vector rotations is summing the batched vector that is encrypted.  
  
### Adversary Models  
Adversary models are used to describe the capabilities and goals of attackers who may attempt to compromise the security of the system, such as:  
- **Semi-Honest ("honest, but curious")**: All parties follow protocol instructions, but dishonest parties may be curious to violate privacy of others when possible.  
- **Fully Malicious Model**: Adversarial Parties may deviate from the protocol arbitrarily (quit unexpectedly, send different messages etc). It is much harder to achieve security in the fully malicious model.  

