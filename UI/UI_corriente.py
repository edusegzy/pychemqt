#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from math import exp, log
import sqlite3
from ConfigParser import ConfigParser
from functools import partial

from PyQt4 import QtCore, QtGui
from scipy.constants import lb
from numpy import all
from scipy.special import erf

from tools import UI_databank
from tools.UI_psychrometry import PsychroInput
from lib.corriente import Corriente, Mezcla, Solid, PsyStream
from lib.psycrometry import PsychroState, PsyState
from lib import unidades, config
from lib.utilities import representacion
from lib.thread import Evaluate
from UI import texteditor
from UI.delegate import CellEditor
from UI.widgets import Tabla, Entrada_con_unidades, Status
    

###Estándares de filtros, unidades en mm
Tyler=[0.033, 0.043, 0.053, 0.061, 0.074, 0.088, 0.104, 0.121, 0.147, 0.173, 0.208, 0.246, 0.295, 0.351, 0.417, 0.495, 0.589, 0.701, 0.833, 0.991, 1.168, 1.397, 1.651, 1.981, 2.362, 2.794, 3.327, 3.962, 4.699, 5.613, 6.680, 7.925]
#ASTM E 11-70
ASTM=[0.02, 0.025, 0.032, 0.038, 0.045, 0.053, 0.063, 0.075, 0.09, 0.106, 0.125, 0.150, 0.180, 0.212, 0.250, 0.300, 0.355, 0.425, 0.5, 0.6, 0.71, 0.85, 1., 1.18, 1.4, 1.7, 2., 2.36, 2.8, 3.35, 4., 4.75, 5.6, 6.3, 6.7, 8., 9.5, 11.2, 12.5, 13.2, 16.0, 19., 22.4, 25., 26.5, 31.5, 37.5, 45., 50., 53., 63., 75., 90., 100., 106., 125]
#DIN 4188
DIN=[0.02, 0.022, 0.025, 0.028, 0.032, 0.036, 0.04, 0.045, 0.05, 0.056, 0.063, 0.071, 0.08, 0.09, 0.1, 0.125, 0.14, 0.18, 0.2, 0.224, 0.25, 0.28, 0.315, 0.355, 0.4, 0.5, 0.56, 0.63, 0.71, 0.8, 0.9, 1.0, 1.18, 1.25, 1.4, 1.6, 1.8, 2., 2.24, 2.5, 2.8, 3.15, 3.55, 4., 4.5, 5., 5.6]
#AFNOR NFX11-501
AFNOR=[0.02, 0.022, 0.025, 0.028, 0.032, 0.036, 0.04, 0.045, 0.05, 0.056, 0.063, 0.071, 0.08, 0.09, 0.1, 0.125, 0.14, 0.16, 0.18, 0.2, 0.224, 0.25, 0.28, 0.315, 0.355, 0.4, 0.45, 0.5, 0.56, 0.63, 0.71, 0.8, 0.9, 1.0, 1.18, 1.25, 1.4, 1.6, 1.8, 2., 2.24, 2.5, 3.15, 3.55, 4., 4.5, 5., 5.6]
#ISO 565
ISO=[0.02, 0.022, 0.025, 0.028, 0.032, 0.036, 0.045, 0.05, 0.063, 0.071, 0.08, 0.09, 0.1, 0.125, 0.14, 0.18, 0.2, 0.224, 0.25, 0.28, 0.315, 0.355, 0.4, 0.45, 0.63, 0.71, 0.8, 0.9, 1.0, 1.18, 1.25, 1.4, 1.6, 1.8, 2., 2.24, 2.5, 2.8, 3.15, 3.55, 4., 4.5, 5., 5.6]
#BS 410
BS=[0.045, 0.053, 0.063, 0.075, 0.09, 0.106, 0.125, 0.15, 0.18, 0.212, 0.25, 0.3, 0.355, 0.425, 0.5, 0.6, 0.71, 0.85, 1.0, 1.18, 1.4, 1.7, 2.0, 2.36, 2.8, 3.35, 4.0, 4.75, 5.6]



