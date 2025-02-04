#!/usr/bin/python
# -*- coding: utf-8 -*-

from lib.meos import MEoS
from lib import unidades


class R12(MEoS):
    """Multiparameter equation of state for R12"""
    name = "dichlorodifluoromethane"
    CASNumber = "75-69-4"
    formula = "CCl2F2"
    synonym = "R12"
    rhoc = unidades.Density(565.)
    Tc = unidades.Temperature(385.12)
    Pc = unidades.Pressure(4136.1, "kPa")
    M = 120.913  # g/mol
    Tt = unidades.Temperature(116.099)
    Tb = unidades.Temperature(243.398)
    f_acent = 0.17948
    momentoDipolar = unidades.DipoleMoment(0.510, "Debye")
    id = 216

    CP1 = {"ao": 4.003638529,
           "an": [], "pow": [],
           "ao_exp": [3.160638395, .3712598774, 3.562277099, 2.121533311],
           "exp": [1.4334342e3, 2.4300498e3, 6.8565952e2, 4.1241579e2],
           "ao_hyp": [], "hyp": []}

    helmholtz1 = {
        "__type__": "Helmholtz",
        "__name__": "Helmholtz equation of state for R-12 of Marx et al. (1992).",
        "__doi__": {"autor": "Marx, V., Pruss, A., and Wagner, W.",
                    "title": "Neue Zustandsgleichungen fuer R 12, R 22, R 11 und R 113. Beschreibung des thermodynamishchen Zustandsverhaltens bei Temperaturen bis 525 K und Druecken bis 200 MPa", 
                    "ref": "Duesseldorf: VDI Verlag, Series 19 (Waermetechnik/Kaeltetechnik), No. 57, 1992.",
                    "doi": ""}, 

        "R": 8.314471,
        "cp": CP1,
        
        "Tmin": Tt, "Tmax": 525.0, "Pmax": 200000.0, "rhomax": 15.13, 
        "Pmin": 0.000243, "rhomin": 15.1253, 

        "nr1": [0.2075343402e1, -0.2962525996e1, 0.1001589616e-1, 0.1781347612e-1,
                0.2556929157e-1, 0.2352142637e-2, -0.8495553314e-4],
        "d1": [1, 1, 1, 2, 4, 6, 8],
        "t1": [0.5, 1, 2, 2.5, -0.5, 0, 0],

        "nr2": [-0.1535945599e-1, -0.2108816776, -0.1654228806e-1,
                -0.1181316130e-1, -0.4160295830e-4, 0.2784861664e-4,
                0.1618686433e-5, -0.1064614686, 0.9369665207e-3,
                0.2590095447e-1, -0.4347025025e-1, 0.1012308449,
                -0.1100003438, -0.3361012009e-2, 0.3789190008e-3],
        "d2": [1, 1, 5, 7, 12, 12, 14, 1, 9, 1, 1, 3, 3, 5, 9],
        "t2": [-0.5, 1.5, 2.5, -0.5, 0, 0.5, -0.5, 4, 4, 2, 4, 12, 14, 0, 14],
        "c2": [1, 1, 1, 1, 1, 1, 1, 2, 2, 3, 3, 3, 3, 3, 4],
        "gamma2": [1]*15}

    helmholtz2 = {
        "__type__": "Helmholtz",
        "__name__": "short Helmholtz equation of state for R-12 of Span and Wagner (2003)",
        "__doi__": {"autor": "Span, R., Wagner, W.",
                    "title": "Equations of State for Technical Applications. III. Results for Polar Fluids", 
                    "ref": "Int. J. Thermophys., 24(1):111-162, 2003.",
                    "doi": "10.1023/A:1022362231796"}, 
        "__test__": """
            >>> st=R12(T=700, rho=200, eq=1)
            >>> print "%0.4f %0.3f %0.4f" % (st.cp0.kJkgK, st.P.MPa, st.cp.kJkgK)
            0.7421 11.552 1.1052
            >>> st2=R12(T=750, rho=100, eq=1)
            >>> print "%0.2f %0.5f" % (st2.h.kJkg-st.h.kJkg, st2.s.kJkgK-st.s.kJkgK)
            121.54 0.28621
            """, # Table III, Pag 117
            
        "R": 8.31451,
        "cp": CP1,
        
        "Tmin": 173.0, "Tmax": 600.0, "Pmax": 100000.0, "rhomax": 13.9, 
        "Pmin": 1.1633, "rhomin": 13.892, 

        "nr1": [0.10557228e1, -0.33312001e1, 0.10197244e1, 0.84155115e-1,
                0.28520742e-3],
        "d1": [1, 1, 1, 3, 7],
        "t1": [0.25, 1.25, 1.5, 0.25, 0.875],

        "nr2": [0.39625057, 0.63995721, -0.21423411e-1, -0.36249173,
                0.1934199e-2, -0.92993833e-1, -0.24876461e-1],
        "d2": [1, 2, 5, 1, 1, 4, 2],
        "t2": [2.375, 2, 2.125, 3.5, 6.5, 4.75, 12.5],
        "c2": [1, 1, 1, 2, 2, 2, 3],
        "gamma2": [1]*7}

    eq = helmholtz1, helmholtz2

    _surface = {"sigma": [-0.000124, 0.05662], "exp": [0.4318, 1.263]}
    _vapor_Pressure = {
        "eq": 5,
        "ao": [-0.70834e1, 0.43562e1, -0.35249e1, -0.28872e1, -0.89926],
        "exp": [1.0, 1.5, 1.67, 4.14, 10.0]}
    _liquid_Density = {
        "eq": 1,
        "ao": [0.32983e2, -0.10997e3, 0.17067e3, -0.13342e3, 0.42525e2],
        "exp": [0.57, 0.72, 0.89, 1.07, 1.25]}
    _vapor_Density = {
        "eq": 3,
        "ao": [-0.31530e1, -0.64734e1, -0.17346e2, -0.15918e2, -0.32492e2, -0.12072e3],
        "exp": [0.418, 1.32, 3.3, 6.6, 7.0, 15.0]}
