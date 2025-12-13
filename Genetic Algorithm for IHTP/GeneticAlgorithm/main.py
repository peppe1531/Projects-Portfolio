import json
import time
import subprocess
from chromosome import Chromosome
from hospital.nurse import Nurse
from hospital.occupant import Occupant
from hospital.ot import OperatingTheater
from hospital.patient import Patient
from hospital.surgeon import Surgeon
from hospital.room import Room
from GA import GeneticAlgorithm
from globals import input_file

with open(input_file, "r") as f: 
    data = json.load(f) # open the istance file in order to read data

print(data.keys())

D = data["days"] # get the number of days
shift_map = {name: i for i, name in enumerate(data["shift_types"])} 
age_group_map = {name: i for i, name in enumerate(data["age_groups"])}
print(shift_map)
print(age_group_map)

weights = data["weights"]

# From now, all the objects related to the rooms, operating theaters, occupants, patients, nurses 
# and surgeons are created and stored in Python lists.
rooms = []
room_ids = []
for room in data["rooms"]:
    rooms.append(Room(room, D))
    room_ids.append(room["id"])

operating_theaters = []
ot_ids = []
for ot in data["operating_theaters"]:
    operating_theaters.append(OperatingTheater(ot))
    ot_ids.append(ot["id"])

occupants = []
for occ in data["occupants"]:
    occupant = Occupant(occ, age_group_map, rooms, operating_theaters)
    occupants.append(occupant)

patients = []
for patient in data["patients"]:
    patients.append(Patient(patient, D, age_group_map, None, None))

nurses = []
for nurse in data["nurses"]:
    nurses.append(Nurse(nurse, D, shift_map, None, None))

surgeons = []
for surgeon in data["surgeons"]:
    surgeons.append(Surgeon(surgeon, D))

N = 20 # dimension of the population

population = []

# The following while loop is used to generate the first generation of chromosomes.
while len(population)!=N: 
    ch = Chromosome(patients, occupants, rooms, nurses, surgeons, operating_theaters, room_ids, ot_ids, D)
    valid = ch.random_initialize() 
    if valid == False: # A first check after the function random_initialize() is executed
        continue
    ch.compute_cost()
    # Then, for being sure, we double check whether the number of hard violations is 0. If it is, then
    # add the chromosome to the population.
    if ch.total_cost[0]==0:
        population.append(ch)
        


ga = GeneticAlgorithm(population, 500, patients, nurses, rooms, occupants, surgeons, operating_theaters, room_ids, ot_ids, D)
start = time.time()
ga.evolve() # Here, the Genetic Algorithm starts.
end = time.time()
print(f"Time: {end-start}")
solution = ga.get_best()
sol_file = solution.save_solution()
print(solution.total_cost)
result = subprocess.run(
            ["IHTP_Validator_2.exe", input_file, sol_file],
            capture_output=True,  
            text=True            
        )
print(result.stdout)

