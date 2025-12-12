import random

class Patient:
    def __init__(self, data, D, age_group_map, rooms, operating_theaters):
        self.id = data["id"]
        self.mandatory = data["mandatory"]
        self.gender = data["gender"] 
        self.age_group = age_group_map[data["age_group"]]
        self.length_of_stay = data["length_of_stay"]
        self.surgery_release_day = data["surgery_release_day"]
        if "surgery_due_day" in data.keys():
            self.surgery_due_day = data["surgery_due_day"]
        else:
            self.surgery_due_day = None
        self.surgery_duration = data["surgery_duration"]
        self.surgeon_id = data["surgeon_id"]
        self.incompatible_room_ids = data.get("incompatible_room_ids", [])
        self.workload_produced = data["workload_produced"]
        self.skill_level_required = data["skill_level_required"]
        self.D = D
        self.admission_day = None
        self.room = None
        self.operating_theater = None
        self.rooms = rooms
        self.operating_theaters = operating_theaters
        self.surgeon = None
    
    def get_room(self, room_id):
        for r in self.rooms:
            if r.id == room_id:
                return r
            
    def find_compatible_rooms(self, rooms_to_exclude):
        compatible_rooms = []
        for r in self.rooms:
            if r.isCompatible(self) == True and r.id not in self.incompatible_room_ids:
                compatible_rooms.append(r)
        if rooms_to_exclude == None:
            return compatible_rooms
        else:
            return list(set(compatible_rooms)-set(rooms_to_exclude))
            
    def assign_room_to_patient(self, rooms_to_exclude):
        compatible_rooms = self.find_compatible_rooms(rooms_to_exclude)
        if len(compatible_rooms)!=0:
            self.room = random.choice(compatible_rooms)
            self.room.add_patient(self)
            return True
        else:
            return False
           

    def find_compatible_ots(self, ots_to_exclude):
        compatible_ots = []
        for ot in self.operating_theaters:
            if ot.isCompatible(self) == True:
                compatible_ots.append(ot)
        if ots_to_exclude == None:
            return compatible_ots
        else:
            return list(set(compatible_ots)-set(ots_to_exclude))

    def assign_ot_to_patient(self, ots_to_exclude):
        compatible_ots = self.find_compatible_ots(ots_to_exclude)
        if len(compatible_ots) != 0:
            self.operating_theater = random.choice(compatible_ots)
            self.operating_theater.schedule_patient(self)
            return True
        else:
            return False
           
    

    def initialize_patient(self, assign_prob = 0.5):
        # If the patient is not mandatory, with a certain probability we decide whether to admit it or not.
        if self.mandatory == False and random.random() > assign_prob: 
            return True
        possible_days = []
        if self.mandatory == True:
            possible_days = list(range(self.surgery_release_day, self.surgery_due_day + 1))
        else:
            possible_days = list(range(self.surgery_release_day,  self.D))   
        random.shuffle(possible_days)
        found = 0
        for day in possible_days:
            self.admission_day = day
            # for each possible day, we check whether the patient can be correcly hospitalized by using the 
            # two following if statements.
            if self.surgeon.check_schedule_surgery(day, self.surgery_duration) == True:
                if len(self.find_compatible_rooms(None))>0 and len(self.find_compatible_ots(None))>0:
                    found = 1
                    self.surgeon.schedule_surgery(day, self.surgery_duration)
                    self.assign_room_to_patient(None)
                    self.assign_ot_to_patient(None)
                    break
        if found==0:
            self.admission_day = None
            return False
        else:
            return True
        


    def to_dict(self):
        if self.admission_day is not None:
            return {"id": self.id, "admission_day": self.admission_day, "room": self.room.id,
                                      "operating_theater": self.operating_theater.id}
        else:
            return {"id": self.id, "admission_day": "none"}

