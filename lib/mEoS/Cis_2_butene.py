#!/usr/bin/python
# -*- coding: utf-8 -*-

from lib.meos import MEoS
from lib import unidades


class Cis_2_butene(MEoS):
    """Multiparameter equation of state for cis-butene"""
    name = "cis-butene"
    CASNumber = "590-18-1"
    formula = "CH3-CH=CH-CH3"
    synonym = ""
    rhoc = unidades.Density(238.11522208)
    Tc = unidades.Temperature(435.75)
    Pc = unidades.Pressure(4225.5, "kPa")
    M = 56.10632  # g/mol
    Tt = unidades.Temperature(134.3)
    Tb = unidades.Temperature(276.87)
    f_acent = 0.202
    momentoDipolar = unidades.DipoleMoment(0.3, "Debye")
    id = 25

    Fi1 = {"ao_log": [1, 2.9687],
           "pow": [0, 1],
           "ao_pow": [0.2591542, 2.4189888],
           "ao_exp": [3.2375, 7.0437, 11.414, 7.3722],
           "titao": [248/Tc, 1183/Tc, 2092/Tc, 4397/Tc]}

    helmholtz1 = {
        "__type__": "Helmholtz",
        "__name__": "short Helmholtz equation of state for cis-butene of Lemmon and Ihmels (2005)",
        "__doi__": {"autor": "Lemmon, E.W., Ihmels, E.C.",
                    "title": "Thermodynamic properties of the butenes: Part II. Short fundamental equations of state", 
                    "ref": "Fluid Phase Equilibria 228 – 229 (2004), 173 – 187.",
                    "doi":  "10.1016/j.fluid.2004.09.004"}, 
        "__test__": """
            >>> st=Cis_2_butene(T=350, rho=0)
            >>> print "%0.0f %0.1f %0.1f %0.5g %0.5g %0.5g %0.5g" % (st.T, st.rhoM, st.P.MPa, st.hM.kJkmol, st.cvM.kJkmolK, st.cpM.kJkmolK, st.w)
            350 0.0 0.0 29735 83.593 91.907 238.8
            >>> st=Cis_2_butene(T=350, rho=0.3*56.10632)
            >>> print "%0.0f %0.1f %.5g %.5g %0.5g %0.5g %0.5g %0.5g" % (st.T, st.rhoM, st.P.MPa, st.hM.kJkmol, st.sM.kJkmolK, st.cvM.kJkmolK, st.cpM.kJkmolK, st.w)
            350 0.3 0.74661 28294 84.888 89.258 106.34 209.87
            >>> st=Cis_2_butene(T=350, rho=10*56.10632)
            >>> print "%0.0f %0.1f %.5g %.5g %0.5g %0.5g %0.5g %0.5g" % (st.T, st.rhoM, st.P.MPa, st.hM.kJkmol, st.sM.kJkmolK, st.cvM.kJkmolK, st.cpM.kJkmolK, st.w)
            350 10.0 5.8051 9632.7 29.1 93.935 138.23 770.1
            >>> st=Cis_2_butene(T=440, rho=4*56.10632)
            >>> print "%0.0f %0.1f %.5g %.5g %0.5g %0.5g %0.5g %0.5g" % (st.T, st.rhoM, st.P.MPa, st.hM.kJkmol, st.sM.kJkmolK, st.cvM.kJkmolK, st.cpM.kJkmolK, st.w)
            440 4.0 4.5067 28321 75.755 126 1686.3 130.71
            """, # Table 9, Pag 186

        "R": 8.314472,
        "cp": Fi1,
        "ref": "NBP", 

        "Tmin": Tt, "Tmax": 525., "Pmax": 50000.0, "rhomax": 14.09, 
        "Pmin": 0.00026, "rhomin": 14.09, 

        "nr1":  [0.77827, -2.8064, 1.003, 0.013762, 0.085514, 0.00021268],
        "d1": [1, 1, 1, 2, 3, 7],
        "t1": [0.12, 1.3, 1.74, 2.1, 0.28, 0.69],

        "nr2": [0.22962, -0.072442, -0.23722, -0.074071, -0.026547, 0.012032],
        "d2": [2, 5, 1, 4, 3, 4],
        "t2": [0.75, 2., 4.4, 4.7, 15., 14.],
        "c2": [1, 1, 2, 2, 3, 3],
        "gamma2": [1]*6}

    eq = helmholtz1,

    _vapor_Pressure = {
        "eq": 5,
        "ao": [-0.70022e1, 0.13695e1, -0.30509e1, 0.10012, -0.15577e1],
        "exp": [1.0, 1.5, 3.2, 3.46, 6.4]}
    _liquid_Density = {
        "eq": 1,
        "ao": [0.46849e1, -0.54614e1, 0.34718e1, 0.50511e1, -0.50389e1],
        "exp": [0.402, 0.54, 0.69, 6.6, 7.0]}
    _vapor_Density = {
        "eq": 3,
        "ao": [-0.28918e1, -0.58582e1, -0.17443e2, -0.24566e2, -0.29413e2,
               -0.11392e3],
        "exp": [0.4098, 1.174, 3.11, 6.1, 7.6, 14.8]}