class Dialog_Distribucion(QtGui.QDialog):
    def __init__(self, parent=None):
        super(Dialog_Distribucion, self).__init__(parent)
        self.setWindowTitle(QtGui.QApplication.translate("pychemqt", "Generate solid distribution"))
        self.matriz=[]
        
        layout = QtGui.QGridLayout(self)
        layout.addWidget(QtGui.QLabel(QtGui.QApplication.translate("pychemqt", "Model")),0,0,1,1)
        self.modelo=QtGui.QComboBox()
        layout.addWidget(self.modelo, 0, 1, 1, 1)
        self.stacked = QtGui.QStackedWidget()
        self.modelo.currentIndexChanged.connect(self.stacked.setCurrentIndex)
        layout.addWidget(self.stacked, 1, 0, 1, 2)
        
        layout.addWidget(QtGui.QLabel(QtGui.QApplication.translate("pychemqt", "Standards:")),2,0,1,1)
        self.standard=QtGui.QComboBox()
        self.standard.addItem("Tyler")
        self.standard.addItem("ASTM")
        self.standard.addItem("DIN")
        self.standard.addItem("BS")
        self.standard.addItem("AFNOR")
        self.standard.addItem("ISO")
        self.standard.addItem(QtGui.QApplication.translate("pychemqt", "Custom"))
        self.standard.currentIndexChanged.connect(self.standardCambiado)
        layout.addWidget(self.standard, 2, 1, 1, 1)
        
        self.diametros = QtGui.QLineEdit()
        layout.addWidget(self.diametros, 3, 1, 1, 2)
        
        layout.addItem(QtGui.QSpacerItem(20,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding),4,1,1,3)
        self.buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.accepted.connect(self.aceptar)
        layout.addWidget(self.buttonBox, 5, 0, 1, 2)
        
        self.rosin=QtGui.QWidget()
        self.stacked.addWidget(self.rosin)
        self.modelo.addItem("Rosin Rammler Sperling")
        layout = QtGui.QGridLayout(self.rosin)
        layout.addWidget(QtGui.QLabel("d*="),1,1,1,1)
        layout.addWidget(QtGui.QLabel("S="),2,1,1,1)
        self.rosinEntries=[Entrada_con_unidades(unidades.Length, "ParticleDiameter"), Entrada_con_unidades(float)]
        layout.addWidget(self.rosinEntries[0],1,2,1,1)
        layout.addWidget(self.rosinEntries[1],2,2,1,1)
        layout.addItem(QtGui.QSpacerItem(20,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding),5,1,1,3)
        
        self.gates=QtGui.QWidget()
        self.stacked.addWidget(self.gates)
        self.modelo.addItem("Gates Gaudin Schumann")
        layout = QtGui.QGridLayout(self.gates)
        layout.addWidget(QtGui.QLabel("d*="),1,1,1,1)
        layout.addWidget(QtGui.QLabel("N="),2,1,1,1)
        self.gatesEntries=[Entrada_con_unidades(unidades.Length, "ParticleDiameter"), Entrada_con_unidades(float)]
        layout.addWidget(self.gatesEntries[0],1,2,1,1)
        layout.addWidget(self.gatesEntries[1],2,2,1,1)
        
        layout.addItem(QtGui.QSpacerItem(20,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding),5,1,1,3)

        self.broadbent=QtGui.QWidget()
        self.stacked.addWidget(self.broadbent)
        self.modelo.addItem("Broadbent Callcott")
        layout = QtGui.QGridLayout(self.broadbent)
        layout.addWidget(QtGui.QLabel("d*="),1,1,1,1)
        layout.addWidget(QtGui.QLabel("N="),2,1,1,1)
        self.broadbentEntries=[Entrada_con_unidades(unidades.Length, "ParticleDiameter"), Entrada_con_unidades(float)]
        layout.addWidget(self.broadbentEntries[0],1,2,1,1)
        layout.addWidget(self.broadbentEntries[1],2,2,1,1)
        layout.addItem(QtGui.QSpacerItem(20,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding),5,1,1,3)

        self.gaudin=QtGui.QWidget()
        self.stacked.addWidget(self.gaudin)
        self.modelo.addItem("Gaudin Meloy")
        layout = QtGui.QGridLayout(self.gaudin)
        layout.addWidget(QtGui.QLabel("d*="),1,1,1,1)
        layout.addWidget(QtGui.QLabel("N="),2,1,1,1)
        self.gaudintEntries=[Entrada_con_unidades(unidades.Length, "ParticleDiameter"), Entrada_con_unidades(float)]
        layout.addWidget(self.gaudintEntries[0],1,2,1,1)
        layout.addWidget(self.gaudintEntries[1],2,2,1,1)
        layout.addItem(QtGui.QSpacerItem(20,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding),5,1,1,3)

        self.logaritmic=QtGui.QWidget()
        self.stacked.addWidget(self.logaritmic)
        self.modelo.addItem("Lognormal")
        layout = QtGui.QGridLayout(self.logaritmic)
        layout.addWidget(QtGui.QLabel("d*="),1,1,1,1)
        layout.addWidget(QtGui.QLabel(u"σ="),2,1,1,1)
        self.logaritmicEntries=[Entrada_con_unidades(unidades.Length, "ParticleDiameter"), Entrada_con_unidades(float)]
        layout.addWidget(self.logaritmicEntries[0],1,2,1,1)
        layout.addWidget(self.logaritmicEntries[1],2,2,1,1)
        layout.addItem(QtGui.QSpacerItem(20,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding),5,1,1,3)

        self.harris=QtGui.QWidget()
        self.stacked.addWidget(self.harris)
        self.modelo.addItem("Harris")
        layout = QtGui.QGridLayout(self.harris)
        layout.addWidget(QtGui.QLabel("d*="),1,1,1,1)
        layout.addWidget(QtGui.QLabel("S="),2,1,1,1)
        layout.addWidget(QtGui.QLabel("N="),3,1,1,1)
        self.harrisEntries=[Entrada_con_unidades(unidades.Length, "ParticleDiameter"), Entrada_con_unidades(float), Entrada_con_unidades(float)]
        layout.addWidget(self.harrisEntries[0],1,2,1,1)
        layout.addWidget(self.harrisEntries[1],2,2,1,1)
        layout.addWidget(self.harrisEntries[2],3,2,1,1)
        layout.addItem(QtGui.QSpacerItem(20,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding),5,1,1,3)
        
        self.standardCambiado(0)
        
    def standardCambiado(self, estandar):
        if estandar==6:
            self.diametros.setEnabled(True)
        else:
            self.diametros.setEnabled(False)
            self.estandares=[Tyler, ASTM, DIN, BS, AFNOR, ISO][estandar]
    
    def aceptar(self):
        if self.standard.currentIndex()<6:
            d=self.estandares
        else:
            pass
        if self.modelo.currentIndex()==0:
            funcion = lambda p, d: 1.-exp(-(d/p[0]/1000.)**p[1])
            parametros=[i.value for i in self.rosinEntries]
        elif self.modelo.currentIndex()==1:
            funcion = lambda p, d: (d/p[0]/1000.)**p[1]
            parametros=[i.value for i in self.gatesEntries]
        elif self.modelo.currentIndex()==2:
            funcion = lambda p, d: 1-(1-d/p[0]/1000.)**p[1]
            parametros=[i.value for i in self.broadbentEntries]
        elif self.modelo.currentIndex()==3:
            funcion = lambda p, d: 1.-exp(-(d/p[0]/1000.)**p[1])/(1-exp(-1.))
            parametros=[i.value for i in self.gaudintEntries]
        elif self.modelo.currentIndex()==4:
            funcion = lambda p, d: erf(log(d/p[0]/1000.)/p[1]) 
            parametros=[i.value for i in self.logaritmicEntries]
        elif self.modelo.currentIndex()==5:
            funcion = lambda p, d: 1-(1-d/(p[0]/1000.)**p[1])**p[2]
            parametros=[i.value for i in self.harrisEntries]
        
        diametros=[unidades.Length(x) for x in d ]
        acumulado=[0]+[funcion(parametros, x) for x in d]
        if acumulado[-1]<1.:
            acumulado[-1]=1.
        diferencia=[acumulado[i+1]-acumulado[i] for i in range(len(d))]
        self.matriz=[[diametros[i].config("Diameter"), diferencia[i]] for i in range(len(d))]
        self.accept()


