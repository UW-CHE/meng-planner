from planner import (
    Specialization,
)


__all__ = [
    'AccelMEngMLAI',
    'MEngMLAI',
    'MEng',
    'AccelMEngSEAM',
]


class AccelMEngMLAI(Specialization):
    name = 'Accel MEng in AI/ML'
    N_per_term = [1, 1, 3, 3]
    Nrequired = 8
    mandatory = ['CHE523', 'CHE626']
    optional = ['CHE520', 'CHE521', 'CHE522', 'CHE621', 'CHE620']


class MEngMLAI(Specialization):
    name = 'MEng in AI/ML'
    N_per_term = [3, 3, 3]
    Nrequired = 8
    mandatory = ['CHE523', 'CHE626']
    optional = ['CHE520', 'CHE521', 'CHE522', 'CHE621', 'CHE620']


class MEng(Specialization):
    name = 'MEng'
    N_per_term = [3, 3, 3]
    Nrequired = 8
    mandatory = []
    optional = []


class AccelMEngSEAM(Specialization):
    name = 'Accel MEng in Sustainable Energy & Materials'
    N_per_term = [1, 1, 3, 3]
    Nrequired = 8
    mandatory = ['SEED671', 'SEED672']
    optional = ['CHE571', 'CHE572', 'CHE514', 'CHE602']

