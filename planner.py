import matplotlib.pyplot as plt


__all__ = [
    'Specialization',
    'make_pretty',
]


class Specialization(dict):

    name = None

    def __getitem__(self, key):
        if key in self.keys():
            return super().__getitem__(key)
        else:
            return False

    @property
    def courses(self):
        return self.mandatory + self.optional

    def specialization_count(self):
        flag1 = [self[course] for course in self.mandatory]
        flag2 = [self[course] for course in self.optional]
        return sum(flag1 + flag2)

    def specialization_achieved(self):
        flag1 = all(self[course] for course in self.mandatory)
        flag2 = sum(self[course] for course in self.optional) >= 2
        return flag1 * flag2
    
    def degree_achieved(self):
        return sum(self.values()) >= self.Nrequired
        
    def count_500s(self):
        count = sum([self[crs] for crs in self.keys() if crs[-3] == '5'])
        return count
    
    def count_nonCHE(self):
        count = 0
        for item in self.keys():
            if not (item.startswith("CHE") or item.startswith("NANO")):
                count += 1
        return count
    

def make_pretty(styler):
    # styler.hide()
    styler.background_gradient(cmap=plt.cm.PiYG, vmin=-2, vmax=3, axis=None)
    styler.format(precision=0)
    return styler
