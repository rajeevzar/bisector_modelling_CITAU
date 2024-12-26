# Bisector Analysis for Exoplanet Detection

This repository contains a Python code designed to model and analyze the bisector behavior of cross-correlation functions (CCFs) observed in stellar systems. The code is specifically used to investigate the relationship between bisector span and radial velocity (RV) to demonstrate the presence of an orbiting companion. The analysis supports the detection of a planet with a ~25-day orbital period and 3.6 Jupiter masses (see Manick et al., 2024).

## Overview

The primary goal of the code is to show that a Doppler shift is required to reproduce the observed bisector-RV plane, confirming the influence of an orbiting planet. The simulation models the combined effects of a star’s surface hot spot and a planet on the observed CCF profile.

## Features

1. **Input Data**
   - Reads bisector and RV observational data from a text file (`CITAU_Bis_ccf_Eder_All_15.txt`) for the star CI Tau.

2. **Gaussian Modeling**
   - Two Gaussian profiles simulate the system:
     - **Hot Spot (Blue Gaussian):** Represents a spot on the star's surface.
     - **Star Profile (Red Gaussian):** Models the star's overall line profile.
   - The combined profile (Black line) reproduces the total observed signal.

3. **Doppler Shift Simulation**
   - Introduces sinusoidal variations in RV values to simulate the motions of the hot spot and the planet.

4. **Bisector Calculation**
   - Computes bisector spans by identifying percentile points along the combined profile’s depth.
   - Calculates top and bottom bisector values and their difference (span).

5. **Visualization**
   - Plots the profiles for each simulation step and saves them as images.
   - Generates a video to visualize the evolution of the bisector behavior over time.

6. **Output**
   - Produces bisector vs. RV plots to compare observed data with the modeled results.
   - Confirms that observed bisector variations are induced by an orbiting companion.

## Files
- **`CITAU_Bis_ccf_Eder_All_15.txt`:** Input file containing observational data.
- **Python Script:** Code for modeling and analyzing bisector spans.
- **Generated Images:** Saved at each simulation step for creating a video.

## Dependencies
- `numpy`
- `matplotlib`
- `scipy`
- `astropy`

## How to Run
1. Clone the repository and ensure all dependencies are installed.
2. Place the input file (`CITAU_Bis_ccf_Eder_All_15.txt`) in the working directory.
3. Run the Python script.
4. View the generated plots and images in the output folder.
5. make a video of them if you want (like shown here)

## Key Reference
- Manick, R., et al. (2024). Detection of an embedded planet in CI Tau.