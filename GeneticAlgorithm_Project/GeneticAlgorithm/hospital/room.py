from hospital.occupant import Occupant

class Room:
    def __init__(self, data, D):
        self.id = data["id"]
        self.capacity = data["capacity"]
        self.schedule_patients = [[] for _ in range(D)] # it keeps track of patients assigned in this room, for each day
        self.schedule_nurses = ['' for _ in range(3*D)] # the same, but with nurses, for each shift
        self.D = D
    
    
        
    def assign_nurse(self, nurse, shift):
        self.schedule_nurses[shift] = nurse.id
    
    def remove_nurse(self, shift):
        self.schedule_nurses[shift] = ''
    
    def add_patient(self, patient):
        if isinstance(patient, Occupant):
            admission_day = 0
        else:
            admission_day = patient.admission_day
        length_of_stay = patient.length_of_stay
        for i in range(admission_day, min(admission_day+length_of_stay, self.D)):
            self.schedule_patients[i].append(patient)


    def remove_patient(self, patient):
        admission_day = patient.admission_day
        length_of_stay = patient.length_of_stay
        for i in range(admission_day, min(admission_day+length_of_stay, self.D)):
            for p in self.schedule_patients[i]:
                if p.id == patient.id:
                    self.schedule_patients[i].remove(p)
            
    def get_gender(self, patient):
        genders = set()
        for i in range(patient.admission_day, min(patient.admission_day+patient.length_of_stay, self.D)):
            day_genders = [p.gender for p in self.schedule_patients[i]]
            genders.update(day_genders)
        if len(genders)>1:
            return 'mix'
        if len(genders) == 0:
            return patient.gender
        else:
            return genders.pop()
    
    def check_capacity(self, patient):
        for i in range(patient.admission_day, min(patient.admission_day+patient.length_of_stay, self.D)):
            if len(self.schedule_patients[i])>=self.capacity:
                return False
        return True
    
    # Useful to find whether the current room is compatible with the patient passed as argument
    def isCompatible(self, patient):  
        if patient.gender == self.get_gender(patient) and self.check_capacity(patient)==True:
            return True
        else:
            return False
        