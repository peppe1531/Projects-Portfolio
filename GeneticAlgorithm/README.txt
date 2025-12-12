The purpose of this project is to implement a Genetic Algorithm to be applied to a stochastic optimization problem. Specifically, it addresses the Integrated Healthcare Timetabling Problem, which consists in finding the most optimal arrangement of patients, resources, and hospital staff.

Before running the program, you need to set the global variable input_file in the file globals.py with the name of the instance file you want to test the algorithm on. Afterwards, inside main.py, you can define the population size by setting the parameter N. You can also specify the maximum number of iterations by passing it as the second argument to the constructor of the GeneticAlgorithm object.

To run the program, simply execute the file main.py.

The core of the algorithm is implemented within the GeneticAlgorithm class, where it is also possible to modify several parameter values, such as num_selected, crossover_probability, mutation_probability, and others.

The classes representing the hospital entities: Nurse, Patient, Occupant, Surgeon, OperatingTheater and Room. They are all contained within the hospital folder.

The Chromosome class is used to represent potential solutions to the optimization problem. It relies on the validator IHTP_Validator_2.exe to compute the number of hard and soft violations. The executable IHTP_Validator_2.exe is provided in the project folder.

The solutions of the instances where the algorithm successfully converged are stored in the "solutions" folder, inside "GeneticAlgorithm" folder, organized by instance. For a single instance, multiple solutions may be available, each obtained with a different population size and maximum number of iterations, as reported in the report.