from base import (
    Specialization,
    Degree,
)


class AccelMEngMLAI(Specialization):
    name = 'Accel MEng in AI/ML'
    max_per_term = [1, 1, 3, 3]
    N_required = 8
    required = ['CHE523', 'CHE626']
    optional = ['CHE520', 'CHE521', 'CHE522', 'CHE621', 'CHE620']


class MEngMLAI(Specialization):
    name = 'MEng in AI/ML'
    max_per_term = [3, 3, 3]
    N_required = 8
    required = ['CHE523', 'CHE626']
    optional = ['CHE520', 'CHE521', 'CHE522', 'CHE621', 'CHE620']


class MEng(Degree):
    name = 'MEng'
    max_per_term = [3, 3, 3]
    N_required = 8
    required = []
    optional = []


class MEngCoop1Term(Degree):
    name = 'MEng Coop - 1 Term'
    max_per_term = [3, 3, 0, 3]
    N_required = 8
    required = []
    optional = []


class MEngCoop2Term(Degree):
    name = 'MEng Coop - 2 Term'
    max_per_term = [3, 3, 0, 0, 3]
    N_required = 8
    required = []
    optional = []


class AccelMEngSEAM(Specialization):
    name = 'Accel MEng in Sustainable Energy & Materials'
    max_per_term = [1, 1, 3, 3]
    N_required = 8
    required = ['SEED671', 'SEED681']
    optional = ['CHE571', 'CHE572', 'CHE514', 'CHE602']


class MEngHLTH(Specialization):
    name = 'Accel MEng in Health Technologies'
    max_per_term = [3, 3, 3]
    N_required = 9
    required = ['PHIL699', 'ECON622']
    optional = ['HLTH680', 'HLTH681', 'HLTH683', 'HLTH687']
    N_outside = 4
