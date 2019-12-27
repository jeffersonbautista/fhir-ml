class Patient:
    def __init__(self, patient_id):
        self.id = patient_id
        self.gender = None

class Observation(Patient):
    def __init__(self):
        pass

class Condition(Patient):
    def __init__(self):
        pass