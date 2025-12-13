import copy
import json
import os
import random, subprocess
from globals import input_file

class Chromosome:
    def __init__(self, patients, occupants, rooms, nurses, surgeons, ots, room_ids, ot_ids, D):
        self.patients = copy.deepcopy(patients)
        self.nurses = copy.deepcopy(nurses)
        self.occupants = occupants
        self.rooms = copy.deepcopy(rooms)
        self.surgeons = copy.deepcopy(surgeons)
        self.ots = copy.deepcopy(ots)
        self.cost = None
        self.tot_hard_violations = None
        self.room_ids = room_ids
        self.ot_ids = ot_ids
        self.total_cost = None
        self.D = D
        self.crossovered = 0
        self.mutated = 0

    def get_room(self, room_id):
         for r in self.rooms:
            if r.id == room_id:
                return r
    
    def get_ot(self, ot_id):
        for ot in self.ots:
            if ot.id == ot_id:
                return ot
    
    def get_surgeon(self, surgeon_id):
        for s in self.surgeons:
            if s.id == surgeon_id:
                return s

    def sorted_mandatory_patients(self):
       mandatory_patients = []
       for p in self.patients:
           if p.mandatory == True:
                mandatory_patients.append(p)
       return sorted(mandatory_patients, key = lambda p : p.surgery_due_day - p.surgery_release_day)
    

    def find_available_nurses(self, day_shift):
        available_nurses = []
        for nurse in self.nurses:
            if nurse.working_shifts[day_shift]>0:
                available_nurses.append(nurse)
        return available_nurses

    
    def fix_uncovered_rooms(self):
        for r in random.sample(self.rooms, len(self.rooms)):
            for i in range(self.D):
                if len(r.schedule_patients[i])>0: # check if the room is occupied in the i-th day
                    for shift_offset in range(3):
                        day_shift = i*3 + shift_offset
                        if r.schedule_nurses[day_shift] == '': # check if in that shift of the i-th day, there is a nurse or not.
                            available_nurses = self.find_available_nurses(day_shift)
                            if len(available_nurses)>0: 
                                available_nurse = random.choice(available_nurses)
                                r.assign_nurse(available_nurse, day_shift)
                                available_nurse.assigned_room[day_shift].append(r)
                            else:
                                return False
                            
        return True


    def random_initialize(self): 
        # It randomly initializes the chromosome. The function arranges first the mandatory patients sorted
        # (with ascending order) according to the length of the interval between surgery_release_day 
        # and surgery_due_day. Then, it arranges the non mandatory patients, if any.
        mandatory_patients = self.sorted_mandatory_patients()
        for patient in mandatory_patients:
            patient.rooms = self.rooms
            patient.operating_theaters = self.ots
            for s in self.surgeons:
                if s.id == patient.surgeon_id:
                    patient.surgeon = s
            valid = patient.initialize_patient()
            if valid == False:
               return False
        non_mandatory_patients = list(set(self.patients)-set(mandatory_patients))
        for patient in random.sample(non_mandatory_patients, len(non_mandatory_patients)):
            patient.rooms = self.rooms
            patient.operating_theaters = self.ots
            for s in self.surgeons:
                if s.id == patient.surgeon_id:
                    patient.surgeon = s
            valid_patient = patient.initialize_patient()
            if valid_patient == False:
               return False

        # After having arranged the patients, the nurses are assigned to the rooms too.
        for nurse in random.sample(self.nurses, len(self.nurses)):
            nurse.rooms = self.rooms
            nurse.initialize_nurse()
        
        # This last function is fundamental to satisfy the hard constraint "UncoveredRoom". It basically
        # scans all the occupied rooms and if there are any that are not covered by a nurse
        # at a specific shift, it tries to assign one random nurse chosen from the ones available
        # at that shift.
        valid_nurses = self.fix_uncovered_rooms()

        if valid_nurses == True:
            return True
        return False

    # This function is used to represent the chromosome in .json format, in order to be evaluated by the
    # validator. 
    def to_json(self): 
        solution_patients = []
        for p in self.patients:
            solution_patients.append(p.to_dict())

        solution_nurses = []
        for n in self.nurses:
            solution_nurses.append(n.to_dict())

        return {
            "patients" : sorted(solution_patients, key=lambda p: p["id"]),
            "nurses" : sorted(solution_nurses, key=lambda n: n["id"])
        }

    
    def save_to_file(self):
      name_file = f"ch_{id(self)}.json"
      with open(name_file, "w") as f:
          json.dump(self.to_json(), f, indent=2)
      return name_file


    def save_solution(self):
      name_file = f"ch_{self.total_cost[0]}_{self.total_cost[1]}.json"
      with open(name_file, "w") as f:
          json.dump(self.to_json(), f, indent=2)
      return name_file
    
    
    def compute_cost(self):
        # This function is used to compute the total violations and the total cost by using the validator.
        file_ch = self.save_to_file()  
        hard_violations = None
        cost = None
        with open("output.txt", "w") as out_file:
            subprocess.run(
                ["IHTP_Validator_2.exe", input_file, file_ch],
                stdout=out_file,
                stderr=subprocess.STDOUT  
            )
        with open("output.txt") as f:
            for line in f:
                if "Total violations" in line:
                    hard_violations = int(line.strip().split('=')[1])
                if "Total cost" in line:
                    cost = int(line.strip().split('=')[1])
        os.remove(file_ch)
        os.remove("output.txt")
        self.total_cost = (hard_violations, cost)


    