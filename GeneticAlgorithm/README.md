# Genetic Algorithm for Healthcare Timetabling

## Overview
This project implements a Genetic Algorithm to solve a stochastic optimization problem in the healthcare domain, namely the **Integrated Healthcare Timetabling Problem (IHTP)**.

The goal is to find an optimal scheduling of patients, hospital resources, and medical staff while minimizing constraint violations.

This project was developed as part of an academic assignment.

Experimental results and comparisons between different parameter configurations are reported in the accompanying project report.

## Problem Description
The Integrated Healthcare Timetabling Problem consists of determining feasible and efficient assignments for:
- patients
- nurses
- surgeons
- operating theaters
- rooms

The optimization objective is evaluated in terms of **hard and soft constraint violations**, computed using an external validator.

## Project Structure
The main components of the project are:

- `GeneticAlgorithm/`  
  Core implementation of the genetic algorithm.

- `hospital/`  
  Contains the classes representing hospital entities:
  - Nurse
  - Patient
  - Occupant
  - Surgeon
  - OperatingTheater
  - Room

- `Chromosome.py`  
  Represents candidate solutions for the optimization problem.

- `IHTP_Validator_2.exe`  
  External executable used to compute hard and soft constraint violations.

- `solutions/`  
  Stores the solutions obtained for each instance where the algorithm successfully converged.  
  Multiple solutions may exist for the same instance, obtained with different population sizes and iteration limits.


## Parameters and Configuration

Several parameters of the genetic algorithm can be tuned within the `GeneticAlgorithm` class, including:

- number of selected individuals
- crossover probability
- mutation probability
- other evolutionary parameters

These parameters directly influence the convergence behavior of the algorithm and the quality of the generated solutions.


## How to Run
Before running the program:

1. Set the global variable `input_file` in `globals.py` with the name of the instance file to test.
2. In `main.py`, define:
   - the population size by setting the parameter `N`
   - the maximum number of iterations by passing it to the `GeneticAlgorithm` constructor

To execute the algorithm:
```bash
python main.py
