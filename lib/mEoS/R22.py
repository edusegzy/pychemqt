#!/usr/bin/python
# -*- coding: utf-8 -*-

from lib.meos import MEoS
from lib import unidades


class R22(MEoS):
    """Multiparameter equation of state for R22"""
    name = "chlorodifluoromethane"
    CASNumber = "75-45-6"
    formula = "CHClF2"
    synonym = "R22"
    rhoc = unidades.Density(523.8422)
    Tc = unidades.Temperature(369.295)
    Pc = unidades.Pressure(4990., "kPa")
    M = 86.468  # g/mol
    Tt = unidades.Temperature(115.73)
    Tb = unidades.Temperature(232.340)
    f_acent = 0.22082
    momentoDipolar = unidades.DipoleMoment(1.458, "Debye")
    id = 220

    CP1 = {"ao": 4.00526140446,
           "an": [1.20662553e-4], "pow": [1],
           "ao_exp": [1]*9,
           "exp": [4352.3095, 1935.1591, 1887.67936, 1694.88284, 1605.67848,
                   1162.53424, 857.51288, 605.72638, 530.90982],
           "ao_hyp": [], "hyp": []}

    Fi2 = {"ao_log": [1, 3.00671581],
           "pow": [0, 1],
           "ao_pow": [-11.8829672, 8.09247802],
           "ao_exp": [3.9321463, 1.10074668, 1.87129085, 2.22706659],
           "titao": [4.82421333, 11.392964, 2.82862148, 1.55580861]}

    helmholtz1 = {
        "__type__": "Helmholtz",
        "__name__": "Helmholtz equation of state for R-22 of Kamei et al. (1995)",
        "__doi__": {"autor": "Kamei, A., Beyerlein, S.W., and Jacobsen, R.T.",
                    "title": "Application of nonlinear regression in the development of a wide range formulation for HCFC-22", 
                    "ref": "Int. J. Thermophysics, 16:1155-1164, 1995.",
                    "doi": "10.1007/BF02081283"}, 

        "R": 8.31451,
        "cp": CP1,
        "ref": "IIR", 
        
        "Tmin": Tt, "Tmax": 550.0, "Pmax": 60000.0, "rhomax": 19.91, 
        "Pmin": 0.0003793, "rhomin": 19.907, 

        "nr1": [0.695645445236e-1, 0.252275419999e2, -0.202351148311e3,
                0.350063090302e3, -0.223134648863e3, 0.488345904592e2,
                0.108874958556e-1, 0.590315073614, -0.689043767432,
                0.284224445844, 0.125436457897, -0.113338666416e-1,
                -0.631388959170e-1, 0.974021015232e-2, -0.408406844722e-3,
                0.741948773570e-3, 0.315912525922e-3, 0.876009723338e-5,
                -0.110343340301e-3, -0.705323356879e-4],
        "d1": [1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 3, 3, 4, 5, 6, 7, 7, 7, 8, 8],
        "t1": [-1, 1.75, 2.25, 2.5, 2.75, 3, 5.5, 1.5, 1.75, 3.5, 1, 4.5, 1.5,
               0.5, 4.5, 1, 4, 5, -0.5, 3.5],

        "nr2": [0.235850731510, -0.192640494729, 0.375218008557e-2,
                -0.448926036678e-4, 0.198120520635e-1, -0.356958425255e-1,
                0.319594161562e-1, 0.260284291078e-5, -0.897629021967e-2,
                0.345482791645e-1, -0.411831711251e-2, 0.567428536529e-2,
                -0.563368989908e-2, 0.191384919423e-2, -0.178930036389e-2],
        "d2": [2, 2, 2, 2, 3, 4, 4, 4, 4, 6, 6, 6, 8, 8, 8],
        "t2": [5, 7, 12, 15, 3.5, 3.5, 8, 15, 25, 3, 9, 19, 2, 7, 13],
        "c2": [2, 2, 2, 2, 3, 2, 2, 2, 4, 2, 2, 4, 2, 2, 4],
        "gamma2": [1]*15}

    helmholtz2 = {
        "__type__": "Helmholtz",
        "__name__": "Helmholtz equation of state for R-22 of Wagner et al. (1993)",
        "__doi__": {"autor": "Wagner, W., Marx, V., and Pruss, A.",
                    "title": "A New Equation of State for Chlorodifluoromethane (R22) Covering the Entire Fluid Region from 116 K to 550 K at Pressures up to 200 MPa", 
                    "ref": "Int. J. Refrig., 16(6):373-389, 1993.",
                    "doi": "10.1016/0140-7007(93)90055-D"}, 

        "__test__":
            """
            >>> st=R22(T=273.15, P=1e6, eq=1)
            >>> print "%0.2f %0.5f %0.5f %0.5f %0.5f %0.5f %0.5f %0.5f %0.5f" % ( \
                st.T, st.rho, st.cv.kJkgK, st.cp.kJkgK, st.w, st.h.kJkg, \
                st.s.kJkgK, st.u.kJkg, st.joule.KMPa)
            273.15 1283.58841 0.67801 1.17239 665.35405 200.10557 0.99895 199.32650 -0.18190
            >>> st=R22(T=373.15, P=1e6, eq=1)
            >>> print "%0.2f %0.5f %0.5f %0.5f %0.5f %0.5f %0.5f %0.5f %0.5f" % ( \
                st.T, st.rho, st.cv.kJkgK, st.cp.kJkgK, st.w, st.h.kJkg, \
                st.s.kJkgK, st.u.kJkg, st.joule.KMPa)
            323.15 36.58815 0.62447 0.79727 173.92097 434.49209 1.79016 407.16083 18.34747
            """, 
            
        "R": 8.31451,
        "cp": Fi2,
        "ref": "IIR", 
        
        "Tref": 369.28, "rhoref": 520, 
        
        "Tmin": Tt, "Tmax": 550.0, "Pmax": 60000.0, "rhomax": 19.91, 
        "Pmin": 0.00036783, "rhomin": 19.907, 

        "nr1": [0.29599201810, -0.1151392173e1, 0.5259746924, -0.6644393736,
                .1723481086, -.1158525163e-3, .3803104348e-3, .4119291557e-5],
        "d1": [1, 1, 2, 2, 2, 5, 7, 8],
        "t1": [0, 1.5, 0, 0.5, 1.5, 3, 0, 2.5],

        "nr2": [-0.2267374456, 0.1433024764e-1, -0.1392978451, -0.1172221416,
                0.2003394173, -0.2097857448, 0.1284497611e-1, 0.1724693488e-2,
                -0.5663447308e-3, 0.1485459957e-4, -0.5691734346e-3,
                0.8341057068e-2, -0.2526287501e-1, 0.1185506149e-2],
        "d2": [1, 3, 4, 5, 5, 1, 1, 9, 10, 12, 1, 3, 3, 6],
        "t2": [2.5, 3.5, 1.5, -0.5, 0, 4, 6, 4, 2, 2, 12, 15, 18, 36],
        "c2": [1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 4],
        "gamma2": [1]*17}

    helmholtz3 = {
        "__type__": "Helmholtz",
        "__name__": "short Helmholtz equation of state for R-22 of Span and Wagner (2003).",
        "__doi__": {"autor": "Span, R., Wagner, W.",
                    "title": "Equations of State for Technical Applications. III. Results for Polar Fluids", 
                    "ref": "Int. J. Thermophys., 24(1):111-162, 2003.",
                    "doi": "10.1023/A:1022362231796"}, 
        "__test__": """
            >>> st=R22(T=700, rho=200, eq=2)
            >>> print "%0.4f %0.3f %0.4f" % (st.cp0.kJkgK, st.P.MPa, st.cp.kJkgK)
            0.8498 17.202 1.3137
            >>> st2=R22(T=750, rho=100, eq=2)
            >>> print "%0.2f %0.5f" % (st2.h.kJkg-st.h.kJkg, st2.s.kJkgK-st.s.kJkgK)
            151.95 0.37335
            """, # Table III, Pag 117
            
        "R": 8.31451,
        "cp": Fi2,
        "ref": "IIR", 
        
        "Tmin": Tt, "Tmax": 600.0, "Pmax": 100000.0, "rhomax": 20.0, 
        "Pmin": 0.00036704, "rhomin": 19.976, 

        "nr1": [.96268924, -.25275103e1, .31308745, .72432837e-1, .21930233e-3],
        "d1": [1, 1, 1, 3, 7],
        "t1": [0.25, 1.25, 1.5, 0.25, 0.875],

        "nr2": [0.33294864, 0.63201229, -0.32787841e-2, -0.33680834,
                -0.22749022e-1, -0.87867308e-1, -0.21108145e-1],
        "d2": [1, 2, 5, 1, 1, 4, 2],
        "t2": [2.375, 2, 2.125, 3.5, 6.5, 4.75, 12.5],
        "c2": [1, 1, 1, 2, 2, 2, 3],
        "gamma2": [1]*7}

    eq = helmholtz1, helmholtz2, helmholtz3

    _surface = {"sigma": [3.0587, -2.99856], "exp": [1.41809, 1.42291]}
    _vapor_Pressure = {
        "eq": 5,
        "ao": [-0.70780e1, 0.17211e1, -0.16379e1, -0.37952e1, 0.86937],
        "exp": [1.0, 1.5, 2.2, 4.8, 6.2]}
    _liquid_Density = {
        "eq": 1,
        "ao": [0.18762e1, 0.68216, 0.41342e-1, 0.22589, 0.15407],
        "exp": [0.345, 0.74, 1.2, 2.6, 7.2]}
    _vapor_Density = {
        "eq": 3,
        "ao": [-.23231e1, -.59231e1, -.16331e2, -.49343e2, -.25662e2, -.89335e2],
        "exp": [0.353, 1.06, 2.9, 6.4, 12.0, 15.0]}
