import numpy as np
from numpy import random
import matplotlib.pyplot as plt
from GMM import *
from Client import *


def gen_data(num_of_gaussians=3, points_per_gaussian=200, mean_range=[-10, 10]):
  """
  Generates 2D points from a mixture of Gaussians.

  Args:
  - num_of_gaussians: Number of Gaussian components
  - points_per_gaussian: Number of points in each Gaussian component
  - mean_range: Range of mean values

  Returns:
  2D points data: Generated 2D points from a mixture of Gaussians
  num_of_points: Number of the generated points = Number of Gaussians * Number of points in each component
  """
  x = []
  mean = random.rand(num_of_gaussians, 2)*(mean_range[1]-mean_range[0]) + mean_range[0]
  for i in range(num_of_gaussians):
      cov = random.rand(2, 12)
      cov = np.matmul(cov, cov.T)
      _x = np.random.multivariate_normal(mean[i], cov, points_per_gaussian)
      x += list(_x)
  x = np.array(x)
  fig = plt.figure()
  ax = fig.gca()
  ax.scatter(x[:,0], x[:,1], s=3, alpha=0.4)
  ax.autoscale(enable=True)
  tot_points = num_of_gaussians*points_per_gaussian
  return x, tot_points

def plot(title):
    """Draw the data points and the fitted mixture model."""
    fig = plt.figure(figsize=(8, 8))
    ax = fig.gca()
    ax.scatter(X[:, 0], X[:, 1], s=3, alpha=0.4)
    ax.scatter(gmm.means[:, 0], gmm.means[:, 1], c=gmm.colors_of_gaussians)
    gmm.draw(ax, lw=3)
    ax.set_xlim((-12, 12))
    ax.set_ylim((-12, 12))
    plt.title(title)
    plt.show()
    plt.clf()


if __name__ == '__main__':
    NUM_OF_CLUSTERS = 3
    POINTS_PER_CLUSTER = 1000
    X, NUM_OF_POINTS = gen_data(num_of_gaussians=NUM_OF_CLUSTERS, points_per_gaussian=POINTS_PER_CLUSTER)

    clients = []
    for i in range(NUM_OF_POINTS):
        clt = Client(data=X[i], num_of_gaussians=NUM_OF_CLUSTERS)
        clients.append(clt)

    gmm = GMM(parties=clients, num_of_parties=NUM_OF_POINTS, num_of_gaussians=NUM_OF_CLUSTERS)

    NUM_OF_ITERATIONS = 40
    # plotting the points alongside the Gaussian components
    plot("Step 0")
    for e in range(NUM_OF_ITERATIONS):
        gmm.e_step()
        gmm.m_step()
        plot(title="Step " + str(e + 1))