class StreamDefinition(QtGui.QWidget):
    """Widget for stream definition as standard P,T,x composition input"""
    changedValue = QtCore.pyqtSignal(str, float)
    changedFraction = QtCore.pyqtSignal(str, list)
    
    def __init__(self, stream=None, readOnly=False, parent=None):
        super(StreamDefinition, self).__init__(parent)
        
        self.indices, self.nombres, M=config.getComponents()
        
        lyt =  QtGui.QGridLayout(self)
        lyt.setVerticalSpacing(0)
        lyt.addWidget(QtGui.QLabel(QtGui.QApplication.translate(
            "pychemqt", "Temperature")), 1, 1)
        self.T=Entrada_con_unidades(unidades.Temperature, readOnly=readOnly)
        self.T.valueChanged.connect(partial(self.calculo, "T"))
        lyt.addWidget(self.T, 1, 2, 1, 2)
        lyt.addWidget(QtGui.QLabel(QtGui.QApplication.translate(
            "pychemqt", "Pressure")), 2, 1)
        self.P=Entrada_con_unidades(unidades.Pressure, readOnly=readOnly)
        self.P.valueChanged.connect(partial(self.calculo, "P"))
        lyt.addWidget(self.P, 2, 2, 1, 2)
        lyt.addWidget(QtGui.QLabel(QtGui.QApplication.translate(
            "pychemqt", "Vapor fraccion")), 3, 1)
        self.x=Entrada_con_unidades(float, readOnly=readOnly)
        self.x.valueChanged.connect(partial(self.calculo, "x"))
        lyt.addWidget(self.x, 3, 2, 1, 2)
        lyt.addItem(QtGui.QSpacerItem(10, 10, QtGui.QSizePolicy.Fixed, 
                                      QtGui.QSizePolicy.Fixed), 4, 1, 1, 2)
        lyt.addWidget(QtGui.QLabel(QtGui.QApplication.translate(
            "pychemqt", "Mass flow")), 5, 1)
        self.caudalMasico=Entrada_con_unidades(unidades.MassFlow, readOnly=readOnly)
        self.caudalMasico.valueChanged.connect(partial(self.calculo, "caudalMasico"))
        lyt.addWidget(self.caudalMasico, 5, 2, 1, 2)
        lyt.addWidget(QtGui.QLabel(QtGui.QApplication.translate(
            "pychemqt", "Molar flow")), 6, 1)
        self.caudalMolar=Entrada_con_unidades(unidades.MolarFlow, readOnly=readOnly)
        self.caudalMolar.valueChanged.connect(partial(self.calculo, "caudalMolar"))
        lyt.addWidget(self.caudalMolar, 6, 2, 1, 2)
        lyt.addWidget(QtGui.QLabel(QtGui.QApplication.translate(
            "pychemqt", "Volumetric flow")), 7, 1)
        self.caudalVolumetrico=Entrada_con_unidades(unidades.VolFlow, "volliq", readOnly=readOnly)
        self.caudalVolumetrico.valueChanged.connect(partial(self.calculo, "caudalVolumetrico"))
        lyt.addWidget(self.caudalVolumetrico, 7, 2, 1, 2)
        
        lyt.addItem(QtGui.QSpacerItem(10, 10, QtGui.QSizePolicy.Fixed, 
                                      QtGui.QSizePolicy.Fixed), 8, 1, 1, 1)
        lyt.addWidget(QtGui.QLabel(QtGui.QApplication.translate(
            "pychemqt", "Composition")), 9, 1)
        self.tipoFraccion = QtGui.QComboBox()
        self.tipoFraccion.addItem(unidades.MassFlow.text())
        self.tipoFraccion.addItem(unidades.MolarFlow.text())
        self.tipoFraccion.addItem(QtGui.QApplication.translate("pychemqt", "Mass fraction"))
        self.tipoFraccion.addItem(QtGui.QApplication.translate("pychemqt", "Molar fraction"))
        self.tipoFraccion.setCurrentIndex(3)
        self.tipoFraccion.currentIndexChanged.connect(self.tipoFraccionesCambiado)
        self.tipoFraccion.setSizePolicy(QtGui.QSizePolicy.Maximum,QtGui.QSizePolicy.Maximum)
        lyt.addWidget(self.tipoFraccion, 9, 2)
        lyt.addItem(QtGui.QSpacerItem(5, 5, QtGui.QSizePolicy.Fixed, 
                                      QtGui.QSizePolicy.Fixed), 10, 1, 1, 1)

        composition = QtGui.QWidget()
        comp_lyt = QtGui.QGridLayout(composition)
        comp_lyt.setVerticalSpacing(0)
        self.xi = []
        for i, nombre in enumerate(self.nombres):
            label = QtGui.QLabel(nombre)
            label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
            comp_lyt.addWidget(label, i, 1)
            widget = Entrada_con_unidades(float, readOnly=readOnly)
            widget.valueChanged.connect(self.changeFraction)
            comp_lyt.addWidget(widget, i, 2)
            self.xi.append(widget)
        scroll = QtGui.QScrollArea()
        scroll.setFrameShape(QtGui.QFrame.NoFrame)
        scroll.setWidget(composition)
        lyt.addWidget(scroll, 10, 1, 1, 2)
            
        if stream:
            self.setStream(stream)
        else:
            self.stream=Corriente()
        
        lyt.addItem(QtGui.QSpacerItem(0,0,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding),11,3)

    def setReadOnly(self, bool):
        self.T.setReadOnly(bool)
        self.P.setReadOnly(bool)
        self.x.setReadOnly(bool)
        self.caudalMasico.setReadOnly(bool)
        self.caudalMolar.setReadOnly(bool)
        self.caudalVolumetrico.setReadOnly(bool)
        for widget in self.xi:
            widget.setReadOnly(bool)

    def setStream(self, stream):
        self.stream = stream
        if stream.status==1:
            self.T.setValue(stream.T)
            self.setResaltado(stream, "T")
            self.P.setValue(stream.P)
            self.setResaltado(stream, "P")
            self.x.setValue(stream.x)
            self.setResaltado(stream, "x")
            self.caudalMasico.setValue(stream.caudalmasico)
            self.setResaltado(stream, "caudalMasico")
            self.caudalMolar.setValue(stream.caudalmolar)
            self.setResaltado(stream, "caudalMolar")
            self.caudalVolumetrico.setValue(stream.Q)
            self.setResaltado(stream, "caudalVolumetrico")
            
            if stream.tipoFlujo == 1:
                self.tipoFraccion.setCurrentIndex(0)
                prop = stream.caudalunitariomasico
            elif stream.tipoFlujo == 2:
                self.tipoFraccion.setCurrentIndex(1)
                prop = stream.caudalunitariomolar
            elif stream.tipoFlujo in (4, 6):
                self.tipoFraccion.setCurrentIndex(2)
                prop = stream.fraccion_masica
            else:
                self.tipoFraccion.setCurrentIndex(3)
                prop = stream.fraccion
            for value, widget in zip(prop, self.xi):
                widget.setValue(value)

        elif stream.numInputs:
            for input in ["T", "P", "x", "caudalMasico", "caudalMolar", "caudalVolumetrico"]:
                if stream.kwargs[input]:
                    self.__getattribute__(input).setValue(stream.kwargs[input])
                    self.__getattribute__(input).setResaltado(True)
                else:
                    self.__getattribute__(input).clear()
                    self.__getattribute__(input).setResaltado(False)
            
            prop = None
            if stream.tipoFlujo == 1:
                self.tipoFraccion.setCurrentIndex(0)
                propi = stream.kwargs["caudalUnitarioMasico"]
                prop = []
                for value in propi:
                    prop.append(unidades.MassFlow(value).config())
            elif stream.tipoFlujo == 2:
                self.tipoFraccion.setCurrentIndex(1)
                propi = stream.kwargs["caudalUnitarioMolar"]
                prop = []
                for value in propi:
                    prop.append(unidades.MolarFlow(value).config())
            elif stream.tipoFlujo in (4, 6):
                self.tipoFraccion.setCurrentIndex(2)
                prop = stream.kwargs["fraccionMasica"]
            elif stream.tipoFlujo in (3, 5):
                self.tipoFraccion.setCurrentIndex(3)
                prop = stream.kwargs["fraccionMolar"]
            elif stream.kwargs["fraccionMasica"]:
                self.tipoFraccion.setCurrentIndex(2)
                prop = stream.kwargs["fraccionMasica"]
            elif stream.kwargs["fraccionMolar"]:
                self.tipoFraccion.setCurrentIndex(3)
                prop = stream.kwargs["fraccionMolar"]
                
            if prop:
                for value, widget in zip(prop, self.xi):
                    widget.setValue(value)
                self.caudalMolar.setValue(stream.mezcla.caudalmolar)
                self.caudalMasico.setValue(stream.mezcla.caudalmasico)

    def setResaltado(self, stream, arg):
            if stream.kwargs[arg]:
                self.__getattribute__(arg).setResaltado(True)
            else:
                self.__getattribute__(arg).setResaltado(False)
                
    def calculo(self, key, value):
        self.changedValue[str, float].emit(key, value)

    def tipoFraccionesCambiado(self, index):
        values = None
        if self.stream.status == 1:
            if index == 0:
                values = self.stream.caudalunitariomasico
            elif index == 1:
                values = self.stream.caudalunitariomolar
            elif index == 2:
                values = self.stream.fraccion_masica
            else:
                values = self.stream.fraccion

        elif self.stream.tipoFlujo:
            if index == 0:
                values = self.stream.mezcla.caudalunitariomasico
            elif index == 1:
                values = self.stream.mezcla.caudalunitariomolar
            elif index == 2:
                values = self.stream.mezcla.fraccion_masica
            else:
                values = self.stream.mezcla.fraccion
        
        if values:
            for value, widget in zip(values, self.xi):
                widget.setValue(value.config())

    def changeFraction(self):
        key = ["caudalUnitarioMasico", "caudalUnitarioMolar", "fraccionMasica",
               "fraccionMolar"][self.tipoFraccion.currentIndex()]
        values = []
        for widget in self.xi:
            if self.tipoFraccion.currentIndex() == 0:
                value = unidades.MassFlow(widget.value, "conf")
            elif self.tipoFraccion.currentIndex() == 1:
                value = unidades.MolarFlow(widget.value, "conf")
            else:
                value = widget.value
            values.append(value)
        if sum(values) == 1.0 or all(values):
            self.changedFraction[str, list].emit(key, values)


