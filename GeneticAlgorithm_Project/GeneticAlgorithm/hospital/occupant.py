class Occupant:
    def __init__(self, data, age_group_map, rooms, operating_theaters):
        self.id = data["id"]
        self.gender = data["gender"]
        self.age_group = age_group_map[data["age_group"]]
        self.length_of_stay = data["length_of_stay"]
        self.workload_produced = data["workload_produced"]
        self.skill_level_required = data["skill_level_required"]
        self.room_id = data["room_id"]
        self.room = None
        for room in rooms:
            if room.id == self.room_id:
                self.room = room
        self.room.add_patient(self)