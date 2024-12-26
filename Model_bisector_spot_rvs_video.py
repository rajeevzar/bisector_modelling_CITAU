#!/usr/bin/env python
# coding: utf-8

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from astropy.timeseries import LombScargle
from random import random
from scipy import stats

BIS_obs, RV_obs, RV_obs_err = np.loadtxt('CITAU_Bis_ccf_Eder_All_15.txt', usecols=(3, 4, 5), skiprows=1, unpack = True)

BIS_obs_err = RV_obs_err

# BIS_obs, RV_obs = np.loadtxt('eder_bis_rv.dat', usecols=(0, 2), skiprows=1, unpack = True)
# BIS_obs = - (BIS_obs - np.mean(BIS_obs))

# Define the two Gaussian distributions
mean_spot = 16.39 # mean RV of starspot 
mean_planet = 16.39 # mean RV of Planet 

# RV_obs = RV_obs + mean_planet

stddev_spot = 0.4 #0.4
stddev_planet = 0.9 #0.9
amplitude_spot = 0.25 #0.25
amplitude_planet = 0.9 #0.9

# gaussian1 = norm(mean1, stddev1)
BIS_list = []
miny_list = []
BIS_list_err = []
rverr = []

amplitude_motion_planet = 0.0 #0.0, 0.55, 0.775, 1.1
frequency_motion_planet = 0.042 # 24 days

amplitude_motion_spot = 0.9 #0.9
frequency_motion_spot= 0.11  #9 days
# Add the two Gaussians together in sequence
# fig, ax = plt.subplots(num=None, figsize=(10,5), dpi=120, facecolor='w', edgecolor='k')
x = np.linspace(0, 100, 10000)


for i in range(100):
    gaussian_planet = norm(mean_planet + amplitude_motion_planet * np.sin(2 * np.pi * frequency_motion_planet * i), stddev_planet) # for circular motion of planet
    gaussian_spot = norm(mean_spot + amplitude_motion_spot * np.sin(2 * np.pi * frequency_motion_spot * i), stddev_spot)
    y_spot = amplitude_spot * gaussian_spot.pdf(x)
    y_planet = amplitude_planet * gaussian_planet.pdf(x)
    
    y = -1.0 * (y_spot + y_planet) + 1.0

    # Update fig1
    plt.plot(x, -1.0 * y_spot + 1, 'b', alpha=0.5, label='spot')
    plt.plot(x, -1.0 * y_planet + 1, 'r', alpha=0.5, label='planet')
    plt.plot(x, y,label='total signal', color='k', alpha=0.9)
    plt.xlabel('RV (km/s)', fontsize=16)
    plt.ylabel('Norm. CCF (flux units)', fontsize=16)
    plt.tick_params(axis='both', which='major', labelsize=14)
    plt.xlim(12, 21)
    plt.ylim(0.3,1.1)

    peak_index = np.argmin(y)
    peak_x = x[peak_index]
    miny_list.append(peak_x)
    depth = max(y) - min(y)

    # Find the values that correspond to the top and bottom 20 percentiles
    top_cutoffup = max(y) - 0.05 * depth #0.2
    top_cutoffdown = max(y) - 0.15 * depth #0.3
    bottom_cutoffup = max(y) - 0.85 * depth #0.7
    bottom_cutoffdown = max(y) - 0.95 * depth #0.8

    # Create masks for the top and bottom 20 percentiles
    top_mask = (y > top_cutoffdown) & (y < top_cutoffup)
    bottom_mask = (y > bottom_cutoffdown) & (y < bottom_cutoffup)

    # Calculate the mean of the x and y values for the top and bottom percentiles
    peak_index = np.argmin(y)
    x_top_left_mask = (x < x[peak_index]) & (y > top_cutoffdown) & (y < top_cutoffup)
    x_top_right_mask = (x > x[peak_index]) & (y > top_cutoffdown) & (y < top_cutoffup)
    top_xmean_left = np.nanmean(x[x_top_left_mask])
    top_xmean_right = np.nanmean(x[x_top_right_mask])
    top_ymean_left = np.nanmean(y[x_top_left_mask])
    top_ymean_right = np.nanmean(y[x_top_right_mask])

    x_bottom_left_mask = (x < x[peak_index]) & (y > bottom_cutoffdown) & (y < bottom_cutoffup)
    x_bottom_right_mask = (x > x[peak_index]) & (y > bottom_cutoffdown) & (y < bottom_cutoffup)
    bottom_xmean_left = np.nanmean(x[x_bottom_left_mask])
    bottom_xmean_right = np.nanmean(x[x_bottom_right_mask])
    bottom_ymean_left = np.nanmean(y[x_bottom_left_mask])
    bottom_ymean_right = np.nanmean(y[x_bottom_right_mask])
    
    bisector_up = (top_xmean_left + top_xmean_right) / 2.
    err_bis_up = (np.nanstd(x[x_top_left_mask]) + np.nanstd(x[x_top_right_mask]))/2.
    bisector_bottom = (bottom_xmean_left + bottom_xmean_right) / 2.
    err_bis_down = (np.nanstd(x[x_bottom_left_mask]) + np.nanstd(y[x_bottom_right_mask]))/ 2.
    
    BIS = bisector_up - bisector_bottom
    BIS_list.append(BIS + BIS*random()) #+ BIS*0*random()
    BIS_err = np.sqrt(err_bis_up **2. + err_bis_down **2.)
    BIS_list_err.append(BIS_err)
   
    top_ymean = (top_ymean_left + top_ymean_right)/2.
    bottom_ymean = (bottom_ymean_left + bottom_ymean_right)/2.
#     
#     plt.plot(bisector_bottom, bottom_ymean, 'go')
#     plt.plot(bisector_up, top_ymean, 'go')
#     
# #     fig2 = plt.figure()
# #     plt.scatter(peak_x, BIS + BIS*random(), marker='o')
# #     plt.xlim(15, 18)
# #     plt.ylim(-1.5, 1.5)
    if i < 10:
     plt.savefig("00%d.png" % i)
    else:
     plt.savefig("0%d.png" % i)
    plt.show()
    




# plt.legend()
################## MODEL BISECTOR PLOT ########################
# fig, ax = plt.subplots(num=None, figsize=(10,5), dpi=120, facecolor='w', edgecolor='k')
# 
# plt.scatter(miny_list, BIS_list, marker='o')
# plt.xlabel('RV (km/s)', fontsize=16)
# plt.ylabel('BIS Span (km/s)', fontsize=16)
# # plt.ylim(-2.5, 3)
# # plt.xlim(15,18)
# ax.tick_params(axis='both', which='major', labelsize=14)
# 
# plt.show()