class SolidDefinition(QtGui.QWidget):
    """Widget for solids edit/view"""
    Changed = QtCore.pyqtSignal(Solid)
    solido = Solid()
    
    def __init__(self, solid=None, readOnly=False, parent=None):
        super(SolidDefinition, self).__init__(parent)
        
        self.solidos, self.nombreSolidos, MSolidos=config.getComponents(solidos=True)
        self.readOnly=readOnly
        self.semaforo=QtCore.QSemaphore(1)
        self.evaluate=Evaluate()
        self.evaluate.finished.connect(self.fill)

        lyt = QtGui.QGridLayout(self)
        header = [QtGui.QApplication.translate("pychemqt", "Mass flow") + ", " 
                  + unidades.MassFlow.text()]
        self.TablaSolidos = Tabla(1, horizontalHeader=header, stretch=False,
            verticalHeaderLabels=self.nombreSolidos, filas=len(self.solidos))
        self.TablaSolidos.setFixedHeight(22*len(self.solidos)+24+4)
        self.CaudalSolidos=[]
        for i in range(len(self.nombreSolidos)):
            widget = Entrada_con_unidades(unidades.MassFlow, texto=False, boton=False,
                                        width=self.TablaSolidos.columnWidth(0))
            widget.valueChanged.connect(self.caudalesSolidoFinished)
            self.CaudalSolidos.append(widget)
            self.TablaSolidos.setCellWidget(i, 0, widget)
        lyt.addWidget(self.TablaSolidos, 1, 1, 1, 2)
        lyt.addItem(QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Expanding, 
                                      QtGui.QSizePolicy.Fixed), 2, 2)
        lyt.addWidget(QtGui.QLabel(QtGui.QApplication.translate(
            "pychemqt", "Mean Diameter")),3,1,1,1)
        self.diametroParticula=Entrada_con_unidades(unidades.Length,
                                                    "ParticleDiameter")
        self.diametroParticula.valueChanged.connect(partial(self.calculo,
                                                            "diametroMedio"))
        lyt.addWidget(self.diametroParticula,3,2,1,1)  
        self.checkDistribucion = QtGui.QCheckBox(QtGui.QApplication.translate(
            "pychemqt", "Use particle size distribution"))
        self.checkDistribucion.toggled.connect(self.checkDistributionToggled)
        lyt.addWidget(self.checkDistribucion,5,1,1,2)

        header = [QtGui.QApplication.translate("pychemqt", "Diameter") + ", " +
                  unidades.Length.text("ParticleDiameter"),
                  QtGui.QApplication.translate("pychemqt", "Fraction")]
        self.distribucionTamanos = Tabla(2, horizontalHeader=header, 
                                         stretch=False, verticalHeader=False)
        self.distribucionTamanos.rowFinished.connect(self.diametro_medio)
        self.distribucionTamanos.editingFinished.connect(self.distribucionFinished)
        lyt.addWidget(self.distribucionTamanos,6,1,1,2)
        
        dialog = self.buttonBox = QtGui.QDialogButtonBox()
        self.botonNormalizar = QtGui.QPushButton(
            QtGui.QApplication.translate("pychemqt", "Normalize"))
        self.botonNormalizar.clicked.connect(self.botonNormalizar_clicked)
        dialog.addButton(self.botonNormalizar, QtGui.QDialogButtonBox.AcceptRole)
        self.botonGenerar = QtGui.QPushButton(
            QtGui.QApplication.translate("pychemqt", "Generate"))
        self.botonGenerar.clicked.connect(self.botonGenerar_clicked)
        dialog.addButton(self.botonGenerar, QtGui.QDialogButtonBox.AcceptRole)
        lyt.addWidget(dialog,7,1,1,2)
        
        if solid:
            self.setSolido(solid)
        self.distribucionTamanos.setConnected()

    def setSolido(self, solido):
        if solido:
            self.solido=solido
            self.fill()

    def fill(self):
        if self.semaforo.available()>0:
            self.semaforo.acquire(1)
            if self.solido._def:
                for i, caudal in enumerate(self.solido.caudalUnitario):
                    self.CaudalSolidos[i].setValue(caudal)
                if self.solido._def==1:
                    self.checkDistribucion.setChecked(False)
                else:
                    self.checkDistribucion.setChecked(True)
                if self.solido.diametros:
                    diametros=[d.config("ParticleDiameter") for d in self.solido.diametros]
                    self.distribucionTamanos.setColumn(0, diametros)
                    self.distribucionTamanos.setColumn(1, self.solido.fracciones)
                self.diametroParticula.setValue(self.solido.diametro_medio)
            self.semaforo.release(1)

    def setReadOnly(self, bool):
        if bool:
            triggers = QtGui.QAbstractItemView.NoEditTriggers
        else:
            triggers = QtGui.QAbstractItemView.AllEditTriggers
        self.TablaSolidos.setEditTriggers(triggers)
        self.distribucionTamanos.setEditTriggers(triggers)

    def distribucionFinished(self):
        conversion=unidades.Length(1, "conf", "ParticleDiameter").m
        diametros=[diametro*conversion for diametro in self.distribucionTamanos.getColumn(0, False)]
        fracciones=self.distribucionTamanos.getColumn(1, False)
        if diametros:
            kwargs={"distribucion_diametro": diametros, "distribucion_fraccion": fracciones}
            self.salida(**kwargs)
    
    def caudalesSolidoFinished(self):
        caudales=self.caudalSolido()
        kwargs={"caudalSolido": caudales}
        self.salida(**kwargs)
        
    def caudalSolido(self):
        caudales=[]
        for widget in self.CaudalSolidos:
            caudales.append(widget.value)
        return caudales

    def checkDistributionToggled(self, bool):
        self.distribucionTamanos.setEnabled(bool)
        self.botonGenerar.setEnabled(bool)
        self.botonNormalizar.setEnabled(bool)
        self.diametroParticula.setDisabled(bool)
        if bool:
            self.solido.kwargs["diametroMedio"]=None
            self.distribucionFinished()
            
        else:
            self.solido.kwargs["distribucion_diametro"]=[]
            self.solido.kwargs["distribucion_fraccion"]=[]
            kwargs={"diametroMedio": self.diametroParticula.value}
            self.salida(**kwargs)


    def botonNormalizar_clicked(self, diametros=None, fracciones=None):
        if not diametros:
            diametros=self.distribucionTamanos.getColumn(0, False)
        if not fracciones:
            fracciones=self.distribucionTamanos.getColumn(1, False)
        if diametros:
            diametros.sort()
            suma=sum(fracciones)
            fracciones=[fraccion/suma for fraccion in fracciones]
            self.distribucionTamanos.setColumn(0, diametros)
            self.distribucionTamanos.setColumn(1, fracciones)


    def botonGenerar_clicked(self):
        dialog=Dialog_Distribucion(self)
        if dialog.exec_():
            self.distribucionTamanos.setMatrix(dialog.matriz)

    def diametro_medio(self):
        conversion=unidades.Length(1, "conf", "ParticleDiameter").m
        diametros=[diametro*conversion for diametro in self.distribucionTamanos.getColumn(0, False)]
        fracciones=self.distribucionTamanos.getColumn(1, False)
        if sum(fracciones)!=1.:
            suma=sum(fracciones)
            fracciones=[fraccion/suma for fraccion in fracciones]

        diametro_medio=sum([diametro*fraccion for diametro, fraccion in zip(diametros, fracciones)])
        self.diametroParticula.setValue(diametro_medio)

    def calculo(self):
        pass

    def salida(self, **kwargs):
        """Return kwargs argument to solid definition"""
        if not kwargs:
            kwargs={}
            kwargs["caudalSolido"]=self.caudalSolido()
            kwargs["diametroMedio"]=self.diametroParticula.value
            kwargs["distribucion_diametro"]=self.TablaSolidos.getColumn(0)
            kwargs["distribucion_fraccion"]=self.TablaSolidos.getColumn(1)
            
        if not self.evaluate.isRunning():
            self.evaluate.start(self.solido, kwargs)


