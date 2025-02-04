#!/usr/bin/python
# -*- coding: utf-8 -*-

from lib.meos import MEoS
from lib import unidades


class RE245fa2(MEoS):
    """Multiparameter equation of state for RE245fa2"""
    name = "2,2,2-trifluoroethyl-difluoromethyl-ether"
    CASNumber = "1885-48-9"
    formula = "CHF2OCH2CF3"
    synonym = "HFE-245fa2"
    rhoc = unidades.Density(515.001169364688)
    Tc = unidades.Temperature(444.88)
    Pc = unidades.Pressure(3433., "kPa")
    M = 150.047336  # g/mol
    Tt = unidades.Temperature(250)
    Tb = unidades.Temperature(302.4)
    f_acent = 0.387
    momentoDipolar = unidades.DipoleMoment(1.631, "Debye")
    id = 671
    # id = 1817
    
    CP1 = {"ao": 5.259865,
           "an": [], "pow": [],
           "ao_exp": [], "exp": [],
           "ao_hyp": [12.12843, 13.25677, 0.521867, 0],
           "hyp": [486, 1762, 7631, 0]}

    helmholtz1 = {
        "__type__": "Helmholtz",
        "__name__": "Helmholtz equation of state for RE245fa2 of Zhou et al. (2012)",
        "__doi__": {"autor": "Zhou, Y. and Lemmon, E.W.",
                    "title": "preliminary equation, 2012.", 
                    "ref": "",
                    "doi":  ""}, 
            
        "R": 8.314472,
        "cp": CP1,
        "ref": "NBP", 
        
        "Tmin": Tt, "Tmax": 500.0, "Pmax": 400000.0, "rhomax": 10.02, 
        "Pmin": 8.272, "rhomin": 10., 

        "nr1": [0.47771378e-1, 0.15745383e1, -0.24763491e1, -0.49414564,
                0.19380498],
        "d1": [4, 1, 1, 2, 3],
        "t1": [1, 0.32, 0.91, 1.265, 0.4266],

        "nr2": [-0.97863158, -0.42660297, 0.85352583, -0.53380114,
                -0.29780036e-1],
        "d2": [1, 3, 2, 2, 7],
        "t2": [2.24, 1.64, 1.65, 3.28, 0.855],
        "c2": [2, 2, 1, 2, 1],
        "gamma2": [1]*5,

        "nr3": [0.97659111, -0.33121365, -0.14122591, -0.15312295e2],
        "d3": [1, 1, 3, 3],
        "t3": [1.227, 3.0, 4.3, 2.5],
        "alfa3": [1.005, 1.515, 1.156, 17.7],
        "beta3": [2, 3.42, 1.37, 471],
        "gamma3": [1.084, 0.72, 0.49, 1.152],
        "epsilon3": [0.723, 0.9488, 0.818, 0.891]}

    eq = helmholtz1,

    _vapor_Pressure = {
        "eq": 5,
        "ao": [-8.9235, 10.527, -23.058, 30.291, -20.913, -26.745],
        "exp": [1, 1.5, 1.9, 2.4, 2.9, 3.2]}
    _liquid_Density = {
        "eq": 1,
        "ao": [1.2479, 5.5732, -12.26, 13.964, -6.0384],
        "exp": [0.34, 0.75, 1.2, 1.7, 2.3]}
    _vapor_Density = {
        "eq": 3,
        "ao": [-0.667, -5.8238, -26.927, 21.574, -65.645],
        "exp": [0.28, 0.66, 2.6, 3.5, 5.2]}

    visco0 = {"eq": 5, "omega": 3,
              "__doi__": {"autor": "T-H. Chung, Ajlan, M., Lee, L.L. and Starling, K.E",
                          "title": "Generalized Multiparameter Correlation for Nonpolar and Polar Fluid Transport Properties", 
                          "ref": "Ind. Eng. Chem. Res., 1988, 27 (4), pp 671–679",
                          "doi": "10.1021/ie00076a024"}, 
              "__name__": "Chung (1988)",
              "w": 0.387, "mur": 0.0, "k": 0.0}

    _viscosity = visco0,
