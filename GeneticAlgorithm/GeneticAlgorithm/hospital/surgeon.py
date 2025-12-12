class Surgeon:
    def __init__(self, data, D):
        self.id = data["id"]
        self.max_surgery_time = data["max_surgery_time"]

    def check_schedule_surgery(self, day, surgery_time):
        if self.max_surgery_time[day] >= surgery_time:
            return True
        else:
            return False

    def schedule_surgery(self, day, surgery_time):
        self.max_surgery_time[day] -= surgery_time

    def unschedule_surgery(self, day, surgery_time):
        self.max_surgery_time[day] += surgery_time