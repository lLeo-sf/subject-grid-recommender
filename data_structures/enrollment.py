from typing import List
from data_structures.subject import Subject

class Enrollment: 
    semesterNumber: int = 0
    subjects: List[Subject]
    maxCredit: int = 400
    credit: int

    def __init__(self, number):
        self.number = number
        self.subjects = []
        self.credit = 0
        
    def AddSubject(self, id: str, subject: Subject):
        if (self.credit + subject.credit) > self.maxCredit:
            return False

        self.subjects[id] = subject
        self.credits += subject.credit
        return True

    def isFull(self):
        return (self.maxCredit - self.credit) < 32

    def isEmpty(self):
        return len(self.materias) == 0

    def isEvenSemester(self):
        return self.semesterNumber % 2 == 0