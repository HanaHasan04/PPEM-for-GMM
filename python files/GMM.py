from KMS import *
from Server import *
import numpy as np
from numpy import random
from matplotlib.patches import Ellipse
import matplotlib.transforms as transforms


class GMM:
    """
    This class represents a Gaussian Mixture Model (GMM). We wish to fit a GMM to the full dataset of all parties.

    Attributes:
    -----------
    parties:
        The parties (clients) that the data is distributed among them.

    num_of_parties:
        Number of parties (which is the number of data points).

    server: Server
        The server (untrusted third party) to perform computations on the encrypted data.

    kms: KMS
        The key management system that is used to generate, distribute, and manage cryptographic keys.

    num_of_gaussians:
        Number of gaussian components.

    colors_of_gaussians:
        Colors of the gaussian clusters for poltting. size: (num_of_gaussians, 3).

    means:
        The means of the Gaussian components. size: (num_of_gaussians, 2).

    covariances:
        The covariances of the Gaussian components. size: (num_of_gaussians, 2, 2).

    coefficients:
        The coefficients of the Gaussian components. size: num_of_gaussians.
    """

    def __init__(self, parties, num_of_parties, num_of_gaussians):
        self.parties = parties
        self.num_of_parties = num_of_parties
        self.server = Server(num_of_parties)
        self.kms = KMS(parties, poly_modulus_degree=8192, coeff_mod_bit_sizes=[60, 40, 40, 60], global_scale=2 ** 40)
        self.num_of_gaussians = num_of_gaussians
        self.colors_of_gaussians = random.rand(num_of_gaussians, 3)
        # parameters estimates
        self.means = random.rand(num_of_gaussians, 2) * 20 - 10  # initial means: random from uniform[-10, 10]
        covariances = np.zeros((num_of_gaussians, 2, 2))
        for j in range(num_of_gaussians):
            covariances[j] = np.eye(2)
        self.covariances = covariances
        self.coefficients = np.ones(num_of_gaussians) / num_of_gaussians

    def e_step(self):
        """E-step of EM algorithm."""
        for party in self.parties:
            party.e_step(self)

    def m_step(self):
        """M-step of EM algorithm."""
        self.kms.gen_context()
        # self.kms.dist_context()

        for j in range(self.num_of_gaussians):
            for party in self.parties:
                enc_v_ij = party.inter_m_step(j, self, self.kms.context)
                self.server.add_vec(enc_v_ij)

            enc_sum_j = self.server.calc_sum()
            self.server.clear_server()

            sum_j = self.parties[random.randint(0, self.num_of_parties - 1)].decrypt(enc_sum_j)
            a_j = sum_j[0]
            b_j_0 = sum_j[1]
            b_j_1 = sum_j[2]
            c_j_00 = sum_j[3]
            c_j_01 = sum_j[4]
            c_j_10 = sum_j[5]
            c_j_11 = sum_j[6]
            self.coefficients[j] = a_j / self.num_of_parties
            self.means[j][0] = b_j_0 / a_j
            self.means[j][1] = b_j_1 / a_j
            self.covariances[j][0][0] = c_j_00 / a_j
            self.covariances[j][0][1] = c_j_01 / a_j
            self.covariances[j][1][0] = c_j_10 / a_j
            self.covariances[j][1][1] = c_j_11 / a_j

    def plot_gaussian(self, mean, cov, ax, n_std=3.0, facecolor='none', **kwargs):
        """Utility function to plot one Gaussian from mean and covariance."""
        pearson = cov[0, 1] / np.sqrt(cov[0, 0] * cov[1, 1])
        ell_radius_x = np.sqrt(1 + pearson)
        ell_radius_y = np.sqrt(1 - pearson)
        ellipse = Ellipse((0, 0), width=ell_radius_x * 2, height=ell_radius_y * 2, facecolor=facecolor, **kwargs)
        scale_x = np.sqrt(cov[0, 0]) * n_std
        mean_x = mean[0]
        scale_y = np.sqrt(cov[1, 1]) * n_std
        mean_y = mean[1]
        transf = transforms.Affine2D().rotate_deg(45).scale(scale_x, scale_y).translate(mean_x, mean_y)
        ellipse.set_transform(transf + ax.transData)
        return ax.add_patch(ellipse)

    def draw(self, ax, n_std=2.0, facecolor='none', **kwargs):
        """Function to draw the Gaussians."""
        for j in range(self.num_of_gaussians):
            self.plot_gaussian(self.means[j], self.covariances[j], ax, n_std=n_std,
                               edgecolor=self.colors_of_gaussians[j], **kwargs)