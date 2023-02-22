import numpy as np
from scipy import random
from scipy.stats import multivariate_normal
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import matplotlib.transforms as transforms
import tenseal as ts

# we work with 2D points
# attributes of PPEM_for_GMM: 
#   num_of_gaussians, num_of_points, means (size: 2*num_of_gaussians),
#   covariances(size: 2*2*num_of_gaussians), coeffecients(size: num_of_gaussians),
#   data(size: num_of_points*2), colors_of_gaussians(size: num_of_gaussians)
#   a(size: num_of_points*num_of_gaussians), b(size: num_of_points*num_of_gaussians),
#   c(size: num_of_points*num_of_gaussians)

class GaussianMixtureModel:
    """
    param data: 2D points from a mixture of Gaussians
    param num_of_gaussians: number of gaussian clusters
    param num_of_points: total number of points in the dataset
    param colors_of_gaussians: colors of the gaussian clusters for poltting
    param means: means of the Gaussian components
    param covariances: covariances of the Gaussian components
    param coefficients: coefficients of the Gaussian components
    param a: intermediate updates for coefficients - results of the E-Step
    param b: intermediate updates for means
    param c: intermediate updates for covariances
    """
    def __init__(self, data, num_of_gaussians, num_of_points):
        self.data = data
        self.num_of_gaussians = num_of_gaussians
        self.num_of_points = num_of_points
        self.colors_of_gaussians = random.rand(num_of_gaussians, 3)
        self.means = random.rand(num_of_gaussians, 2)*20 - 10
        covariances = np.zeros((num_of_gaussians, 2, 2))
        for i in range(num_of_gaussians):
            covariances[i] = np.eye(2)
        self.covariances = covariances
        self.coefficients = np.ones(num_of_gaussians)/num_of_gaussians
        self.a = np.zeros((num_of_points, num_of_gaussians))
        self.b = np.zeros((num_of_points, num_of_gaussians))
        self.c = np.zeros((num_of_points, num_of_gaussians))

    def e_step(self):
        '''
        Expectation Step (E-Step) of the Expectation Maximization algorithm.
        '''
        for i in range(self.num_of_points):
            for j in range(self.num_of_gaussians):
                self.a[i][j] = self.coefficients[j] * multivariate_normal.pdf(self.data[i], mean=self.means[j], cov=self.covariances[j])
            self.a[i][:] /= self.a[i][:].sum(axis=1, keepdims=True)

    def m_step(self):
        '''
        Maximization Step (M-Step) of the Expectation Maximization algorithm.
        '''

        # E-Step updates the 'a' values (intermediate updates for the Gaussian components' weights)

        # updating the 'b' values (intermediate updates for the Gaussian components' means)
        for i in range(self.num_of_points):
            for j in range(self.num_of_gaussians):
                self.b[i][j] = self.a[i][j] * self.data[i]

        # updating the 'c' values (intermediate updates for the Gaussian components' covariances)
        for i in range(self.num_of_points):
            for j in range(self.num_of_gaussians):
                self.b[i][j] = self.a[i][j] * (self.data[i] - self.means[j]) * np.transpose(self.data[i] - self.means[j])

        # Setup TenSEAL context
        context = ts.context(
            ts.SCHEME_TYPE.CKKS,
            poly_modulus_degree=8192,
            coeff_mod_bit_sizes=[60, 40, 40, 60]
        )
        context.generate_galois_keys()
        context.global_scale = 2 ** 40

        # for each Gaussian component, each party i sends its corresponding [a_ij, b_ij, c_ij] encrypted
        # to the untrusted third party, then the TP computes the encrypted sums a_j, b_j, c_j
        # the results are then decrypted and the global updates are performed.

        for j in range(self.num_of_gaussians):
            enc_sum_abc = ts.ckks_vector(context, [0, 0, 0])
            for i in range(self.num_of_points):
                abc_ij = [self.a[i][j], self.b[i][j], self.c[i][j]]     # [a_ij, b_ij, c_ij]
                enc_ij = ts.ckks_vector(context, abc_ij)        # [a_ij, b_ij, c_ij] encrypted
                enc_sum_abc = enc_sum_abc + enc_ij
            # enc_sum_abc is now [a_j, b_j, c_j] encrypted
            sum_abc = enc_sum_abc.decrypt()         # [a_j, b_j, c_j]
            # global updates
            self.coefficients[j] = sum_abc[0] / self.num_of_points     # beta_j = a_j/n
            self.means[j] = sum_abc[1] / sum_abc[0]     # mu_j = b_j/a_j
            self.covariances[j] = sum_abc[2] / sum_abc[0]       # Sigma_j = c_j/a_j



            # enc_aj = ts.ckks_vector(context, self.a[:, j]).sum()
            # enc_bj = ts.ckks_vector(context, self.b[:, j]).sum()
            # enc_cj = ts.ckks_vector(context, self.c[:, j]).sum()
            # a_j = enc_aj.decrypt()
            # b_j = enc_bj.decrypt()
            # c_j = enc_cj.decrypt()
            #
            # self.coefficients[j] = a_j / self.num_of_points
            # self.means[j] = b_j / a_j
            # self.covariances[j] = c_j / a_j

    def log_likelihood(self):
        
