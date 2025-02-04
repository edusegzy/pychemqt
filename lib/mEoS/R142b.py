#!/usr/bin/python
# -*- coding: utf-8 -*-

from lib.meos import MEoS
from lib import unidades


class R142b(MEoS):
    """Multiparameter equation of state for R142b"""
    name = "1-chloro-1,1-difluoroethane"
    CASNumber = "75-68-3"
    formula = "CClF2CH3"
    synonym = "R142b"
    rhoc = unidades.Density(445.997)
    Tc = unidades.Temperature(410.26)
    Pc = unidades.Pressure(4055.0, "kPa")
    M = 100.49503  # g/mol
    Tt = unidades.Temperature(142.72)
    Tb = unidades.Temperature(264.03)
    f_acent = 0.2321
    momentoDipolar = unidades.DipoleMoment(2.14, "Debye")
    id = 241

    Fi1 = {"ao_log": [1, 3.],
           "pow": [0, 1],
           "ao_pow": [-12.6016527149, 8.3160183265],
           "ao_exp": [5.0385, 6.8356, 4.0591, 2.8136],
           "titao": [473/Tc, 1256/Tc, 2497/Tc, 6840/Tc]}
           
    helmholtz1 = {
        "__type__": "Helmholtz",
        "__name__": "short Helmholtz equation of state for R-142b of Lemmon and Span (2006)",
        "__doi__": {"autor": "Lemmon, E.W., Span, R.",
                    "title": "Short Fundamental Equations of State for 20 Industrial Fluids", 
                    "ref": "J. Chem. Eng. Data, 2006, 51 (3), pp 785–850",
                    "doi":  "10.1021/je050186n"}, 
        "__test__": """
            >>> st=R142b(T=412, rho=4*100.49503)
            >>> print "%0.0f %0.0f %0.3f %0.3f %0.3f %0.3f %0.3f %0.3f" % (st.T, st.rhoM, st.P.kPa, st.hM.kJkmol, st.sM.kJkmolK, st.cvM.kJkmolK, st.cpM.kJkmolK, st.w)
            412 4 4165.653 44982.401 170.029 117.705 3187.213 96.468
            """, # Table 10, Pag 842
            
        "R": 8.314472,
        "cp": Fi1,
        "ref": "NBP", 
        
        "Tmin": Tt, "Tmax": 470.0, "Pmax": 60000.0, "rhomax": 14.44, 
        "Pmin": 0.00363, "rhomin": 14.44, 

        "nr1": [1.0038, -2.7662, 0.42921, 0.081363, 0.00024174],
        "d1": [1, 1, 1, 3, 7],
        "t1": [0.25, 1.25, 1.5, 0.25, 0.875],

        "nr2": [0.48246, 0.75542, -0.007430, -0.41460, -0.016558, -0.10644,
                -0.021704],
        "d2": [1, 2, 5, 1, 1, 4, 2],
        "t2": [2.375, 2, 2.125, 3.5, 6.5, 4.75, 12.5],
        "c2": [1, 1, 1, 2, 2, 2, 3],
        "gamma2": [1]*7}

    eq = helmholtz1,

    _surface = {"sigma": [0.05685], "exp": [1.237]}
    _vapor_Pressure = {
        "eq": 5,
        "ao": [-0.73074e1, 0.23186e1, -0.23278e1, -0.32761e1, 0.42103],
        "exp": [1.0, 1.5, 2.2, 4.8, 6.2]}
    _liquid_Density = {
        "eq": 1,
        "ao": [0.17162e2, -0.47495e2, 0.57171e2, -0.25404e2, 0.15855e1],
        "exp": [0.53, 0.71, 0.9, 1.1, 2.3]}
    _vapor_Density = {
        "eq": 3,
        "ao": [-.3146e1, -.65221e1, -.18006e2, -.46694e2, -.26087e1, -.1102e3],
        "exp": [0.408, 1.28, 3.2, 6.6, 7.0, 14.0]}
