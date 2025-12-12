import copy
import random
import subprocess
from chromosome import Chromosome
from globals import input_file

class GeneticAlgorithm:

  def __init__(self, first_population, eras, patients, nurses, rooms, occupants, surgeons, ots, room_ids, ot_ids, D, crossover_probability=0.8, mutation_probability=0.1, schedule_non_mandatory=0.5, unschedule_non_mandatory=0.4):
    self.patients = patients
    self.nurses = nurses
    self.occupants = occupants
    self.surgeons = surgeons
    self.ots = ots
    self.room_ids = room_ids
    self.ot_ids = ot_ids
    self.rooms = rooms
    self.D = D
    self.current_population = first_population
    self.num_population = len(first_population) # size of the population
    self.num_selected = int(0.4*self.num_population) # number of chromosomes selected at selection stage
    self.num_eras = eras
    self.original_crossover_probability = crossover_probability
    self.original_mutation_probability = mutation_probability
    self.original_schedule_non_mandatory = schedule_non_mandatory
    self.original_unschedule_non_mandatory = unschedule_non_mandatory
    self.crossover_probability = crossover_probability
    self.mutation_probability = mutation_probability
    self.schedule_non_mandatory = schedule_non_mandatory
    self.unschedule_non_mandatory = unschedule_non_mandatory
    self.best = None
    self.num_times_best = 0
    self.stagnation = 10
    self.flag_save_file = False
    self.best_file = None


  def hasChanged(self, child):
      if child.crossovered==1 or child.mutated==1:
          return True
      return False
     
  
  def crossover(self, parent1, parent2):
    num_patients = random.randint(1, 10) # choose randomly the number of patients to exchange
    child1 = copy.deepcopy(parent1) # chromosome 1
    child2 = copy.deepcopy(parent2) # chromosome 2
    for i1 in random.sample(list(range(len(child1.patients))), num_patients):
        for i2 in range(len(child2.patients)):
            if child1.patients[i1].id == child2.patients[i2].id:
                temp_patient2 = child2.patients[i2]
                temp_patient1 = child1.patients[i1]
                if temp_patient2.admission_day is not None and temp_patient1.admission_day is not None:
                    # after having selected the patient to exchange, first they are both unscheduled in their 
                    # respective chromosomes.
                    temp_patient2.room.remove_patient(temp_patient2)
                    temp_patient2.surgeon.unschedule_surgery(temp_patient2.admission_day, temp_patient2.surgery_duration)
                    temp_patient2.operating_theater.unschedule_patient(temp_patient2)
         
                    temp_patient1.room.remove_patient(temp_patient1)
                    temp_patient1.surgeon.unschedule_surgery(temp_patient1.admission_day, temp_patient1.surgery_duration)
                    temp_patient1.operating_theater.unschedule_patient(temp_patient1)
                  
                    # They are then scheduled within the chromosome to which they are assigned after the crossover
                    # without changing their admission day, room and operating theater
                    temp_patient2.room = child1.get_room(temp_patient2.room.id)
                    temp_patient2.room.add_patient(temp_patient2)
                    temp_patient2.surgeon = child1.get_surgeon(temp_patient2.surgeon.id)
                    temp_patient2.surgeon.schedule_surgery(temp_patient2.admission_day, temp_patient2.surgery_duration)
                    temp_patient2.operating_theater = child1.get_ot(temp_patient2.operating_theater.id)
                    temp_patient2.operating_theater.schedule_patient(temp_patient2)
                    temp_patient2.rooms = child1.rooms
                    temp_patient2.operating_theaters = child1.ots
                    child1.patients[i1] = temp_patient2
                    
                    temp_patient1.room = child2.get_room(temp_patient1.room.id)
                    temp_patient1.room.add_patient(temp_patient1)
                    temp_patient1.surgeon = child2.get_surgeon(temp_patient1.surgeon.id)
                    temp_patient1.surgeon.schedule_surgery(temp_patient1.admission_day, temp_patient1.surgery_duration)
                    temp_patient1.operating_theater = child2.get_ot(temp_patient1.operating_theater.id)
                    temp_patient1.operating_theater.schedule_patient(temp_patient1)
                    temp_patient1.rooms = child2.rooms
                    temp_patient1.operating_theaters = child2.ots
                    child2.patients[i2] = temp_patient1
                    
                    child1.crossovered = 1
                    child2.crossovered = 1
    
    return child1, child2
  

  def selection(self):
    sorted_chromosomes = sorted(self.current_population, \
                                  key = lambda chr : chr.total_cost[1])

    return sorted_chromosomes[:self.num_selected]


  def mutate_patient(self, patient, child, mandatory):
      n = random.choice([0, 1, 2]) # choose randomly one type of mutation
      if n == 0: #change room
          compatible_rooms = patient.find_compatible_rooms([patient.room])
          if len(compatible_rooms)!=0:
              patient.room.remove_patient(patient)
              patient.assign_room_to_patient([patient.room])
              child.mutated = 1
            
      elif n == 1: #change ot
          compatible_ots = patient.find_compatible_ots([patient.operating_theater])
          if len(compatible_ots)!=0:
              patient.operating_theater.unschedule_patient(patient)
              patient.assign_ot_to_patient([patient.operating_theater])
              child.mutated = 1

      elif n == 2: #change admission day
          current_admission_day = patient.admission_day
          if mandatory==True:
              possible_days = list(set(range(patient.surgery_release_day, patient.surgery_due_day + 1))-set([current_admission_day]))
          else:
              possible_days = list(set(range(patient.surgery_release_day, patient.D))-set([current_admission_day]))
          random.shuffle(possible_days)
          for day in possible_days:
              patient.admission_day = day
              if len(patient.find_compatible_ots(None))>0 and len(patient.find_compatible_rooms(None))>0:
                  if patient.surgeon.check_schedule_surgery(day, patient.surgery_duration) == True:
                      patient.admission_day = current_admission_day
                      patient.surgeon.unschedule_surgery(patient.admission_day, patient.surgery_duration)
                      patient.operating_theater.unschedule_patient(patient)
                      patient.room.remove_patient(patient)
                      patient.admission_day = day
                      patient.surgeon.schedule_surgery(patient.admission_day, patient.surgery_duration)
                      patient.operating_theater = random.choice(patient.find_compatible_ots(None))
                      patient.operating_theater.schedule_patient(patient)
                      patient.room = random.choice(patient.find_compatible_rooms(None))
                      patient.room.add_patient(patient)
                      child.mutated = 1
                      break


  def mutation(self, child):
    for patient in random.sample(child.patients, len(child.patients)): # Iterate randomly over all the patients
        if patient.mandatory==True:
            if random.random()<self.mutation_probability:
                self.mutate_patient(patient, child, mandatory=True)
        if patient.mandatory == False:
            if patient.admission_day == None:
                patient.initialize_patient(assign_prob = self.schedule_non_mandatory) 
                # The higher self.schedule_non_mandatory is, the more probable is the scheduling of a 
                # non mandatory patient.
                child.mutated = 1
            elif random.random()<self.mutation_probability:
                self.mutate_patient(patient, child, mandatory=False)
            else:
                if random.random() < self.unschedule_non_mandatory: 
                    patient.room.remove_patient(patient)
                    patient.operating_theater.unschedule_patient(patient)
                    patient.surgeon.unschedule_surgery(patient.admission_day, patient.surgery_duration)
                    patient.room = None
                    patient.operating_theater = None
                    patient.admission_day = None
                    child.mutated = 1

    # In this loop, for each nurse, we randomly decide whether to assign additional rooms to be 
    # covered during a specific shift or to remove some of the existing room assignments.
    for nurse in random.sample(child.nurses, len(child.nurses)):
        if random.random() < self.mutation_probability:
            shifts = [i for i in range(len(nurse.working_shifts)) if nurse.working_shifts[i] > 0]
            chosen_shifts = random.sample(shifts, random.randint(1, len(shifts)))
            for shift in chosen_shifts:
                add_rooms = random.random()
                if add_rooms > 0.5:
                    compatible_rooms = nurse.find_compatible_rooms(shift)
                    if len(compatible_rooms)!=0:
                        num_rooms_to_add = random.randint(0, len(compatible_rooms))
                        nurse.assigned_room[shift] += random.sample(compatible_rooms, k=min(num_rooms_to_add, len(nurse.rooms)))
                        for r in nurse.assigned_room[shift]:
                            r.assign_nurse(nurse, shift)
                        child.mutated = 1
                elif len(nurse.assigned_room[shift])>0:
                    num_rooms_to_remove = random.randint(0, len(nurse.assigned_room[shift]))
                    rooms_to_remove = random.sample(nurse.assigned_room[shift], num_rooms_to_remove)
                    for r in rooms_to_remove:
                        r.remove_nurse(shift)
                    nurse.assigned_room[shift] = list(set(nurse.assigned_room[shift])-set(rooms_to_remove))
                    child.mutated = 1
    return child
  
  
  def evolve(self):
    era = 0
    while era<self.num_eras:
      print(era)
      parents = self.selection() # we select the parents by choosing the best chromosomes of the population
      if self.num_times_best>=2*self.stagnation and random.random()>0.5:
          parents = self.enforce_injection(era, parents)
      new_population = []+parents
      
      while len(new_population)!=self.num_population: # creation of the new generation
          parent1, parent2 = random.sample(parents, 2)
          if random.random()<self.crossover_probability:
              child1, child2 = self.crossover(parent1, parent2)
          else:
              child1, child2 = copy.deepcopy(parent1), copy.deepcopy(parent2)
          child1 = self.mutation(child1)
          child1.fix_uncovered_rooms()
          child1.compute_cost()
          if child1.total_cost[0]==0 and len(new_population)<self.num_population and self.hasChanged(child1)==True:
              new_population.append(child1)
              print(f"new child added at era {era}, length current population = {len(new_population)}")
              print(f"Crossovered: {child1.crossovered}  Mutated: {child1.mutated}")
              child1.crossovered = 0
              child1.mutated = 0
          child2 = self.mutation(child2)
          child2.fix_uncovered_rooms()
          child2.compute_cost()
          if child2.total_cost[0]==0 and len(new_population)<self.num_population and self.hasChanged(child2)==True:
              new_population.append(child2)
              print(f"new child added at era {era}, length current population = {len(new_population)}")
              print(f"Crossovered: {child2.crossovered}  Mutated: {child2.mutated}")
              child2.crossovered = 0
              child2.mutated = 0

      self.current_population = new_population
      sol = self.get_best()
      self.probability_adaptation(sol)
      if self.num_times_best>=self.stagnation:
          self.injection(era) 
      if self.flag_save_file == False:
          self.best_file = self.best.save_solution()
          self.flag_save_file = True
      era+=1
      
      # At each era, we keep track of the current best chromosome.
      result = subprocess.run(
            ["IHTP_Validator_2.exe", input_file, self.best_file],
            capture_output=True,  
            text=True             
        )

      print(result.stdout)
      print()

    
  def enforce_injection(self, era, chromosomes):
    # This function is invoked only when the algorithm continues to be stuck in a local minimum. 
    # It substitutes the worst chromosomes with new ones in order to insert more diversity and introduce
    # new crossover opportunities.
    n_new_chromosomes = len(chromosomes)-int(0.8*len(chromosomes))# choose the number of chromosomes to change
    new_chromosomes = []
    while len(new_chromosomes)!=n_new_chromosomes:
      ch = Chromosome(self.patients, self.occupants, self.rooms, self.nurses, self.surgeons, self.ots, self.room_ids, self.ot_ids, self.D)
      if ch.random_initialize() == True:
        ch.compute_cost()
        if ch.total_cost[0]==0:
            new_chromosomes.append(ch)
    chromosomes.sort(key=lambda c: c.total_cost[1])  
    chromosomes[-n_new_chromosomes:] = new_chromosomes
    random.shuffle(chromosomes)
    print(f"Injection enforced at era {era}")
    return chromosomes


  def update_probabilities(self, reset_probabilities):
    if reset_probabilities == True or self.num_times_best in [i for i in range(50, self.num_eras+1, 50)]:
      self.crossover_probability = self.original_crossover_probability
      self.mutation_probability = self.original_mutation_probability
      self.unschedule_non_mandatory = self.original_unschedule_non_mandatory
      self.schedule_non_mandatory = self.original_schedule_non_mandatory
    else:
      self.crossover_probability = max(0.6, self.crossover_probability - 0.0025)
      print(f"Crossover probability = {self.crossover_probability}")
      self.mutation_probability = min(0.5, self.mutation_probability + 0.01) 
      print(f"Mutation probability = {self.mutation_probability}")
      self.unschedule_non_mandatory = min(0.5, self.unschedule_non_mandatory + 0.005)
      print(f"Unschedule non mandatory = {self.unschedule_non_mandatory}")
      self.schedule_non_mandatory = min(0.7, self.schedule_non_mandatory + 0.005)
      print(f"Schedule non mandatory = {self.schedule_non_mandatory}")


  def probability_adaptation(self, current_solution):
    if self.best is None:
        self.best = current_solution
        self.num_times_best+=1
    elif self.best == current_solution:
        self.num_times_best+=1
    else:
        self.best = current_solution
        self.num_times_best = 1
        self.flag_save_file = False
        self.update_probabilities(reset_probabilities=True)

    if self.num_times_best>=self.stagnation:
        self.update_probabilities(reset_probabilities=False)

  def injection(self, era):
      # It tries to inject new chromosomes in the population if the algorithm is stuck in a local minimum
      print(f"Reinjection at era {era} (num_times_best = {self.num_times_best})")
      num_new = int(0.2 * self.num_population) 
      count = 0
      while count != num_new:
          new_chr = Chromosome(
              self.patients, self.occupants, self.rooms, self.nurses, self.surgeons, self.ots,
              self.room_ids, self.ot_ids, self.D
          )
          new_chr.random_initialize()
          new_chr.compute_cost()
          if new_chr.total_cost[0]==0:
            count+=1
            self.current_population.append(new_chr)
      self.current_population.sort(key=lambda c: c.total_cost[1])
      self.current_population = self.current_population[:self.num_population]


  def get_best(self):
    # It returns the best chromsome of the current population
    self.current_population.sort(key=lambda chr: chr.total_cost[1])
    return self.current_population[0]

  