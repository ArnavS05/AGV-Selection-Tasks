import numpy as np

from utils import minimized_angle

from soccer_field import Field


class ExtendedKalmanFilter:
    def __init__(self, mean, cov, alphas, beta):
        self.alphas = alphas
        self.beta = beta

        self._init_mean = mean
        self._init_cov = cov
        self.reset()

    def reset(self):
        self.mu = self._init_mean
        self.sigma = self._init_cov

    def update(self, env, u, z, marker_id):
        """Update the state estimate after taking an action and receiving a landmark
        observation.

        u: action
        z: landmark observation
        marker_id: landmark ID
        """
        # YOUR IMPLEMENTATION HERE
        # Using the linear taylor approximation of the update function

        # Getting Jacobians
        G = env.G(self.mu, u)      #If g(u_t, x_t-1) gives the initially planed path (green line), the G = dg/d(state_t-1)
        V = env.V(self.mu, u)      #If g(u_t, x_t-1) gives the initially planed path (green line), the G = dg/du

        # Extracting values from u (controls)
        delta_rot1 = minimized_angle(u[0][0])
        delta_trans = u[1][0]
        delta_rot2 = minimized_angle(u[2][0])

        # Extracting values from self.mu (previous state)
        x = self.mu[0][0]
        y = self.mu[1][0]
        theta = minimized_angle(self.mu[2][0])

        # Predicting the belief of the new state before measurement
        xt = x + delta_trans * np.cos(theta + delta_rot1)
        yt = y + delta_trans * np.sin(theta + delta_rot1)
        theta_t = minimized_angle(theta + delta_rot1 + delta_rot2)
        mu_temp = np.array([[xt],[yt],[theta_t]])        #3x1

        # Finding the covariance matrix using the given alpha. (Ignoring the value of alphas[3])
        # Using this Q instead of the given function in soccer_field because this was giving lesser errors.
        Q = np.diag(env.alphas[0:3])        #3x3
        
        sigma_temp = np.dot(np.dot(G, self.sigma), G.T) + np.dot(np.dot(V, Q), V.T)

        # If h(mu_temp) is the measurement function, then H is dh/d(mu_pred)
        # Since measurement is taken after the movement related to time t, thus, finding H as a function of belief of the new state before measurement
        H = env.H(mu_temp, marker_id)
        
        # K = Kalman Gain   (3x1)
        K = np.dot(np.dot(sigma_temp, H.T), np.linalg.inv(np.dot(np.dot(H, sigma_temp), H.T) + env.beta))

        # Calculating h(mu_temp)
        dx = env.MARKER_X_POS[marker_id]-mu_temp[0][0]
        dy = env.MARKER_Y_POS[marker_id]-mu_temp[1][0]
        h = minimized_angle(np.arctan2(dy, dx) - mu_temp[2][0])

        #Finall updating mu and sigma for the new time state.
        self.mu = mu_temp + K*(minimized_angle(z[0]-h))
        self.sigma = np.dot((np.eye(3) - np.dot(K, H)), sigma_temp)

        return self.mu, self.sigma
