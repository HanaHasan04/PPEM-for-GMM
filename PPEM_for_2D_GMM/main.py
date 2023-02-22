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
    def __init__(self, data, num_of_gaussians, num_of_points, ):
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
        