class StreamProperties(QtGui.QTableWidget):
    """Table to show stream properties"""
    def __init__(self, stream=None, parent=None):
        super(StreamProperties, self).__init__(11, 2, parent)
        for i in range(self.rowCount()):
            self.setRowHeight(i, 24)
        self.setColumnWidth(0, 85)
        self.setColumnWidth(1, 85)
        self.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.horizontalHeader().setResizeMode(QtGui.QHeaderView.Fixed)
        self.verticalHeader().setResizeMode(QtGui.QHeaderView.Fixed)
        self.horizontalHeader().resizeSections(QtGui.QHeaderView.Fixed)
        self.setHorizontalHeaderLabels([QtGui.QApplication.translate("pychemqt", "Liquid"), QtGui.QApplication.translate("pychemqt", "Vapor")])
        self.setVerticalHeaderLabels([QtGui.QApplication.translate("pychemqt", "Mass Flow") + ", " + unidades.MassFlow(None).text(), QtGui.QApplication.translate("pychemqt", "Molar Flow") + ", " + unidades.MolarFlow(None).text(), QtGui.QApplication.translate("pychemqt", "Vol Flow") + ", " + unidades.VolFlow(None).text("QLiq"), QtGui.QApplication.translate("pychemqt", "Enthalpy")+ ", "+ unidades.Power(None).text(), QtGui.QApplication.translate("pychemqt", "Molecular Weight"), QtGui.QApplication.translate("pychemqt", "Density")+ ", " + unidades.Density(None).text("DenLiq"), QtGui.QApplication.translate("pychemqt", "Compressibility"), QtGui.QApplication.translate("pychemqt", "Cp") + ", " + unidades.SpecificHeat(None).text(), QtGui.QApplication.translate("pychemqt", "Viscosity") +", "+ unidades.Viscosity(None).text(), QtGui.QApplication.translate("pychemqt", "Conductivity") +", "+ unidades.ThermalConductivity(None).text(), QtGui.QApplication.translate("pychemqt", "Tension")+", "+ unidades.Tension(None).text()])

        self.CaudalLiquido=Entrada_con_unidades(unidades.MassFlow, retornar=False, readOnly=True, texto=False)
        self.setCellWidget(0, 0, self.CaudalLiquido)
        self.CaudalGas=Entrada_con_unidades(unidades.MassFlow, retornar=False, readOnly=True, texto=False)
        self.setCellWidget(0, 1, self.CaudalGas)
        self.CaudalMolarLiquido=Entrada_con_unidades(unidades.MolarFlow, retornar=False, readOnly=True, texto=False)
        self.setCellWidget(1, 0, self.CaudalMolarLiquido)
        self.CaudalMolarGas=Entrada_con_unidades(unidades.MolarFlow, retornar=False, readOnly=True, texto=False)
        self.setCellWidget(1, 1, self.CaudalMolarGas)
        self.CaudalVolumetricoLiquido=Entrada_con_unidades(unidades.VolFlow, "QLiq", retornar=False, readOnly=True, texto=False)
        self.setCellWidget(2, 0, self.CaudalVolumetricoLiquido)
        self.CaudalVolumetricoGas=Entrada_con_unidades(unidades.VolFlow, "QLiq", retornar=False, readOnly=True, texto=False)
        self.setCellWidget(2, 1, self.CaudalVolumetricoGas)
        self.entalpiaLiquido=Entrada_con_unidades(unidades.Power, retornar=False, readOnly=True, texto=False)
        self.setCellWidget(3, 0, self.entalpiaLiquido)
        self.entalpiaGas=Entrada_con_unidades(unidades.Power, retornar=False, readOnly=True, texto=False)
        self.setCellWidget(3, 1, self.entalpiaGas)
        self.PesoMolecularLiquido=Entrada_con_unidades(float, readOnly=True)
        self.setCellWidget(4, 0, self.PesoMolecularLiquido)
        self.PesoMolecularGas=Entrada_con_unidades(float, readOnly=True)
        self.setCellWidget(4, 1, self.PesoMolecularGas)
        self.DensidadLiquido=Entrada_con_unidades(unidades.Density, "DenLiq", retornar=False, readOnly=True, texto=False)
        self.setCellWidget(5, 0, self.DensidadLiquido)
        self.DensidadGas=Entrada_con_unidades(unidades.Density, "DenLiq", retornar=False, readOnly=True, texto=False)
        self.setCellWidget(5, 1, self.DensidadGas)
        self.ZLiquido=Entrada_con_unidades(float, readOnly=True)
        self.setCellWidget(6, 0, self.ZLiquido)
        self.ZGas=Entrada_con_unidades(float, readOnly=True)
        self.setCellWidget(6, 1, self.ZGas)
        self.CpLiquido=Entrada_con_unidades(unidades.SpecificHeat, retornar=False, readOnly=True, texto=False)
        self.setCellWidget(7, 0, self.CpLiquido)
        self.CpGas=Entrada_con_unidades(unidades.SpecificHeat, retornar=False, readOnly=True, texto=False)
        self.setCellWidget(7, 1, self.CpGas)
        self.ViscosidadLiquido=Entrada_con_unidades(unidades.Viscosity, retornar=False, readOnly=True, texto=False)
        self.setCellWidget(8, 0, self.ViscosidadLiquido)
        self.ViscosidadGas=Entrada_con_unidades(unidades.Viscosity, retornar=False, readOnly=True, texto=False)
        self.setCellWidget(8, 1, self.ViscosidadGas)
        self.ConductividadLiquido=Entrada_con_unidades(unidades.ThermalConductivity, retornar=False, readOnly=True, texto=False)
        self.setCellWidget(9, 0, self.ConductividadLiquido)
        self.ConductividadGas=Entrada_con_unidades(unidades.ThermalConductivity, retornar=False, readOnly=True, texto=False)
        self.setCellWidget(9, 1, self.ConductividadGas)
        self.Tension=Entrada_con_unidades(unidades.Tension, retornar=False, readOnly=True, texto=False)
        self.setCellWidget(10, 0, self.Tension)
        
        if stream:
            self.fill(stream)
        
    def fill(self, stream):
        if stream.status == 1:
            if stream.x>0:
                self.CaudalGas.setValue(stream.Gas.caudalmasico)
                self.CaudalMolarGas.setValue(stream.Gas.caudalmolar)
                self.entalpiaGas.setValue(stream.Gas.h)
                self.PesoMolecularGas.setValue(stream.Gas.M)
                self.DensidadGas.setValue(stream.Gas.rho)
                self.CaudalVolumetricoGas.setValue(stream.Gas.Q)
                self.ZGas.setValue(stream.Gas.Z)
                self.CpGas.setValue(stream.Gas.cp)
                self.ViscosidadGas.setValue(stream.Gas.mu)
                self.ConductividadGas.setValue(stream.Gas.k)
            if stream.x<1:
                self.CaudalLiquido.setValue(stream.Liquido.caudalmasico)
                self.CaudalMolarLiquido.setValue(stream.Liquido.caudalmolar)
                self.entalpiaLiquido.setValue(stream.Liquido.h)
                self.PesoMolecularLiquido.setValue(stream.Liquido.M)
                self.DensidadLiquido.setValue(stream.Liquido.rho)
                self.CaudalVolumetricoLiquido.setValue(stream.Liquido.Q)
                self.ZLiquido.setValue(stream.Liquido.Z)
                self.CpLiquido.setValue(stream.Liquido.cp)
                self.ViscosidadLiquido.setValue(stream.Liquido.mu)
                self.ConductividadLiquido.setValue(stream.Liquido.k)
                self.Tension.setValue(stream.Liquido.epsilon)


