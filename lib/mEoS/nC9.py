#!/usr/bin/python
# -*- coding: utf-8 -*-

from lib.meos import MEoS
from lib import unidades


class nC9(MEoS):
    """Multiparameter equation of state for n-nonane"""
    name = "nonane"
    CASNumber = "111-84-2"
    formula = "CH3-(CH2)7-CH3"
    synonym = ""
    rhoc = unidades.Density(232.1417)
    Tc = unidades.Temperature(594.55)
    Pc = unidades.Pressure(2281.0, "kPa")
    M = 128.2551  # g/mol
    Tt = unidades.Temperature(219.7)
    Tb = unidades.Temperature(423.91)
    f_acent = 0.4433
    momentoDipolar = unidades.DipoleMoment(0.07, "Debye")
    id = 13

    Fi1 = {"ao_log": [1, 16.349],
           "pow": [0, 1],
           "ao_pow": [10.7927224829, -8.2418318753],
           "ao_exp": [24.926, 24.842, 11.188, 17.483],
           "titao": [1221/Tc, 2244/Tc, 5008/Tc, 11724/Tc]}
           
    Fi2 = {"ao_log": [1, 3.0],
           "pow": [0, 1],
           "ao_pow": [16.313913248, -102.160247463],
           "ao_exp": [], "titao": [], 
           "ao_hyp": [18.0241, 38.1235, 53.3415, 0],
           "hyp": [0.263819696, 1.370586158, 2.848860483, 0]}

    helmholtz1 = {
        "__type__": "Helmholtz",
        "__name__": "short Helmholtz equation of state for nonane of Lemmon and Span (2006)",
        "__doi__": {"autor": "Lemmon, E.W., Span, R.",
                    "title": "Short Fundamental Equations of State for 20 Industrial Fluids", 
                    "ref": "J. Chem. Eng. Data, 2006, 51 (3), pp 785–850",
                    "doi":  "10.1021/je050186n"}, 
        "__test__": """
            >>> st=nC9(T=596, rho=128.2551)
            >>> print "%0.0f %0.0f %0.3f %0.3f %0.3f %0.3f %0.3f %0.3f" % (st.T, st.rhoM, st.P.kPa, st.hM.kJkmol, st.sM.kJkmolK, st.cvM.kJkmolK, st.cpM.kJkmolK, st.w)
            596 1 2200.687 81692.218 156.217 379.897 715.553 85.318
            """, # Table 10, Pag 842
            
        "R": 8.314472,
        "cp": Fi1,
        "ref": "NBP", 

        "Tmin": Tt, "Tmax": 600.0, "Pmax": 800000.0, "rhomax": 6.06, 
        "Pmin": 0.00044, "rhomin": 6.05, 

        "nr1": [1.1151, -2.7020, 0.83416, -0.38828, 0.1376, 0.00028185],
        "d1": [1, 1, 1, 2, 3, 7],
        "t1": [0.25, 1.125, 1.5, 1.375, 0.25, 0.875],

        "nr2": [0.62037, 0.015847, -0.61726, -0.15043, -0.012982, 0.0044325],
        "d2": [2, 5, 1, 4, 3, 4],
        "t2": [0.625, 1.75, 3.625, 3.625, 14.5, 12.],
        "c2": [1, 1, 2, 2, 3, 3],
        "gamma2": [1]*6}

    GERG = {
        "__type__": "Helmholtz",
        "__name__": "Helmholtz equation of state for propane of Kunz and Wagner (2008).",
        "__doi__": {"autor": "Kunz, O., Wagner, W.",
                    "title": "The GERG-2008 Wide-Range Equation of State for Natural Gases and Other Mixtures: An Expansion of GERG-2004", 
                    "ref": "J. Chem. Eng. Data, 2012, 57 (11), pp 3032-3091",
                    "doi":  "10.1021/je300655b"}, 
        "R": 8.314472,
        "cp": Fi2,
        "ref": "OTO", 

        "Tmin": Tt, "Tmax": 600.0, "Pmax": 800000.0, "rhomax": 6.06, 
        "Pmin": 0.00044, "rhomin": 6.05, 

        "nr1": [0.11151e1, -0.27020e1, 0.83416, -0.38828, 0.13760, 0.28185e-3],
        "d1": [1, 1, 1, 2, 3, 7],
        "t1": [0.25, 1.125, 1.5, 1.375, 0.25, 0.875],

        "nr2": [0.62037, 0.15847e-1, -0.61726, -0.15043, -0.12982e-1, 0.44325e-2],
        "d2": [2, 5, 1, 4, 3, 4],
        "t2": [0.625, 1.75, 3.625, 3.625, 14.5, 12.],
        "c2": [1, 1, 2, 2, 3, 3],
        "gamma2": [1]*6}

    eq = helmholtz1, GERG

    _surface = {"sigma": [0.053388], "exp": [1.262]}
    _dielectric = {"eq": 3, "Tref": 273.16, "rhoref": 1000.,
                   "a0": [0.10924],  "expt0": [-1.], "expd0": [1.],
                   "a1": [44.53, 0.045], "expt1": [0, 1], "expd1": [1, 1],
                   "a2": [286.27, 529.31, -83471, -90493],
                   "expt2": [0, 1, 0, 1], "expd2": [2, 2, 3, 3]}
    _vapor_Pressure = {
        "eq": 5,
        "ao": [-0.84804e1, 0.28640e1, -0.37414e1, -0.57479e1, 0.18799e1],
        "exp": [1.0, 1.5, 2.3, 4.6, 5.0]}
    _liquid_Density = {
        "eq": 1,
        "ao": [-0.43785, 0.37240e1, -0.23029e1, 0.18270e1, 0.38664],
        "exp": [0.116, 0.32, 0.54, 0.8, 3.5]}
    _vapor_Density = {
        "eq": 3,
        "ao": [-0.33199e1, -0.23900e1, -0.15307e2, -0.51788e2, -0.11133e3],
        "exp": [0.461, 0.666, 2.12, 5.1, 11.0]}

    visco0 = {"eq": 1, "omega": 1,
              "collision": [0.340344, -0.466455],
              "__name__": "Huber (2004)",
              "__doi__": {"autor": "Huber, M.L., Laesecke, A. and Xiang, H.W.",
                        "title": "Viscosity correlations for minor constituent fluids in natural gas: n-octane, n-nonane and n-decane", 
                        "ref": "Fluid Phase Equilibria 224(2004)263-270.",
                        "doi": "10.1016/j.fluid.2004.07.012"}, 
              "__test__": """
                  >>> st=nC9(T=300, rhom=5.6191)
                  >>> print "%0.2f" % st.mu.muPas
                  709.53
                  """, # Section 3.2 pag 267

            "ek": 472.12, "sigma": 0.66383,
              "Tref": 1, "rhoref": 1.*M,
              "n_chapman": 0.2418675/M**0.5,

              "n_virial": [-0.19572881e2, 0.21973999e3, -0.10153226e4,
                           0.24710125e4, -0.33751717e4, 0.24916597e4,
                           -0.78726086e3, 0.14085455e2, -0.34664158],
              "t_virial": [0.0, -0.25, -0.5, -0.75, -1, -1.25, -1.5, -2.5, -5.5],
              "Tref_virial": 472.12, "etaref_virial": 0.1761657,

              "Tref_res": 594.55, "rhoref_res": 1.81*M, "etaref_res": 1000,
              "n_packed": [2.66987, 1.32137, 0],
              "t_packed": [0, 0.5, 1],
              "n_poly": [-0.314367e-1, 0.639384e-2, 0.326258e-1, -0.108922e-1,
                         -0.192935],
              "t_poly": [-1, -1, -2, -2, 0],
              "d_poly": [2, 3, 2, 3, 1],
              "g_poly": [0, 0, 0, 0, -1],
              "c_poly": [0, 0, 0, 0, 0],
              "n_num": [0.192935],
              "t_num": [0],
              "d_num": [1],
              "g_num": [0],
              "c_num": [0],
              "n_den": [1, -1],
              "t_den": [0, 0],
              "d_den": [0, 1],
              "g_den": [1, 0],
              "c_den": [0, 0]}

    _viscosity = visco0,

    thermo0 = {"eq": 1,
               "__name__": "Huber (2005)",
              "__doi__": {"autor": "Huber, M.L. and Perkins, R.A.",
                        "title": "Thermal conductivity correlations for minor constituent fluids in natural gas: n-octane, n-nonane and n-decane", 
                        "ref": "Fluid Phase Equilibria 227 (2005) 47-55",
                        "doi": "10.1016/j.fluid.2004.10.031"}, 
               "__test__": """
                   >>> st=nC9(T=300, rhom=5.6194)
                   >>> print "%0.2f" % st.k
                   130.31
                   """, # Section 3.2 pag 53

               "Tref": 594.55, "kref": 1,
               "no": [0.878765e-2, -0.413510e-1, 0.104791, -0.320032e-1],
               "co": [0, 1, 2, 3],

               "Trefb": 594.55, "rhorefb": 1.81, "krefb": 1,
               "nb": [0.490088e-2, 0.996486e-2, -0.807305e-2, 0.0, 0.557431e-2,
                      0.0, 0.0, 0.0, 0.0, 0.0],
               "tb": [0, 1]*5,
               "db": [1, 1, 2, 2, 3, 3, 4, 4, 5, 5],
               "cb": [0]*10,

               "critical": 3,
               "gnu": 0.63, "gamma": 1.239, "R0": 1.03,
               "Xio": 0.194e-9, "gam0": 0.0496, "qd": 1.043054e-9, "Tcref": 891.825}

    _thermal = thermo0,
