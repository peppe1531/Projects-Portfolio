import random
class Nurse:
    def __init__(self, data, D, shift_map, rooms, operating_theaters):
        self.id = data["id"]
        self.skill_level = data["skill_level"]
        self.working_shifts = [-1 for _ in range(3*D)]
        self.assigned_room =  [[] for _ in range(3*D)]
        for shift in data["working_shifts"]:
            if shift["shift"]=="early":
                self.working_shifts[shift["day"]*3]=shift["max_load"]
            elif shift["shift"]=="late":
                self.working_shifts[shift["day"]*3+1]=shift["max_load"]
            elif shift["shift"]=="night":
                self.working_shifts[shift["day"]*3+2]=shift["max_load"]
        self.D = D
        self.shift_map = shift_map
        self.rooms = None

    # It finds all the rooms that are uncovered at the shift passed as argument.
    def find_compatible_rooms(self, shift_index):  
        day = shift_index//3
        compatible_rooms = []
        for r in self.rooms:
            if len(r.schedule_patients[day]) != 0 and r.schedule_nurses[shift_index]=='':
                compatible_rooms.append(r)
        return compatible_rooms


    def initialize_nurse(self): 
        # for each i-th shift, it assigns a random number of rooms to the nurse
        num_rooms = len(self.rooms)
        for i in range(3*self.D): 
            if self.working_shifts[i]>0:
                compatible_rooms = self.find_compatible_rooms(i)
                if len(compatible_rooms)!=0:
                    num_selected_rooms = random.randint(0, len(compatible_rooms))
                    self.assigned_room[i] = random.sample(compatible_rooms, k=min(num_selected_rooms, num_rooms))
                    for r in self.assigned_room[i]:
                        r.assign_nurse(self, i)

    
    def to_dict(self):
        assignments = []
        for i in range(3*self.D):
            if self.working_shifts[i]>0:
                day = i//3
                id_shift = i%3
                shift = ""
                for key in self.shift_map.keys():
                    if self.shift_map[key]==id_shift:
                        shift = key
                assignments.append({"day": day, "shift": shift, "rooms": sorted([r.id for r in self.assigned_room[i]])})
        return {"id": self.id, "assignments": assignments}
