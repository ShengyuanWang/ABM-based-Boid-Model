# ABM-based-Boid-Model
Capstone Project for 2023 Fall Math Modeling Course @ Macalester College  
`Author: Shengyuan (Alan) Wang`

## Introduction
This project is a simulation of the flocking behavior of birds. The model is based on the Boid model proposed by Craig Reynolds in 1986. The model is an agent-based model, which means that each bird is an agent that has its own set of rules to follow. The model is implemented in Python using the Mesa library. The model is also visualized using the matplotlib library and PyQt5.

## How to run the model
1. Install the required libraries: matplotlib, PyQt5
2. Run the `simulation.py` file for visualization of the model
3. Run the `main.ipynb` file for the model with different parameters to test the hypothesis shown in my paper.

## Repository Structure
- `simulation.py`: the main file for visualization of the model
- `main.ipynb`: the main file for running the model with different parameters
- `Agent/`: the folder that contains the agent class, including Boids, Predators, and Obstacles (Mountain)
