import random
import numpy as np

def normal_distribution (x, mu, sigma) :
    d = x.shape[0]
    x_m = x - mu
    return (1 / (np.sqrt ((2 * np.pi)**d * np.linalg.det (sigma))) * np.exp (- (np.linalg.solve (sigma, x_m).T.dot (x_m)) / 2))

def calc_posterior_prob (pp, means, sigma, data, index) :
    total = 0
    for i in range (pp.shape[0]) :
        total += normal_distribution (data, means[i], sigma[i])
    return normal_distribution (data, means[index], sigma[index]) / total

def expected_maximization (data, k, epsilon=1e-2) :
    if len (data) == 0 :
        return None

    data = np.array (data)

    dim = data.shape[1]
    n = data.shape[0]

    means = np.array ([[random.random() for _ in range (dim)] for _ in range (k)])
    sigma = np.array ([np.eye(dim) for _ in range (k)])
    prior_probability = np.array ([(1/k) for _ in range (k)])

    while (True) :
        total_change = 0
        w = np.zeros ((k, n))
        for i in range (k) :
            for j in range (n) :
                w[i][j] = calc_posterior_prob (prior_probability, means, sigma, data[j], i)

        for i in range (k) :
            mean = [0] * dim
            s = np.zeros ((dim, dim))
            w_total = 0

            for j in range (n) :
                mean += w[i][j] * data[j]
                w_total += w[i][j]
                s += w[i][j] * np.matmul (np.expand_dims (data[j] - means[i], -1), np.expand_dims (data[j] - means[i], -1).T)
            
            total_change += np.mean (np.abs (means[i] - (mean / w_total)))
            means[i] = mean / w_total
            sigma[i] = s / w_total
            prior_probability[i] = w_total / n

        if total_change < epsilon : 
            return means, sigma, prior_probability

def expected_maximization_function (means, sigma, pp, x) :
    x = np.array (x)
    k = len (means)

    f_x = 0
    for i in range (k) :
        f_x += pp[i] * normal_distribution (x, means[i], sigma[i])

    return f_x