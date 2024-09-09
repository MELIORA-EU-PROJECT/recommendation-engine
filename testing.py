import random
import numpy as np
import matplotlib.pyplot as plt

# # inverse lognormal distribution from 1 to 5
# distribution = np.random.lognormal(3.6, 0.6, 1000)
# distribution = np.clip(distribution, 0, 100)
# # plt.hist(distribution, bins=100)
# distribution = -distribution
# distribution = distribution + 100
# distribution = np.round(distribution)
# distribution = distribution / (100 / 5)
# distribution = distribution.astype(int)
#
# plt.hist(distribution, bins=100)
# plt.legend(["Lognormal Distribution", "Inverse Lognormal Distribution"])
# plt.show()

distribution = np.random.normal(3, 1.4, 1000)
distribution = np.round(distribution)
distribution = np.clip(distribution, 0, 6)
distribution = distribution.astype(int)
plt.hist(distribution, bins=100)
plt.show()