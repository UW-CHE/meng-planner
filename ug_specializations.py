from base import (
    Specialization,
)


class EES(Specialization):
    name = 'Energy and Environmental Systems and Processes'
    max_per_term = [2, 2, 2]
    N_required = 4
    required = []
    optional = [
        'CHE499',
        'CHE500',
        'CHE514',
        'CHE516',
        'CHE520',
        'CHE565',
        'CHE571',
        'CHE572',
        'CHE574',
        'EARTH458',
        'EARTH459',
        'ENVE376',
        'ENVE573',
        'ENVE577',
        'ME452',
        'ME459',
        'ME571',
    ]


class PSE(Specialization):
    name = 'Chemical Process Modelling, Optimization and Control'
    max_per_term = [2, 2, 2]
    N_required = 4
    required = []
    optional = [
        'CHE499',
        'CHE500',
        'CHE520',
        'CHE521',
        'CHE522',
        'CHE524',
        'CHE565',
        'EARTH456',
        'ME362',
        'ME559',
        'ME566',
        'MSE332',
        'MSE431',
        'MSE432',
        'MSE551',
        'NE451',
        'SYDE531',
    ]


class MMP(Specialization):
    name = 'Materials and Manufacturing Processes'
    max_per_term = [2, 2, 2]
    N_required = 4
    required = []
    optional = [
        'CHE499',
        'CHE500',
        'CHE520',
        'CHE541',
        'CHE543',
        'CHE560',
        'CHE561',
        'CHE562',
        'CHE564',
        'CHE565',
        'CHE571',
        'ME435',
        'ME531',
        'ME533',
        'MSE432',
        'MSE551',
        'NE352',
    ]

