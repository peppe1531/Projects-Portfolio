class OperatingTheater:
    def __init__(self, data):
        self.id = data["id"]
        self.daily_availability = data["availability"]
        print(self.daily_availability)
    
    def schedule_patient(self, patient): 
        # to schedule the surgery of the patient inside the operating theater
        self.daily_availability[patient.admission_day] -= patient.surgery_duration

    def unschedule_patient(self, patient): 
        # to unschedule the surgery of the patient inside the operating theater
        self.daily_availability[patient.admission_day] += patient.surgery_duration

    def isCompatible(self, patient): 
        # it finds operating theaters available in the admission day of the patient
        if self.daily_availability[patient.admission_day]>=patient.surgery_duration:
            return True
        return False