import matplotlib.pyplot as plt


__all__ = [
    'Specialization',
    'Degree'
]


class Degree(dict):

    name = None
    N_per_term = [3, 3, 3]
    N_required = 8
    required = []
    optional = []
    N_outside = 2

    def __getitem__(self, key):
        if key in self.keys():
            return super().__getitem__(key)
        else:
            return False

    @property
    def courses(self):
        return self.required + self.optional

    def degree_achieved(self):
        return sum(self.values()) >= self.N_required
        
    def count_500s(self):
        count = sum([self[crs] for crs in self.keys() if crs[-3] == '5'])
        return count
    
    def count_nonCHE(self):
        count = 0
        for item in self.keys():
            if not (item.startswith("CHE") or item.startswith("NANO")):
                count += int(self[item])
        return count


class Specialization(Degree):

    def specialization_count(self):
        flag1 = [self[course] for course in self.required]
        flag2 = [self[course] for course in self.optional]
        return sum(flag1 + flag2)

    def specialization_achieved(self):
        flag1 = all(self[course] for course in self.required)
        flag2 = sum(self[course] for course in self.optional) >= 2
        return flag1 * flag2
