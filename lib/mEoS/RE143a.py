#!/usr/bin/python
# -*- coding: utf-8 -*-

from lib.meos import MEoS
from lib import unidades


class RE143a(MEoS):
    """Multiparameter equation of state for RE143a"""
    name = "methyl trifluoromethyl ether "
    CASNumber = "421-14-7"
    formula = "CH3-O-CF3"
    synonym = "HFE-143a"
    rhoc = unidades.Density(465)
    Tc = unidades.Temperature(377.921)
    Pc = unidades.Pressure(3635., "kPa")
    M = 100.0398  # g/mol
    Tt = unidades.Temperature(240)
    Tb = unidades.Temperature(249.572)
    f_acent = 0.289
    momentoDipolar = unidades.DipoleMoment(2.32, "Debye")
    id = 671
    # id = 1817
    
    CP1 = {"ao": 20.37,
           "an": [], "pow": [],
           "ao_exp": [0.2918, -1.950e-4, 4.650e-8],
           "exp": [1, 2, 3],
           "ao_hyp": [], "hyp": []}

    helmholtz1 = {
        "__type__": "Helmholtz",
        "__name__": "Helmholtz equation of state for RE143a of Akasaka and Kayukawa (2012)",
        "__doi__": {"autor": "Zhou, Y. and Lemmon, E.W.",
                    "title": "A fundamental equation of state for trifluoromethyl methyl ether (HFE-143m) and its application to refrigeration cycle analysis", 
                    "ref": "Int. J. Refrig., 35(4):1003-1013, 2012.",
                    "doi":  "10.1016/j.ijrefrig.2012.01.003"}, 
            
        "R": 8.314472,
        "cp": CP1,
        "ref": "NBP", 
        
        "Tmin": Tt, "Tmax": 420.0, "Pmax": 7200.0, "rhomax": 12.62, 
        "Pmin": 65.35, "rhomin": 12.62, 

        "nr1": [0.77715884e1, -0.87042750e1, -0.28095049, 0.14540153,
                0.92291277e-2],
        "d1": [1, 1, 1, 2, 5],
        "t1": [0.682, 0.851, 1.84, 1.87, 0.353],

        "nr2": [-0.2141651, 0.99475155e-1, 0.23247135e-1, -0.12873573e-1,
                -0.57366549e-1, 0.3650465, -0.25433763, -0.90896436e-1,
                0.83503619e-1, 0.15477603e-1, -0.16641941e-1, 0.52410163e-2],
        "d2": [1, 3, 5, 7, 1, 2, 2, 3, 4, 2, 3, 5],
        "t2": [3.92, 1.14, 0.104, 1.19, 6.58, 6.73, 7.99, 7.31, 7.45, 16.5,
               24.8, 10.5],
        "c2": [1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3],
        "gamma2": [1]*12}

    eq = helmholtz1,

    _vapor_Pressure = {
        "eq": 5,
        "ao": [-7.44314, 1.69164, -2.27778, -4.094],
        "exp": [1, 1.5, 2.5, 5]}
    _liquid_Density = {
        "eq": 1,
        "ao": [1.20552, 1.33568, 0.0981486, 0.248917],
        "exp": [0.33, 0.5, 1.5, 2.5]}
    _vapor_Density = {
        "eq": 3,
        "ao": [-3.02576, -6.97239, -20.2601, -53.4441],
        "exp": [0.38, 1.24, 3.2, 6.9]}
