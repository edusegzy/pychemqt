#!/usr/bin/python
# -*- coding: utf-8 -*-

###############################################################################
# Flash phase separator equipment dialog
###############################################################################

from functools import partial

from PyQt4 import QtGui

from lib.unidades import Length, Mass, Volume, Density, Currency
from tools.costIndex import CostData
from equipment.parents import UI_equip
from equipment.distillation import Flash
from UI.widgets import Entrada_con_unidades


class UI_equipment (UI_equip):
    """Flash phase separator equipment edition dialog"""
    Equipment = Flash()

    def __init__(self, equipment=None, parent=None):
        """
        equipment: Initial equipment instance to model
        """
        super(UI_equipment, self).__init__(Flash, entrada=False, parent=parent)

        # Calculate tab
        lyt_Calc = QtGui.QGridLayout(self.tabCalculo)
        lyt_Calc.addWidget(QtGui.QLabel(
            QtGui.QApplication.translate("pychemqt", "Method")), 0, 1)
        self.flash = QtGui.QComboBox()
        for txt in self.Equipment.TEXT_FLASH:
            self.flash.addItem(txt)
        self.flash.currentIndexChanged.connect(
            partial(self.changeParams, "metodo"))
        lyt_Calc.addWidget(self.flash, 0, 2)
        lyt_Calc.addItem(QtGui.QSpacerItem(
            20, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding),
            1, 1, 1, 6)

        # Cost tab
        lyt_Cost = QtGui.QGridLayout(self.tabCostos)
        lyt_Cost.addWidget(QtGui.QLabel(
            QtGui.QApplication.translate("pychemqt", "Orientation")), 0, 1)
        self.orientacion = QtGui.QComboBox()
        for txt in self.Equipment.TEXT_ORIENTATION:
            self.orientacion.addItem(txt)
        self.orientacion.currentIndexChanged.connect(
            partial(self.changeParamsCoste, "orientacion"))
        lyt_Cost.addWidget(self.orientacion, 0, 2)
        lyt_Cost.addWidget(QtGui.QLabel(
            QtGui.QApplication.translate("pychemqt", "Material")), 1, 1)
        self.material = QtGui.QComboBox()
        for txt in self.Equipment.TEXT_MATERIAL:
            self.material.addItem(txt)
        self.material.currentIndexChanged.connect(
            partial(self.changeParamsCoste, "material"))
        lyt_Cost.addWidget(self.material, 1, 2, 1, 4)
        lyt_Cost.addWidget(QtGui.QLabel(
            QtGui.QApplication.translate("pychemqt", "Density")), 2, 4)
        self.Densidad = Entrada_con_unidades(Density, "DenLiq")
        self.Densidad.valueChanged.connect(
            partial(self.changeParamsCoste, "densidad"))
        lyt_Cost.addWidget(self.Densidad, 2, 5)
        lyt_Cost.addWidget(QtGui.QLabel(
            QtGui.QApplication.translate("pychemqt", "Diameter")), 2, 1)
        self.diametro = Entrada_con_unidades(Length)
        self.diametro.valueChanged.connect(
            partial(self.changeParamsCoste, "diametro"))
        lyt_Cost.addWidget(self.diametro, 2, 2)
        lyt_Cost.addWidget(QtGui.QLabel(
            QtGui.QApplication.translate("pychemqt", "Length")), 3, 1)
        self.longitud = Entrada_con_unidades(Length)
        self.longitud.valueChanged.connect(
            partial(self.changeParamsCoste, "longitud"))
        lyt_Cost.addWidget(self.longitud, 3, 2)
        lyt_Cost.addWidget(QtGui.QLabel(
            QtGui.QApplication.translate("pychemqt", "Thickness")), 4, 1)
        self.espesor = Entrada_con_unidades(Length, "Thickness")
        self.espesor.valueChanged.connect(
            partial(self.changeParamsCoste, "espesor"))
        lyt_Cost.addWidget(self.espesor, 4, 2)
        lyt_Cost.addWidget(QtGui.QLabel(
            QtGui.QApplication.translate("pychemqt", "Head type")), 5, 1)
        self.cabeza = QtGui.QComboBox()
        for txt in self.Equipment.TEXT_HEAD:
            self.cabeza.addItem(txt)
        self.cabeza.currentIndexChanged.connect(
            partial(self.changeParamsCoste, "cabeza"))
        lyt_Cost.addWidget(self.cabeza, 5, 2)
        lyt_Cost.addWidget(QtGui.QLabel(
            QtGui.QApplication.translate("pychemqt", "Head Thickness")), 6, 1)
        self.espesor_cabeza = Entrada_con_unidades(Length, "Thickness")
        self.espesor_cabeza.valueChanged.connect(
            partial(self.changeParamsCoste, "espesor_cabeza"))
        lyt_Cost.addWidget(self.espesor_cabeza, 6, 2)
        lyt_Cost.addWidget(QtGui.QLabel(QtGui.QApplication.translate(
            "pychemqt", "Straight flange length")), 7, 1)
        self.reborde = Entrada_con_unidades(Length)
        self.reborde.valueChanged.connect(
            partial(self.changeParamsCoste, "reborde"))
        lyt_Cost.addWidget(self.reborde, 7, 2)
        lyt_Cost.addWidget(QtGui.QLabel(
            QtGui.QApplication.translate("pychemqt", "Volume")), 6, 4)
        self.Volumen = Entrada_con_unidades(Volume, "VolLiq", retornar=False)
        self.Volumen.setReadOnly(True)
        lyt_Cost.addWidget(self.Volumen, 6, 5)
        lyt_Cost.addWidget(QtGui.QLabel(
            QtGui.QApplication.translate("pychemqt", "Weight")), 7, 4)
        self.Peso = Entrada_con_unidades(Mass, readOnly=True)
        lyt_Cost.addWidget(self.Peso, 7, 5)
        lyt_Cost.addItem(QtGui.QSpacerItem(
            10, 10, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed),
            2, 3, 6, 1)
        lyt_Cost.addItem(QtGui.QSpacerItem(
            20, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding),
            8, 0, 1, 6)

        self.Costos = CostData(self.Equipment)
        self.Costos.valueChanged.connect(self.changeParamsCoste)
        lyt_Cost.addWidget(self.Costos, 9, 1, 2, 5)

        lyt_Cost.addItem(QtGui.QSpacerItem(
            20, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding),
            11, 0, 1, 6)
        group = QtGui.QGroupBox(
            QtGui.QApplication.translate("pychemqt", "Stimated Costs"))
        lyt_Cost.addWidget(group, 12, 1, 1, 5)
        layout = QtGui.QGridLayout(group)
        layout.addWidget(QtGui.QLabel(
            QtGui.QApplication.translate("pychemqt", "Purchase costs")), 0, 1)
        self.C_adq = Entrada_con_unidades(Currency, retornar=False,
                                          tolerancia=8, decimales=2)
        self.C_adq.setReadOnly(True)
        layout.addWidget(self.C_adq, 0, 2)
        layout.addWidget(QtGui.QLabel(
            QtGui.QApplication.translate("pychemqt", "Installed costs")), 1, 1)
        self.C_inst = Entrada_con_unidades(Currency, retornar=False,
                                           tolerancia=8, decimales=2)
        self.C_inst.setReadOnly(True)
        layout.addWidget(self.C_inst, 1, 2)
        lyt_Cost.addItem(QtGui.QSpacerItem(
            20, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding),
            13, 0, 1, 6)

        # Output tab
        self.addSalida(QtGui.QApplication.translate("pychemqt", "Destilate"))
        self.addSalida(QtGui.QApplication.translate("pychemqt", "Residue"))

        if equipment:
            self.setEquipment(equipment)


if __name__ == "__main__":
    import sys
    from lib.corriente import Corriente
    app = QtGui.QApplication(sys.argv)
    entrada = Corriente(T=340, P=101325, caudalMasico=0.01,
                        ids=[10, 38, 22, 61],
                        fraccionMolar=[.3, 0.5, 0.05, 0.15])
    flash = Flash(entrada=entrada)
    dialogo = UI_equipment(flash)
    dialogo.show()
    sys.exit(app.exec_())
