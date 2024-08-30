# Python Course final assignment 2024

My first idea for the final project was to create a notebook for the analysis of some behavioural tests tipically used in animal research (specifically using mice as animal model). Among the behavioural batteries I should eventually use during my PhD, I decided to focus on the Open Field Test (descpription below). My issue began when i couldn't find proper open source videos of this test online, at least not to the extent I needed them. So at the end I decided to first create random OFT "recordings" (in form of plots and videos) to then perform the analysis of some metrics on the resulting video. 

# Open Field Test Simulation and Analysis
This repository contains two Python scripts that simulate and analyze the random movement of a small box (representing a mouse) within a square arena, mimicking an Open Field Test (OFT) experiment. These scripts are designed to provide a simple framework for understanding animal behavior in a controlled environment.

*Script Descriptions*

**1. Plot_random_OF**

This script simulates a random walk of a small box within a 100x100 cm arena. The box represents a mouse, and its movement is determined by randomly sampling step lengths and speeds from normal distributions. Actual values of mice avarege step length and speed (and their standard error) were extracted from the Mouse Phenome Database (https://phenome.jax.org/) and are referred to wildtype animals (C57BL/6J). The box moves in random directions and reflects off the arena walls if it reaches the boundaries.

Main Features:
Simulates a random walk with customizable parameters such as mean speed, step length, and direction change rate. Tracks the box's position over a specified number of steps. Plots the path of the box within the arena.

Output:
A plot showing the path of the box within the arena.

**2. Video_random_OF_with_analysis**

This script extends the random walk simulation by generating a video of the box's movement within the arena. It also calculates statistics such as total distance traveled, time spent in the center and outer areas, and mean speed.

Main Features:
Simulates the random movement of a box within the arena and generates a video of the movement. Tracks and records statistics about the movement, including distance, speed, and time spent in different areas of the arena. Outputs a video file (random_walk_box.avi) showing the simulated movement.

Output:
A video file showing the box's movement within the arena. Printed statistics summarizing the movement, including total distance traveled, time spent in the center and outer areas, and mean speed.