class Ui_corriente(QtGui.QWidget):
    """Wdiget for flobal stream edit/view"""
    Changed = QtCore.pyqtSignal(Corriente)
    corriente = Corriente()
    def __init__(self, corriente=None, readOnly=False, psychro=False, parent=None):
        super(Ui_corriente, self).__init__(parent)
        self.setWindowTitle(QtGui.QApplication.translate("pychemqt", "Stream"))
        self.readOnly=readOnly
        self.psychro = psychro
        self.semaforo=QtCore.QSemaphore(1)
        self.evaluate=Evaluate()
        self.evaluate.finished.connect(self.repaint)

        self.indices, self.nombres, M=config.getComponents()
        self.solidos, self.nombreSolidos, MSolidos=config.getComponents(solidos=True)

        gridLayout1 = QtGui.QVBoxLayout(self)
        self.toolBox = QtGui.QTabWidget()
        self.toolBox.setTabPosition(QtGui.QTabWidget.South)
        gridLayout1.addWidget(self.toolBox)

        # Standard definition
        self.pageDefinition = StreamDefinition()
        self.pageDefinition.changedFraction.connect(self.calculo)
        self.pageDefinition.changedValue.connect(self.calculo)
        self.toolBox.addTab(self.pageDefinition, QtGui.QApplication.translate(
            "pychemqt", "Definition"))
        
        # Humid Air
        if psychro:
            self.pagePsychro = PsychroDefinition(readOnly)
            self.toolBox.addTab(self.pagePsychro,
                QtGui.QIcon(os.environ["pychemqt"] + "/images/button/psychrometric.png"),
                QtGui.QApplication.translate("pychemqt", "Humid Air"))

        # Solid
        self.pageSolids = SolidDefinition()
        self.pageSolids.Changed.connect(self.corriente.setSolid)
        self.toolBox.addTab(self.pageSolids, QtGui.QApplication.translate(
            "pychemqt", "Solid"))
        self.pageSolids.setEnabled(len(self.solidos))

#        # Electrolite
#        self.pageElectrolite = QtGui.QWidget()
#        lyt_Electrolitos = QtGui.QGridLayout(self.pageElectrolite)
#        lyt_Electrolitos.addWidget(QtGui.QLabel(QtGui.QApplication.translate(
#            "pychemqt", "No implemented")), 0, 0, 1, 1)
#        self.toolBox.addTab(self.pageElectrolite,QtGui.QApplication.translate(
#            "pychemqt", "Electrolitos"))

        # Properties
        self.pageProperties = StreamProperties()
        self.toolBox.addTab(self.pageProperties,
            QtGui.QIcon(os.environ["pychemqt"] + "/images/button/helpAbout.png"),
            QtGui.QApplication.translate("pychemqt", "Properties"))

        # Notes
        self.PageNotas = texteditor.TextEditor()
        self.toolBox.addTab(self.PageNotas, QtGui.QIcon(os.environ["pychemqt"]+
            "/images/button/editor.png"),
            QtGui.QApplication.translate("pychemqt", "Notes"))
        
        if corriente:
            self.setCorriente(corriente)
        else:
            self.corriente=Corriente()
        self.setReadOnly(readOnly)
        self.PageNotas.textChanged.connect(self.corriente.setNotas)

    def setReadOnly(self, bool):
        self.pageDefinition.setReadOnly(bool)
        self.pageSolids.setReadOnly(bool)
    
    def setCorriente(self, corriente):
        if corriente:
            self.corriente=corriente
            self.repaint()
        
    def repaint(self):
        if self.semaforo.available()>0:
            self.semaforo.acquire(1)
        self.pageDefinition.setStream(self.corriente)
        self.pageSolids.setSolido(self.corriente.solido)
        self.PageNotas.setText(self.corriente.notas)
        self.pageProperties.fill(self.corriente)
        if isinstance(self, QtGui.QDialog):
            self.status.setState(self.corriente.status, self.corriente.msg)
        self.semaforo.release(1)

    def tipoFraccionesCambiado(self):
        if self.tipoFraccion.currentIndex()==0:
            for i in range(len(self.indices)):
                self.TablaComposicion.item(i+1, 0).setText(representacion(self.corriente.caudalunitariomasico[i].kgh))
        elif self.tipoFraccion.currentIndex()==1:
            for i in range(len(self.indices)):
                self.TablaComposicion.item(i+1, 0).setText(representacion(self.corriente.caudalunitariomolar[i]))
        elif self.tipoFraccion.currentIndex()==2:
            for i in range(len(self.indices)):
                self.TablaComposicion.item(i+1, 0).setText(representacion(self.corriente.caudalunitariomasico[i].lbh))
        elif self.tipoFraccion.currentIndex()==3:
            for i in range(len(self.indices)):
                self.TablaComposicion.item(i+1, 0).setText(representacion(self.corriente.caudalunitariomolar[i]*lb))
        elif self.tipoFraccion.currentIndex()==4:
            for i in range(len(self.indices)):
                self.TablaComposicion.item(i+1, 0).setText(representacion(self.corriente.fraccion_masica[i]))
        elif self.tipoFraccion.currentIndex()==5:
            for i in range(len(self.indices)):
                self.TablaComposicion.item(i+1, 0).setText(representacion(self.corriente.fraccion[i]))

    def composicionEntrada(self):
        fracciones=self.TablaComposicion.getColumn(0)[1:]
        if self.tipoFraccion.currentIndex()==0:
            variable="caudalUnitarioMasico"
        elif self.tipoFraccion.currentIndex()==1:
            variable="caudalUnitarioMolar"
        elif self.tipoFraccion.currentIndex()==2:
            variable="caudalUnitarioMasico"
            fracciones=[fraccion*lb for fraccion in fracciones]
        elif self.tipoFraccion.currentIndex()==3:
            variable="caudalUnitarioMolar"
            fracciones=[fraccion*lb for fraccion in fracciones]
        elif self.tipoFraccion.currentIndex()==4:
            variable="fraccionMasica"
        elif self.tipoFraccion.currentIndex()==5:
            variable="fraccionMolar"
        return variable, fracciones
        
    def valueTablaFraccionesChanged(self):
        if self.semaforo.available()>0:
            variable, fracciones=self.composicionEntrada()
            if sum(fracciones)==1. or fracciones.count(0)==0:
                self.calculo(variable, fracciones)
        
    def calculo(self, variable, valor):
        if self.semaforo.available()>0:
            if isinstance(self, QtGui.QDialog):
                self.status.setState(4)
            kwargs={str(variable): valor}
            self.salida(**kwargs)


