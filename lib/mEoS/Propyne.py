#!/usr/bin/python
# -*- coding: utf-8 -*-

from lib.meos import MEoS
from lib import unidades


class Propyne(MEoS):
    """Multiparamenter equation of state for propyne"""
    name = "Propyne"
    CASNumber = "74-99-7"
    formula = "CH3-C≡CH"
    synonym = ""
    rhoc = unidades.Density(244.898798)
    Tc = unidades.Temperature(402.38)
    Pc = unidades.Pressure(5626.0, "kPa")
    M = 40.06  # g/mol
    Tt = unidades.Temperature(170.5)
    Tb = unidades.Temperature(248.0)
    f_acent = 0.204
    momentoDipolar = unidades.DipoleMoment(0.781, "Debye")
    id = 66

    CP1 = {"ao": 0.342418/8.3143*40.06,
           "an": [0.484403e-2/8.3143*40.06, -0.347414e-5/8.3143*40.06, 0.144887e-8/8.3143*40.06, -0.26815e-12/8.3143*40.06],
           "pow": [1, 2, 3, 4],
           "ao_exp": [], "exp": [],
           "ao_hyp": [], "hyp": []}

    helmholtz1 = {
        "__type__": "Helmholtz",
        "__name__": "Helmholtz equation of state for propyne of Polt et al. (1992)",
        "__doi__": {"autor": "Polt, A., Platzer, B., and Maurer, G.",
                    "title": "Parameter der thermischen Zustandsgleichung von Bender fuer 14 mehratomige reine Stoffe", 
                    "ref": "Chem. Technik 22(1992)6 , 216/224",
                    "doi": ""}, 
        "R": 8.3143,
        "cp": CP1,
        "ref": "NBP", 

        "Tmin": 273.0, "Tmax": 474.0, "Pmax": 32000.0, "rhomax": 16.28, 
        "Pmin": 0.2, "rhomin": 22.7, 

        "nr1": [0.102590136933e1, -0.220786016506e1, 0.107889905204e1,
                -0.986950667682, 0.459528109357e1, -0.886063623532e1,
                0.556346955561e1, -0.157450028544e1, -0.159068753573,
                0.235738270184, 0.440755494599, 0.196126150614, -0.367759650330,
                0.792931851008e-2, 0.247509085735e-2, 0.832903610194e-2],
        "d1": [0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 3, 3, 4, 4, 5],
        "t1": [3, 4, 5, 0, 1, 2, 3, 4, 0, 1, 2, 0, 1, 0, 1, 1],

        "nr2": [-0.102590136933e1, 0.220786016506e1, -0.107889905204e1,
                -0.382188466986e1, 0.830345065619e1, -0.448323072603e1],
        "d2": [0, 0, 0, 2, 2, 2],
        "t2": [3, 4, 5, 3, 4, 5],
        "c2": [2]*6,
        "gamma2": [1.65533788]*15}

    eq = helmholtz1,

    _surface = {"sigma": [0.05801], "exp": [1.205]}
    _vapor_Pressure = {
        "eq": 5,
        "ao": [-0.69162e1, 0.10904e1, -0.74791, 0.75926e1, -0.25926e2],
        "exp": [1.0, 1.5, 2.2, 4.8, 6.2]}
    _liquid_Density = {
        "eq": 1,
        "ao": [0.22754, 0.33173e1, -0.18041e1, 0.22440e1, -0.35823],
        "exp": [0.1, 0.53, 1.0, 2.0, 3.0]}
    _vapor_Density = {
        "eq": 3,
        "ao": [-0.17504, -0.46021e1, -0.89211e2, 0.18002e3, -0.24399e3, 0.16035e3],
        "exp": [0.1, 0.56, 2.5, 3.0, 4.0, 5.0]}
