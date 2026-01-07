import matplotlib.pyplot as plt
import numpy as np


__all__ = [
    'Specialization',
    'Degree'
]


class Degree(dict):

    name = None
    max_per_term = [3, 3, 3]
    N_required = 8
    required = []
    optional = []
    ineligible = []
    N_outside = 2
    start_term = '1579'
 
    def __getitem__(self, key):
        if key in self.keys():
            return super().__getitem__(key)
        else:
            return False
        
    @property
    def prescribed_courses(self):
        courses = self.required + self.optional
        return courses
    
    @property
    def N_terms(self):
        return len(self.max_per_term)

    @property
    def courses(self):
        courses = list(self.keys())
        return courses
    
    @property
    def count_per_term(self):
        count = {}
        for course in self.keys():
            if self[course] not in count.keys():
                count[self[course]] = 0
            count[self[course]] += 1
        return list(count.values())
    
    def overloaded_terms(self):
        overloaded = np.array(self.count_per_term) > np.array(self.max_per_term)
        return overloaded

    def degree_achieved(self):
        return len(self.courses) >= self.N_required
        
    def count_500s(self):
        count = 0
        for course in self.keys():
            if course[3] == '5':
                count += 1
        return count
    
    def count_nonCHE(self):
        count = 0
        for course in self.courses:
            if not (course.startswith("CHE") or course.startswith("NANO")):
                count += 1
        return count
    

class Specialization(Degree):

    def specialization_count(self):
        set1 = set(self.courses).intersection(self.required)
        set2 = set(self.courses).intersection(self.optional)
        return len(set1.union(set2))

    def specialization_achieved(self):
        flag1 = set(self.courses).intersection(self.required) == set(self.required)
        flag2 = len(set(self.courses).intersection(self.optional)) >= 2
        flag3 = len(set(self.courses).intersection(self.required + self.optional)) >= 4
        return flag1 and flag2 and flag3