#    def distribucionFinished(self):
#        conversion=unidades.Length(1, "conf", "ParticleDiameter").m
#        diametros=[diametro*conversion for diametro in self.distribucionTamanos.getColumn(0, False)]
#        fracciones=self.distribucionTamanos.getColumn(1, False)
#        if diametros:
#            kwargs={"distribucion_diametro": diametros, "distribucion_fraccion": fracciones}
#            self.salida(**kwargs)
#    
#    def caudalesSolidoFinished(self):
#        caudales=self.caudalSolido()
#        kwargs={"caudalSolido": caudales}
#        self.salida(**kwargs)
#        
#    def caudalSolido(self):
#        caudales=[]
#        for widget in self.CaudalSolidos:
#            caudales.append(widget.value)
#        return caudales
#
#    def checkDistributionToggled(self, bool):
#        self.distribucionTamanos.setEnabled(bool)
#        self.botonGenerar.setEnabled(bool)
#        self.botonNormalizar.setEnabled(bool)
#        self.diametroParticula.setDisabled(bool)
#        if bool:
#            self.corriente.kwargs["diametroMedio"]=None
#            self.distribucionFinished()
#            
#        else:
#            self.corriente.kwargs["distribucion_diametro"]=[]
#            self.corriente.kwargs["distribucion_fraccion"]=[]
#            kwargs={"diametroMedio": self.diametroParticula.value}
#            self.salida(**kwargs)
#
#
#    def botonNormalizar_clicked(self, diametros=None, fracciones=None):
#        if not diametros:
#            diametros=self.distribucionTamanos.getColumn(0, False)
#        if not fracciones:
#            fracciones=self.distribucionTamanos.getColumn(1, False)
#        if diametros:
#            diametros.sort()
#            suma=sum(fracciones)
#            fracciones=[fraccion/suma for fraccion in fracciones]
#            self.distribucionTamanos.setColumn(0, diametros)
#            self.distribucionTamanos.setColumn(1, fracciones)
#
#
#    def botonGenerar_clicked(self):
#        dialog=Dialog_Distribucion(self)
#        if dialog.exec_():
#            self.distribucionTamanos.setMatrix(dialog.matriz)
#
#    def diametro_medio(self):
#        conversion=unidades.Length(1, "conf", "ParticleDiameter").m
#        diametros=[diametro*conversion for diametro in self.distribucionTamanos.getColumn(0, False)]
#        fracciones=self.distribucionTamanos.getColumn(1, False)
#        if sum(fracciones)!=1.:
#            suma=sum(fracciones)
#            fracciones=[fraccion/suma for fraccion in fracciones]
#
#        diametro_medio=sum([diametro*fraccion for diametro, fraccion in zip(diametros, fracciones)])
#        self.diametroParticula.setValue(diametro_medio)

    def clear(self):
        pass
    
    def salida(self, **kwargs):
        """Función que crea la instancia corriente"""
        if not kwargs:
            kwargs={}
            kwargs["T"]=self.T.value
            kwargs["P"]=self.P.value
            kwargs["x"]=self.x.value
            kwargs["caudalMasico"]=self.caudal.value
            kwargs["caudalMolar"]=self.caudalMolar.value
            kwargs["caudalVolumetrico"]=self.caudalVol.value
            kwargs["notas"]=self.PageNotas.notas.toHtml()
            
            variable, fracciones=self.composicionEntrada()
            kwargs[variable]=fracciones
            
            
        if not self.evaluate.isRunning():
            self.evaluate.start(self.corriente, kwargs)
        
        
class Corriente_Dialog(QtGui.QDialog, Ui_corriente):
    """Dialogo de definición de formatos de líneas"""
    Changed = QtCore.pyqtSignal(Corriente)
    corriente=Corriente()
    def __init__(self, corriente=Corriente(), readOnly=False, parent=None):
        layout=QtGui.QHBoxLayout()
        self.status=Status()
        layout.addWidget(self.status)
        buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok|QtGui.QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        layout.addWidget(buttonBox)
        super(Corriente_Dialog, self).__init__(corriente, readOnly)
        self.setWindowTitle(QtGui.QApplication.translate("pychemqt", "Edit stream properties"))
        self.layout().addLayout(layout)

        
