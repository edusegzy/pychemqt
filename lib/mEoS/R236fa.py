#!/usr/bin/python
# -*- coding: utf-8 -*-

from lib.meos import MEoS
from lib import unidades


class R236fa(MEoS):
    """Multiparameter equation of state for R236fa"""
    name = "1,1,1,3,3,3-hexafluoropropane"
    CASNumber = "690-39-1"
    formula = "CF3CH2CF3"
    synonym = "R236fa"
    rhoc = unidades.Density(551.2912384)
    Tc = unidades.Temperature(398.07)
    Pc = unidades.Pressure(3200.0, "kPa")
    M = 152.0384  # g/mol
    Tt = unidades.Temperature(179.6)
    Tb = unidades.Temperature(271.66)
    f_acent = 0.377
    momentoDipolar = unidades.DipoleMoment(1.982, "Debye")
    id = 671
    # id = 1873

    Fi1 = {"ao_log": [1, 9.175],
           "pow": [0, 1],
           "ao_pow": [-17.5983849, 8.87150449],
           "ao_exp": [9.8782, 18.236, 49.934],
           "titao": [962/Tc, 2394/Tc, 5188/Tc]}

    CP1 = {"ao": 53.4662555,
           "an": [1, 2], "pow": [0.228092134, 0.352999168e-4],
           "ao_exp": [], "exp": [],
           "ao_hyp": [], "hyp": []}

    helmholtz1 = {
        "__type__": "Helmholtz",
        "__name__": "Helmholtz equation of state for R236fa of Pan et al. (2012).",
        "__doi__": {"autor": "Pan, J., Rui, X., Zhao, X., Qiu, L.",
                    "title": "An equation of state for the thermodynamic properties of 1,1,1,3,3,3-hexafluoropropane (HFC-236fa)", 
                    "ref": "Fluid Phase Equilib., 321:10-16, 2012",
                    "doi": "10.1016/j.fluid.2012.02.012"}, 
                    
        "R": 8.314472,
        "cp": Fi1,
        "ref": {"Tref": 273.15, "Pref": 1, "ho": 54932.8947, "so": 280.341948}, 
        
        "Tmin": Tt, "Tmax": 400.0, "Pmax": 70000.0, "rhomax": 11.235, 
        "Pmin": 0.1603, "rhomin": 11.235, 

        "nr1": [0.04453255, 1.777017, -2.230519, -0.6708606, 0.1587907],
        "d1": [4, 1, 1, 2, 3],
        "t1": [1.07, 0.222, 0.66, 1.33, 0.227],

        "nr2": [-1.425119, -0.6461628, 0.8469985, -0.5635356, -0.01535611],
        "d2": [1, 3, 2, 2, 7],
        "t2": [2.33, 1.94, 1.53, 2.65, 0.722],
        "c2": [2, 2, 1, 2, 1],
        "gamma2": [1]*5,

        "nr3": [1.156362, -0.407031, -0.2172753, -1.007176, -0.00006902909],
        "d3": [1, 1, 3, 3, 2],
        "t3": [1.11, 2.31, 3.68, 4.23, 0.614],
        "alfa3": [1.02, 1.336, 1.055, 5.84, 16.2],
        "beta3": [1.42, 2.31, 0.89, 80, 108],
        "gamma3": [1.13, 0.67, 0.46, 1.28, 1.2],
        "epsilon3": [0.712, 0.91, 0.677, 0.718, 1.64]}

    MBWR = {
        "__type__": "MBWR",
        "__name__": "MBWR equation of state for R-236fa of Outcalt and McLinden (1995).",
        "__doi__": {"autor": "Outcalt, S.L. and McLinden, M.O.",
                    "title": "An equation of state for the thermodynamic properties of R236fa", 
                    "ref": "NIST report to sponsor (U.S. Navy, David Taylor Model Basin) under contract N61533-94-F-0152, 1995.",
                    "doi": ""}, 
                    
        "R": 8.314471,
        "cp": CP1,
        
        "Tmin": Tt, "Tmax": 500.0, "Pmax": 40000.0, "rhomax": 11.30, 
        "Pmin": 0.162, "rhomin": 11.29, 

        "b": [None, -0.661121874831e-1, 0.861763902745e1, -0.233732255968e3,
              0.437486232843e5, -0.539677761508e7, -0.757588552002e-2,
              0.107379563512e2, -0.106626588551e5, -0.103047455432e6,
              -0.194868091617e-2, 0.438365228107e1, -0.111207843880e4,
              -0.263710051508, 0.477521163113e2, 0.197804035098e4,
              -0.485710898935e1, 0.144821196401, -0.221059322936e2,
              0.926270169913, 0.577920666161e7, -0.985511065626e9,
              0.197199808018e6, 0.319420123094e10, 0.792946107314e4,
              -0.693606295610e6, 0.849836259084e2, 0.209702051124e7,
              0.110600369167e1, 0.953714711849e2, -0.881815206562e-2,
              0.973194908842e1, -0.935516922205e3]}

    eq = MBWR,

    _surface = {"sigma": [0.05389], "exp": [1.249]}
    _vapor_Pressure = {
        "eq": 5,
        "ao": [-0.78785e1, 0.15884e1, -0.48864e1, -0.50273e1, 0.89900e1],
        "exp": [1.0, 1.5, 3.1, 8.0, 10.0]}
    _liquid_Density = {
        "eq": 1,
        "ao": [0.12320e2, -0.27579e2, 0.40114e2, -0.35461e2, 0.13769e2],
        "exp": [0.579, 0.77, 0.97, 1.17, 1.4]}
    _vapor_Density = {
        "eq": 3,
        "ao": [-.44507e1, -.37583e1, -.20279e2, -.26801e3, .50171e3, -.34917e3],
        "exp": [0.506, 1.16, 2.8, 7.0, 8.0, 9.0]}
