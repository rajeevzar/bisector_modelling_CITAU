import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from random import random

class BisectorModel:
    def __init__(self, data_file, output_dir="output/"):
        self.data_file = data_file
        self.output_dir = output_dir
        self.x = np.linspace(0, 100, 10000)
        self.BIS_list = []
        self.miny_list = []
        self.BIS_list_err = []

        # Gaussian parameters
        self.mean_spot = 16.39
        self.mean_planet = 16.39
        self.stddev_spot = 0.4
        self.stddev_planet = 0.9
        self.amplitude_spot = 0.25
        self.amplitude_planet = 0.9

        # Motion parameters
        self.amplitude_motion_planet = 0.0
        self.frequency_motion_planet = 0.042  # 24 days
        self.amplitude_motion_spot = 0.9
        self.frequency_motion_spot = 0.11  # 9 days

    def load_data(self):
        self.BIS_obs, self.RV_obs, self.RV_obs_err = np.loadtxt(
            self.data_file, usecols=(3, 4, 5), skiprows=1, unpack=True
        )
        self.BIS_obs_err = self.RV_obs_err

    def calculate_gaussians(self, i):
        planet_shift = self.mean_planet + self.amplitude_motion_planet * np.sin(2 * np.pi * self.frequency_motion_planet * i)
        spot_shift = self.mean_spot + self.amplitude_motion_spot * np.sin(2 * np.pi * self.frequency_motion_spot * i)

        gaussian_planet = norm(planet_shift, self.stddev_planet)
        gaussian_spot = norm(spot_shift, self.stddev_spot)

        y_spot = self.amplitude_spot * gaussian_spot.pdf(self.x)
        y_planet = self.amplitude_planet * gaussian_planet.pdf(self.x)
        total_signal = -1.0 * (y_spot + y_planet) + 1.0

        return y_spot, y_planet, total_signal

    def calculate_bisector(self, y):
        peak_index = np.argmin(y)
        depth = max(y) - min(y)

        top_cutoffup = max(y) - 0.05 * depth
        top_cutoffdown = max(y) - 0.15 * depth
        bottom_cutoffup = max(y) - 0.85 * depth
        bottom_cutoffdown = max(y) - 0.95 * depth

        top_mask = (y > top_cutoffdown) & (y < top_cutoffup)
        bottom_mask = (y > bottom_cutoffdown) & (y < bottom_cutoffup)

        x_top_left_mask = (self.x < self.x[peak_index]) & top_mask
        x_top_right_mask = (self.x > self.x[peak_index]) & top_mask
        x_bottom_left_mask = (self.x < self.x[peak_index]) & bottom_mask
        x_bottom_right_mask = (self.x > self.x[peak_index]) & bottom_mask

        top_xmean_left = np.nanmean(self.x[x_top_left_mask])
        top_xmean_right = np.nanmean(self.x[x_top_right_mask])
        bottom_xmean_left = np.nanmean(self.x[x_bottom_left_mask])
        bottom_xmean_right = np.nanmean(self.x[x_bottom_right_mask])

        bisector_up = (top_xmean_left + top_xmean_right) / 2.0
        bisector_bottom = (bottom_xmean_left + bottom_xmean_right) / 2.0
        BIS = bisector_up - bisector_bottom

        self.BIS_list.append(BIS + BIS * random())

    def plot_iteration(self, i, y_spot, y_planet, total_signal):
        plt.plot(self.x, -1.0 * y_spot + 1, 'b', alpha=0.5, label='Spot')
        plt.plot(self.x, -1.0 * y_planet + 1, 'r', alpha=0.5, label='Planet')
        plt.plot(self.x, total_signal, 'k', alpha=0.9, label='Total Signal')
        plt.xlabel('RV (km/s)', fontsize=16)
        plt.ylabel('Norm. CCF (flux units)', fontsize=16)
        plt.xlim(12, 21)
        plt.ylim(0.3, 1.1)

        plt.legend()
        if i < 10:
            filename = f"{self.output_dir}00{i}.png"
        else:
            filename = f"{self.output_dir}0{i}.png"
        plt.savefig(filename)
        plt.close()

    def run_simulation(self, iterations=100):
        for i in range(iterations):
            y_spot, y_planet, total_signal = self.calculate_gaussians(i)
            self.calculate_bisector(total_signal)
            self.plot_iteration(i, y_spot, y_planet, total_signal)
