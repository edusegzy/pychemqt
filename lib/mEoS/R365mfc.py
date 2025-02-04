#!/usr/bin/python
# -*- coding: utf-8 -*-

from lib.meos import MEoS
from lib import unidades


class R365mfc(MEoS):
    """Multiparameter equation of state for R365mfc"""
    name = "1,1,1,3,3-pentafluorobutane"
    CASNumber = "406-58-6"
    formula = "CF3CH2CF2CH3"
    synonym = "R365mfc"
    rhoc = unidades.Density(473.838464)
    Tc = unidades.Temperature(460.0)
    Pc = unidades.Pressure(3266.0, "kPa")
    M = 148.07452  # g/mol
    Tt = unidades.Temperature(239.0)
    Tb = unidades.Temperature(313.3)
    f_acent = 0.377
    momentoDipolar = unidades.DipoleMoment(3.807, "Debye")
    id = 671
    # id = None

    CP1 = {"ao": 4.,
           "an": [], "pow": [],
           "ao_exp": [17.47, 16.29], "exp": [569., 2232.],
           "ao_hyp": [], "hyp": []}

    helmholtz1 = {
        "__type__": "Helmholtz",
        "__name__": "Helmholtz equation of state for R-365mfc of McLinden and Lemmon. (2013)",
        "__doi__": {"autor": "McLinden, M.O. and Lemmon, E.W.",
                    "title": "Thermodynamic Properties of R-227ea, R-365mfc, R-115, and R-13I1", 
                    "ref": "to be submitted to J. Chem. Eng. Data, 2013",
                    "doi":  ""}, 
                    
        "R": 8.314472,
        "cp": CP1,
        "ref": "NBP", 
        
        "Tmin": Tt, "Tmax": 500.0, "Pmax": 35000.0, "rhomax": 9.3, 
        "Pmin": 2.478, "rhomin": 9.3, 

        "nr1": [2.20027, -2.86240, 0.384559, -0.621227, 0.066596],
        "d1": [1, 1, 2, 2, 4],
        "t1": [0.24, 0.67, 0.5, 1.25, 1],

        "nr2": [-1.19383, 0.635935, 0.461728, -0.533472, -1.07101, 0.139290],
        "d2": [1, 3, 6, 6, 2, 3],
        "t2": [3.35, 2.5, 0.96, 1.07, 5.6, 6.9],
        "c2": [1, 1, 1, 1, 2, 2],
        "gamma2": [1]*6,

        "nr3": [-0.385506, 0.885653, 0.226303, -0.166116],
        "d3": [1, 1, 1, 2],
        "t3": [3, 3.6, 5, 1.25],
        "alfa3": [0.97, 0.94, 2.15, 2.66],
        "beta3": [1.07, 1.08, 10.9, 22.6],
        "gamma3": [1.48, 1.49, 1.01, 1.16],
        "epsilon3": [1.02, 0.62, 0.53, 0.48]}

    eq = helmholtz1,

    _surface = {"sigma": [0.0534], "exp": [1.21]}
    _vapor_Pressure = {
        "eq": 5,
        "ao": [-0.80955e1, 0.20414e1, -0.13333e2, 0.25514e2, -0.19967e2],
        "exp": [1.0, 1.5, 3.4, 4.3, 5.0]}
    _liquid_Density = {
        "eq": 1,
        "ao": [0.17933e1, -0.18792e1, 0.90006e1, -0.11669e2, 0.56329e1],
        "exp": [0.31, 0.6, 0.9, 1.2, 1.5]}
    _vapor_Density = {
        "eq": 3,
        "ao": [-.1612e1, -.67679e1, -.24499e2, .33398e1, -.2111e3, .25807e3],
        "exp": [0.281, 0.91, 3.0, 5.0, 8.0, 10.0]}
