# Proposed Approach  
  
## Motivation  
All proposed approaches in prior work on PPEM involve a trade-off between accuracy, privacy, and performance.  
For example, Fully Homomorphic Encryption (FHE) based algorithms can be time consuming and computationally heavy as computing over encrypted data
incurs a high computational overhead, however privacy will be maintained as FHE allows for secure computations on encrypted data 
without requiring access to the plaintext.  
Another example is Secure Multi-Party Computation (SMPC) based PPEM: maintaining privacy is a primary goal of SMPC. However, achieving perfect privacy comes
at the cost of computational complexity and performance, and the efficiency of SMPC can be impacted by the number of parties involved in the computation.  
  
  
## Our Contribution  
We propose a protocol for privacy-preserving expectation maximization that attains the desirable properties of FHE 
while simplifying calculations to only require addition operations on encrypted data. 
This approach allows us to achieve a high level of privacy while also improving performance and reducing computational overhead.  
By utilizing the strengths of FHE while streamlining the computation process, 
we are able to strike a balance between accuracy, privacy, and performance in our proposed approach.  
  
  
## Settings  
We address the following scenario:  
- Data is distributed and private: there are $n$ parties, each holding its own private data $x_i$ (a two-dimensional point) and 
we wish to fit a GMM to the full dataset, without revealing the private data of each party.  
- We propose a client-server model, where the cloud service is an untrusted third party and acts as the central server, providing a service to the clients who are the owners of the private data.  
- We assume an Honest-but-Curious adversary and do not consider the Malicious case, thus we can assume that the server (the untrusted third party, the "cloud") is not mailcious.  
- To generate, distribute, and manage cryptographic keys for the CKKS scheme via TenSEAL library, we utilize a Key Management Service (KMS).  
  
  
## Reminder: Distributed Expectation-Maximization for Gaussian Mixture Models  
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


## Our Approach  
It's worth noting that in the distributed version of the Expectation Maximization algorithm, the $\{E-Step}$ can be computed locally. 
This means that each party can perform the E-step on its own data, thus preserving data privacy.  
However, the $\{M-Step}$ requires data aggregation to compute global updates of the Gaussian components' parameters, which raises privacy concerns.  
To address this, we simplify the M-step by breaking it down into intermediate updates that are also computed locally and will periodically be communicated with the central server.  
  
### The Algorithm  
For each iteration $t$, the KMS generates a pair of public and secret keys $(pk_t, sk_t)$ and distributes both keys to all parties involved in the computation. Therefore, each party will hold both the public key $pk_t$ and the corresponding secret key $sk_t$ for the current iteration. Furthermore, the server gets access only to the oublic key $pk_t$.  
  
For every Gaussian component $j$, each node $i$ computes the following intermediate updates:  
$$a_{ij}^t = P(x_i|N_j^t)$$ 
$$b_{ij}^t = P(x_i|N_j^t)x_i$$
$$c_{ij}^t = P(x_i|N_j^t)(x_i - \mu_j^t)(x_i - \mu_j^t)^\top$$  
  
All the above updates can also be computed locally at node $i$, and then the node can compute its intermediate updates vector:  
$$v_{ij}^t=[a_{ij}^t,  b_{ij_{0}}^t, b_{ij_{1}}^t, c_{ij_{00}}^t, c_{ij_{01}}^t, c_{ij_{10}}^t, c_{ij_{11}}^t]$$  

$x_i$ is a two-dimensional point, $a_{ij}$ is a scalar, $b_{ij}$ is a two-dimensional vector, and $c_{ij}$ is a 2x2 matrix. Thus, $v_{ij}^t$ includes all the entries of $a$, $b$, and $c$.  
  
Node $i$ then encrypts this vector and sends the ciphertext $\hat{v_{ij}^t} ← Enc_{pk_t}(v_{ij}^t)$ to the server.  
After receiving these intermediate updates from all nodes, the server computes the sum of all the vectors (for a specific Gaussian component $j$):  
$$\hat{v_{j}^t} ← Eval_{pk_t}(C, \hat{v_{i_{1}j}^t}, ..., \hat{v_{i_{n}j}^t})$$  
where $C$ is a full adder circuit.  
  
The server sends back the result $\hat{s_{ij}^t}$ to all the nodes, and then every node $i$ decrypts it to obtain the sum
${v_{j}^t} ← Dec_{sk_t}(\hat{v_{j}^t)}$ which is $v_j^t=\Sigma_{i=1}^n v_{ij}^t$, 
from which we can obtain the sums $\Sigma_{i=1}^n a_{ij}^t,  \Sigma_{i=1}^n b_{ij}^t,  \Sigma_{i=1}^n c_{ij}^t$.  
  
These sums are used to update the global estimates of the mixture weights and the means and covariances of each Gaussian component (global updates):  

$$\beta_j^{t+1} = \frac{\Sigma_{i=1}^n P(x_i|N_j^t)}{n} = \frac{\Sigma_{i=1}^n a_{ij}^t}{n}$$   
  
$$\mu_j^{t+1} = \frac{\Sigma_{i=1}^n P(x_i|N_j^t) x_i}{\Sigma_{i=1}^n P(x_i|N_j^t)} = \frac{\Sigma_{i=1}^n b_{ij}^t}{\Sigma_{i=1}^n a_{ij}^t}$$  
  
$$\Sigma_j^{t+1} = \frac{\Sigma_{i=1}^n P(x_i|N_j^t) (x_i-μ_j^t) (x_i-μ_j^t)^\top}{\Sigma_{i=1}^n P(x_i|N_j^t)} = \frac{\Sigma_{i=1}^n c_{ij}^t}{\Sigma_{i=1}^n a_{ij}^t}$$  

 
## Results  


  

