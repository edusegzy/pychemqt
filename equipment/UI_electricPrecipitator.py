#!/usr/bin/python
# -*- coding: utf-8 -*-

###############################################################################
# Electric precipitator equipment dialog
###############################################################################

from functools import partial

from PyQt4 import QtGui

from lib.unidades import DeltaP, PotencialElectric, Area
from equipment.gas_solid import ElectricPrecipitator
from equipment.parents import UI_equip
from UI.widgets import Entrada_con_unidades


class UI_equipment(UI_equip):
    """Electric precipitator equipment edition dialog"""
    Equipment = ElectricPrecipitator()

    def __init__(self, equipment=None, parent=None):
        """
        equipment: Initial equipment instance to model
        """
        super(UI_equipment, self).__init__(ElectricPrecipitator, entrada=False,
                                           parent=parent)

        # Calculate tab
        lyt_Calc = QtGui.QGridLayout(self.tabCalculo)
        lyt_Calc.addWidget(QtGui.QLabel(QtGui.QApplication.translate(
            "pychemqt", "Mode")), 1, 1)
        self.metodo = QtGui.QComboBox()
        for txt in self.Equipment.TEXT_TIPO:
            self.metodo.addItem(txt)
        self.metodo.currentIndexChanged.connect(self.tipoCalculoCambiado)
        lyt_Calc.addWidget(self.metodo, 1, 2, 1, 4)
        lyt_Calc.addItem(QtGui.QSpacerItem(
            20, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed),
            2, 1, 1, 6)

        lyt_Calc.addWidget(QtGui.QLabel(QtGui.QApplication.translate(
            "pychemqt", "Area")), 3, 1)
        self.area = Entrada_con_unidades(Area, resaltado=True)
        self.area.valueChanged.connect(partial(self.changeParams, "area"))
        lyt_Calc.addWidget(self.area, 3, 2)
        lyt_Calc.addWidget(QtGui.QLabel(QtGui.QApplication.translate(
            "pychemqt", "Allowable efficiency")), 4, 1)
        self.rendimientoAdmisible = Entrada_con_unidades(float,  readOnly=True)
        self.rendimientoAdmisible.valueChanged.connect(
            partial(self.changeParams, "rendimientoAdmisible"))
        lyt_Calc.addWidget(self.rendimientoAdmisible, 4, 2)
        lyt_Calc.addItem(QtGui.QSpacerItem(
            20, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed),
            5, 1, 1, 6)

        lyt_Calc.addWidget(QtGui.QLabel(QtGui.QApplication.translate(
            "pychemqt", "Dielectric constant")), 6, 1)
        self.epsilon = Entrada_con_unidades(float)
        self.epsilon.valueChanged.connect(partial(self.changeParams, "epsilon"))
        lyt_Calc.addWidget(self.epsilon, 6, 2)
        lyt_Calc.addWidget(QtGui.QLabel(QtGui.QApplication.translate(
            "pychemqt", "Charging field")), 7, 1)
        self.potencialCarga = Entrada_con_unidades(PotencialElectric)
        self.potencialCarga.valueChanged.connect(
            partial(self.changeParams, "potencialCarga"))
        lyt_Calc.addWidget(self.potencialCarga, 7, 2)
        lyt_Calc.addWidget(QtGui.QLabel(QtGui.QApplication.translate(
            "pychemqt", "Collecting field")), 8, 1)
        self.potencialDescarga = Entrada_con_unidades(PotencialElectric)
        self.potencialDescarga.valueChanged.connect(
            partial(self.changeParams, "potencialDescarga"))
        lyt_Calc.addWidget(self.potencialDescarga, 8, 2)
        lyt_Calc.addWidget(QtGui.QLabel(QtGui.QApplication.translate(
            "pychemqt", "Pressure drop")), 9, 1)
        self.deltaP = Entrada_con_unidades(DeltaP)
        self.deltaP.valueChanged.connect(partial(self.changeParams, "deltaP"))
        lyt_Calc.addWidget(self.deltaP, 9, 2)
        lyt_Calc.addItem(QtGui.QSpacerItem(
            20, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding),
            10, 1, 1, 6)

        groupbox = QtGui.QGroupBox(QtGui.QApplication.translate(
            "pychemqt", "Result"))
        lyt_Calc.addWidget(groupbox, 11, 1, 1, 5)
        lyt = QtGui.QGridLayout(groupbox)
        lyt.addWidget(QtGui.QLabel(QtGui.QApplication.translate(
            "pychemqt", "Area")), 0, 1)
        self.areaCalculada = Entrada_con_unidades(Area, retornar=False)
        self.areaCalculada.setReadOnly(True)
        lyt.addWidget(self.areaCalculada, 0, 2)
        lyt.addWidget(QtGui.QLabel(QtGui.QApplication.translate(
            "pychemqt", "Efficiency")), 1, 1)
        self.rendimiento = Entrada_con_unidades(float, readOnly=True)
        lyt.addWidget(self.rendimiento, 1, 2)
        lyt_Calc.addItem(QtGui.QSpacerItem(
            20, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding),
            12, 1, 1, 6)

        # Output tab
        self.addSalida(QtGui.QApplication.translate("pychemqt", "Filtered gas"))
        self.addSalida(
            QtGui.QApplication.translate("pychemqt", "Collected solids"))

        if equipment:
            self.setEquipment(equipment)

    def tipoCalculoCambiado(self, tipo_calculo):
        self.area.setReadOnly(tipo_calculo)
        self.area.setResaltado(not tipo_calculo)
        self.rendimientoAdmisible.setReadOnly(not tipo_calculo)
        self.rendimientoAdmisible.setResaltado(tipo_calculo)
        self.changeParams("metodo", tipo_calculo)


if __name__ == "__main__":
    import sys
    from lib.corriente import Corriente, Solid
    app = QtGui.QApplication(sys.argv)
    diametros = [17.5e-6, 22.4e-6, 26.2e-6, 31.8e-6, 37e-6, 42.4e-6, 48e-6,
                 54e-6, 60e-6, 69e-6, 81.3e-6, 96.5e-6, 109e-6, 127e-6]
    fracciones = [0.02, 0.03, 0.05, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1,
                  0.05, 0.03, 0.02]
    solido = Solid(caudalSolido=[0.1], distribucion_diametro=diametros,
                   distribucion_fraccion=fracciones)
    corriente = Corriente(T=300, P=101325, caudalMasico=1.,
                          fraccionMolar=[1.], solido=solido)
    precipitador = ElectricPrecipitator(entrada=corriente, metodo=1,
                                        rendimientoAdmisible=0.9)
    dialogo = UI_equipment(precipitador)
    dialogo.show()
    sys.exit(app.exec_())
