import tenseal as ts
import numpy as np
from scipy.stats import multivariate_normal


class Client:
    """
    This class represents a single party (a client) that holds a data point belonging to a Gaussian Mixture Model (GMM).
    The data point is represented as a two-dimensional point.

    Attributes:
    -----------
    data:
        The two-dimensional data point.

    num_of_gaussians:
        Number of gaussian components.

    context: TenSEALContext
        The parameters of the CKKS scheme in TenSEAL.

    a:
        The intermediate updates for the coefficients of the GMM. size: num_of_gaussians.

    b:
        The intermediate updates for the means of the GMM. size: (num_of_gaussians, 2).

    c:
        The intermediate updates for the covariances of the GMM. size: (num_of_gaussians, 2, 2).
    """

    def __init__(self, data, num_of_gaussians):
        self.data = data
        self.num_of_gaussians = num_of_gaussians
        self.context = None
        # for intermediate updates
        self.a = np.zeros(num_of_gaussians)
        self.b = np.zeros((num_of_gaussians, 2))
        self.c = np.zeros((num_of_gaussians, 2, 2))

    def e_step(self, gmm):
        """Performs the E-Step of the EM algorithm. Computes the conditional probabilities that the client's data belongs to each Gaussian model."""
        self.a[:] = [gmm.coefficients[j] * multivariate_normal.pdf(self.data, mean=gmm.means[j], cov=gmm.covariances[j])
                     for j in range(self.num_of_gaussians)]
        self.a[:] /= self.a[:].sum()

    def inter_m_step(self, j, gmm, context):
        """Performs the intermediate M-Step calcultaions of the EM algorithm. Computes the local updates for the coefficients, means, and covariances of the GMM."""
        a_j = self.a[j]
        b_j_0 = self.a[j] * self.data[0]
        b_j_1 = self.a[j] * self.data[1]
        c_j_00 = self.a[j] * (self.data[0] - gmm.means[j][0]) ** 2
        c_j_01 = self.a[j] * (self.data[0] - gmm.means[j][0]) * (self.data[1] - gmm.means[j][1])
        c_j_10 = self.a[j] * (self.data[1] - gmm.means[j][1]) * (self.data[0] - gmm.means[j][0])
        c_j_11 = self.a[j] * (self.data[1] - gmm.means[j][1]) ** 2

        v_j = [a_j, b_j_0, b_j_1, c_j_00, c_j_01, c_j_10, c_j_11]
        enc_v_j = self.encrypt(v_j, context)
        return enc_v_j

    def encrypt(self, vec, context):
        """Encrypt a vector using the CKKS scheme in TenSEAL."""
        return ts.ckks_vector(context, vec)

    def decrypt(self, vec):
        """Decrypt a CKKSVector using the CKKS scheme in TenSEAL."""
        return vec.decrypt()