class PsychroDefinition(QtGui.QWidget):
    """Widget for stream definition as humid air input"""
    Changed = QtCore.pyqtSignal(PsyState)
    parameters = ["tdb", "twb", "tdp", "w", "mu", "HR", "v", "h", "Pv", "Xa", "Xw"]
    stream = PsyStream
    
    def __init__(self, psystream=None, readOnly=False, parent=None):
        super(PsychroDefinition, self).__init__(parent)
        self.readOnly=readOnly
        layout=QtGui.QGridLayout(self)
        
        self.inputs = PsychroInput()
        self.inputs.stateChanged.connect(self.rellenar)
        layout.addWidget(self.inputs, 1, 1, 1, 2)

        layout.addItem(QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Fixed,
                                         QtGui.QSizePolicy.Fixed), 1, 3)
        layout.addItem(QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Fixed,
                                         QtGui.QSizePolicy.Fixed), 2, 1)
        
        vlayout = QtGui.QVBoxLayout()
        layout.addLayout(vlayout,1, 4, 6, 1)
        vlayout.addItem(QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Expanding,
                                          QtGui.QSizePolicy.Expanding))
        groupbox = QtGui.QGroupBox(QtGui.QApplication.translate(
            "pychemqt", "Calculated properties"))
        vlayout.addWidget(groupbox)
        lytGroup = QtGui.QGridLayout(groupbox)
        lytGroup.addWidget(QtGui.QLabel("Tdb"),1,1)
        self.tdb = Entrada_con_unidades(unidades.Temperature, readOnly=True)
        lytGroup.addWidget(self.tdb, 1, 2)
        lytGroup.addWidget(QtGui.QLabel("Twb"), 2, 1)
        self.twb = Entrada_con_unidades(unidades.Temperature, readOnly=True)
        lytGroup.addWidget(self.twb, 2, 2)
        lytGroup.addWidget(QtGui.QLabel("Tdp"), 3, 1)
        self.tdp = Entrada_con_unidades(unidades.Temperature, readOnly=True)
        lytGroup.addWidget(self.tdp, 3, 2)
        lytGroup.addWidget(QtGui.QLabel(QtGui.QApplication.translate(
            "pychemqt", "Absolute humidity")), 4, 1)
        massUnit = unidades.Mass(None).text()+"/"+unidades.Mass(None).text()
        self.w = Entrada_con_unidades(float, readOnly=True, textounidad=massUnit)
        lytGroup.addWidget(self.w, 4, 2)
        lytGroup.addWidget(QtGui.QLabel(QtGui.QApplication.translate(
            "pychemqt", "Degree of saturation")), 5, 1)
        self.mu=Entrada_con_unidades(float, readOnly=True, textounidad="%")
        lytGroup.addWidget(self.mu, 5, 2)
        lytGroup.addWidget(QtGui.QLabel(QtGui.QApplication.translate(
            "pychemqt", "Relative humidity")), 6, 1)
        self.HR=Entrada_con_unidades(float, readOnly=True, textounidad="%")
        lytGroup.addWidget(self.HR, 6, 2)
        lytGroup.addWidget(QtGui.QLabel(QtGui.QApplication.translate(
            "pychemqt", "Volume")), 7, 1)
        self.v=Entrada_con_unidades(unidades.SpecificVolume, readOnly=True)
        lytGroup.addWidget(self.v, 7, 2)
        lytGroup.addWidget(QtGui.QLabel(QtGui.QApplication.translate(
            "pychemqt", "Enthalpy")), 8, 1)
        self.h=Entrada_con_unidades(unidades.Enthalpy, readOnly=True)
        lytGroup.addWidget(self.h, 8, 2)
        lytGroup.addWidget(QtGui.QLabel(QtGui.QApplication.translate(
            "pychemqt", "Vapour Pressure")), 9, 1)
        self.Pv=Entrada_con_unidades(unidades.Pressure, readOnly=True)
        lytGroup.addWidget(self.Pv, 9, 2)
        lytGroup.addWidget(QtGui.QLabel(QtGui.QApplication.translate(
            "pychemqt", "Air fraction")), 10, 1)
        self.Xa=Entrada_con_unidades(float, readOnly=True)
        lytGroup.addWidget(self.Xa, 10, 2)
        lytGroup.addWidget(QtGui.QLabel(QtGui.QApplication.translate(
            "pychemqt", "Water fraction")), 11, 1)
        self.Xw=Entrada_con_unidades(float, readOnly=True)
        lytGroup.addWidget(self.Xw, 11, 2)
        vlayout.addItem(QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Expanding,
                                          QtGui.QSizePolicy.Expanding))

        layout.addWidget(QtGui.QLabel(QtGui.QApplication.translate(
            "pychemqt", "Mass Flow")), 3, 1)
        self.caudal=Entrada_con_unidades(unidades.MassFlow, readOnly=readOnly)
        self.caudal.valueChanged.connect(partial(self.updatekwargsFlow, "caudal"))
        layout.addWidget(self.caudal, 3, 2)
        layout.addWidget(QtGui.QLabel(QtGui.QApplication.translate(
            "pychemqt", "Molar Flow")), 4, 1)
        self.caudalMolar=Entrada_con_unidades(unidades.MolarFlow, readOnly=readOnly)
        self.caudalMolar.valueChanged.connect(partial(self.updatekwargsFlow, "caudalMolar"))
        layout.addWidget(self.caudalMolar, 4, 2)
        layout.addWidget(QtGui.QLabel(QtGui.QApplication.translate(
            "pychemqt", "Volumetric Flow")), 5, 1)
        self.caudalVolumetrico=Entrada_con_unidades(unidades.VolFlow, readOnly=readOnly)
        self.caudalVolumetrico.valueChanged.connect(partial(self.updatekwargsFlow, "caudalVolumetrico"))
        layout.addWidget(self.caudalVolumetrico, 5, 2)
        layout.addItem(QtGui.QSpacerItem(5, 5, QtGui.QSizePolicy.Expanding,
                                         QtGui.QSizePolicy.Expanding),9,2)

        self.setReadOnly(readOnly)
        self.inputs.updateInputs(0)
        
        if psystream:
            self.setStream(psystream)

    def setStream(self, stream):
        self.stream=stream
        if stream:
            self.rellenar(stream)

    def setReadOnly(self, readOnly):
        self.inputs.setReadOnly(readOnly)
        self.caudal.setReadOnly(readOnly)
        self.caudalMolar.setReadOnly(readOnly)
        self.caudalVolumetrico.setReadOnly(readOnly)

    def calculo(self, key, value):
        self.stream(**{key: value})
        if self.stream:
            self.rellenar(self.stream)
        
    def rellenar(self, stream):
        self.inputs.setState(stream.state)
        if stream:
            for par in self.parameters:
                self.__getattribute__(par).setValue(stream.__getattribute__(par))
        self.rellenarFlow(stream)

    def rellenarFlow(self, stream):
        for arg in ("caudal", "caudalMolar", "caudalVolumetrico"):
            if stream.kwargs[arg]:
                self.__getattribute__(arg).setValue(stream.kwargs[arg])
            else:
                self.__getattribute__(arg).clear()
    
    def updatekwargsFlow(self, key, value):
        self.stream.updatekwargsFlow(key, value)
        self.rellenarFlow(self.stream)

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    
#    distribucion=[[17.5, 0.02],
#                                [22.4, 0.03], 
#                                [26.2,  0.05], 
#                                [31.8,  0.1],  
#                                [37, 0.1],
#                                [42.4, 0.1], 
#                                [48, 0.1], 
#                                [54, 0.1], 
#                                [60, 0.1], 
#                                [69, 0.1], 
#                                [81.3, 0.1], 
#                                [96.5, 0.05], 
#                                [109, 0.03], 
#                                [127, 0.02]]
#    solido=Solid([638], [100], distribucion)
#
#    mezcla=Corriente(340, 1, 1000, Mezcla([10, 38, 22, 61], [.3, 0.5, 0.05, 0.15]), notas="Corriente de ejemplo")
#    mezcla=Corriente(340, 1, 1000, Mezcla([475, 7, 62], [.3, 0.5, 0.2, ]), solido, notas="Corriente de ejemplo")
#    agua=Corriente(T=300, P=1e5, caudalMasico=1, fraccionMolar=[1.])
#    agua(caudalSolido=[35], diametroMedio=0.0002, notas="Corriente de agua de ejemplo")
#    print agua.solido
#    diametros=[17.5e-5, 22.4e-5, 26.2e-5, 31.8e-5, 37e-5, 42.4e-5, 48e-5, 54e-5, 60e-5, 69e-5, 81.3e-5, 96.5e-5, 109e-5, 127e-5]
#    fracciones=[0.02, 0.03, 0.05, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.05, 0.03, 0.02]
#    solido=Solid(caudalSolido=[0.01], distribucion_diametro=diametros, distribucion_fraccion=fracciones)
#    corriente=Corriente(T=300, P=101325, caudalMasico=1.,  fraccionMolar=[1.], solido=solido)

    corriente=Corriente(T=340, P=101325, caudalMasico=0.01, ids=[10, 38, 22, 61], fraccionMolar=[.3, 0.5, 0.05, 0.15])
#    corriente=Corriente(caudalMasico=0.01, ids=[10, 38, 22, 61], fraccionMolar=[.3, 0.5, 0.05, 0.15])
    dialogo = Ui_corriente(corriente)
    dialogo.show()

#    aire=PsyStream(caudal=5, tdb=300, HR=50)
#    corriente=PsychroDefinition(aire)
#    corriente.show()

#    corriente = Dialog_Distribucion()
#    corriente.show()

#    diametros=[17.5e-5, 22.4e-5, 26.2e-5, 31.8e-5, 37e-5, 42.4e-5, 48e-5, 54e-5, 60e-5, 69e-5, 81.3e-5, 96.5e-5, 109e-5, 127e-5]
#    fracciones=[0.02, 0.03, 0.05, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.05, 0.03, 0.02]
#    solido=Solid(caudalSolido=[0.01], distribucion_diametro=diametros, distribucion_fraccion=fracciones)
#    corriente = SolidDefinition(solido)
#    corriente.show()

#    corriente=Corriente(T=300., x=0.8, caudalMasico=1., fraccionMolar=[1.])
#    dialogo = Ui_corriente(corriente)
#    dialogo.show()

#    corriente=Corriente(ids=[10, 38, 22, 61], fraccionMolar=[.3, 0.5, 0.05, 0.15])
#    corriente=Corriente(P=101325)
#    dialogo = StreamDefinition(corriente)
#    dialogo.show()
    
    sys.exit(app.exec_())
