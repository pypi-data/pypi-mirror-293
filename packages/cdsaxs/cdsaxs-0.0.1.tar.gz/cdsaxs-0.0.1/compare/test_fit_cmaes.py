from fit import cmaes
import numpy as np
import os
import time
import matplotlib.pyplot as plt

# Define the path and load data from a file
path = '../data'
qxs = np.loadtxt(os.path.join(path, 'qx_exp.txt'))
qzs = np.loadtxt(os.path.join(path, 'qz_exp.txt'))
data = np.loadtxt(os.path.join(path, 'i_exp.txt'))

# Define initial parameters and multiples
dwx = 0.1
dwz = 0.1
i0 = 0.203
bkg = 0.1
height = 23.48
bot_cd = 54.6
swa = [78, 90, 88, 84, 88, 85]

initial_guess = np.array([dwx, dwz, i0, bkg, height, bot_cd] + swa)
multiples = [1E-8, 1E-8, 1E-8, 1E-7, 1E-7, 1E-7] + len(swa) * [1E-5]

# Check if the number of initial guesses matches the number of multiples
assert len(initial_guess) == len(multiples), f'Number of adds ({len(initial_guess)}) is different from number of multiples ({len(multiples)})'

# Define data arrays
data = data
qxs = qxs
qzs = qzs

# Define a range of population sizes
nbpop = np.arange(10, 700, 50)
# nbpop = [10, 11]

# Initialize lists to store execution times
timeNP = []  # For non-parallel execution

    # Iterate through different population sizes
for i in nbpop:
    # Non-parallel execution
    start = time.time()
    best_corr, best_fitness = cmaes(data=data, qxs=qxs, qzs=qzs, sigma=100, ngen=30, popsize=i, mu=10,
                                        n_default=len(initial_guess), restarts=0, verbose=False, tolhistfun=5e-5,
                                        initial_guess=initial_guess, ftarget=None, dir_save=None)
    end = time.time()
    timeNP.append(end - start)

np.savetxt('time.txt', timeNP)  # Save the execution times for parallel execution

# Create a plot to compare execution times
plt.plot(nbpop, timeNP, label='Non-Parallel')
plt.xlabel('Number of population')
plt.ylabel('Time (s)')
plt.legend()
plt.savefig('time.png')  # Save the plot as an image
plt.show()  # Display the plot
