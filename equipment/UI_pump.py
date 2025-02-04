#!/usr/bin/python
# -*- coding: utf-8 -*-
###############################################################################
# Pump equipment dialog
###############################################################################

from functools import partial

from PyQt4 import QtGui

from lib.unidades import Pressure, Length, Power, VolFlow, Currency
from tools.costIndex import CostData
from equipment.parents import UI_equip
from equipment.pump import Pump
from UI import bombaCurva
from UI.widgets import Entrada_con_unidades


class UI_equipment(UI_equip):
    """Pump equipment edition dialog"""
    Equipment = Pump()

    def __init__(self, equipment=None, parent=None):
        """
        equipment: Initial equipment instance to model
        """
        super(UI_equipment, self).__init__(Pump, entrada=False, salida=False,
                                           parent=parent)
        self.curva = [0, 0, []]

        # Calculate tab
        lyt = QtGui.QGridLayout(self.tabCalculo)
        lyt.addWidget(QtGui.QLabel(
            QtGui.QApplication.translate("pychemqt", "Output Pressure")), 1, 1)
        self.Pout = Entrada_con_unidades(Pressure)
        self.Pout.valueChanged.connect(partial(self.cambiar_data, "Pout"))
        lyt.addWidget(self.Pout, 1, 2)
        lyt.addWidget(QtGui.QLabel(QtGui.QApplication.translate(
            "pychemqt", "Pressure increase")), 2, 1)
        self.deltaP = Entrada_con_unidades(Pressure)
        self.deltaP.valueChanged.connect(partial(self.cambiar_data, "deltaP"))
        lyt.addWidget(self.deltaP, 2, 2)
        lyt.addWidget(QtGui.QLabel(
            QtGui.QApplication.translate("pychemqt", "Head")), 3, 1)
        self.Carga = Entrada_con_unidades(Length, "Head")
        self.Carga.valueChanged.connect(partial(self.cambiar_data, "Carga"))
        lyt.addWidget(self.Carga, 3, 2)
        lyt.addItem(QtGui.QSpacerItem(
            10, 10, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed),
            4, 1, 1, 2)
        self.usarCurva = QtGui.QCheckBox(
            QtGui.QApplication.translate("pychemqt", "Pump curve"))
        self.usarCurva.toggled.connect(self.usarCurvaToggled)
        lyt.addWidget(self.usarCurva, 5, 1, 2, 2)
        lyt.addWidget(QtGui.QLabel(
            QtGui.QApplication.translate("pychemqt", "Efficiency")), 7, 1)
        self.rendimiento = Entrada_con_unidades(float, min=0, max=1,
                                                spinbox=True, step=0.01)
        self.rendimiento.valueChanged.connect(
            partial(self.cambiar_data, "rendimiento"))
        lyt.addWidget(self.rendimiento, 7, 2)
        lyt.addItem(QtGui.QSpacerItem(
            20, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding),
            8, 1, 1, 6)

        self.groupBox_Curva = QtGui.QGroupBox(
            QtGui.QApplication.translate("pychemqt", "Pump curve"))
        self.groupBox_Curva.setEnabled(False)
        lyt.addWidget(self.groupBox_Curva, 5, 4, 3, 1)
        layout = QtGui.QGridLayout(self.groupBox_Curva)

        self.bottonCurva = QtGui.QPushButton(
            QtGui.QApplication.translate("pychemqt", "Curve"))
        self.bottonCurva.clicked.connect(self.bottonCurva_clicked)
        layout.addWidget(self.bottonCurva, 1, 1, 1, 2)
        layout.addWidget(QtGui.QLabel(
            QtGui.QApplication.translate("pychemqt", "Variable")), 2, 1)
        self.incognita = QtGui.QComboBox(self.tabCalculo)
        self.incognita.setToolTip(QtGui.QApplication.translate(
            "pychemqt",
            "If use curve, it can calculate the head or the flowrate, in that \
case it override flow of input stream"))
        self.incognita.addItem(
            QtGui.QApplication.translate("pychemqt", "Output pressure"))
        self.incognita.addItem(
            QtGui.QApplication.translate("pychemqt", "Flowrate"))
        self.incognita.currentIndexChanged.connect(
            partial(self.cambiar_data, "incognita"))
        layout.addWidget(self.incognita, 2, 2)
        layout.addWidget(QtGui.QLabel(
            QtGui.QApplication.translate("pychemqt", "Diameter")), 3, 1)
        self.diametro = Entrada_con_unidades(float, spinbox=True, step=0.1,
                                             suffix='"')
        self.diametro.valueChanged.connect(
            partial(self.cambiar_data, "diametro"))
        layout.addWidget(self.diametro, 3, 2)
        layout.addWidget(QtGui.QLabel(
            QtGui.QApplication.translate("pychemqt", "RPM")), 4, 1)
        self.velocidad = Entrada_con_unidades(int, spinbox=True, step=1)
        self.velocidad.valueChanged.connect(
            partial(self.cambiar_data, "velocidad"))
        layout.addWidget(self.velocidad, 4, 2)

        group = QtGui.QGroupBox(
            QtGui.QApplication.translate("pychemqt", "Results"))
        layout = QtGui.QGridLayout(group)
        layout.addWidget(QtGui.QLabel(
            QtGui.QApplication.translate("pychemqt", "Power")), 0, 0)
        self.power = Entrada_con_unidades(Power, retornar=False, readOnly=True)
        layout.addWidget(self.power, 0, 1)
        layout.addWidget(QtGui.QLabel(
            QtGui.QApplication.translate("pychemqt", "Output Pressure")), 0, 4)
        self.PoutCalculada = Entrada_con_unidades(Pressure, retornar=False)
        self.PoutCalculada.setReadOnly(True)
        layout.addWidget(self.PoutCalculada, 0, 5)
        layout.addWidget(QtGui.QLabel(
            QtGui.QApplication.translate("pychemqt", "Flowrate")), 1, 0)
        self.volflow = Entrada_con_unidades(VolFlow, "QLiq", retornar=False)
        self.volflow.setReadOnly(True)
        layout.addWidget(self.volflow, 1, 1)
        layout.addWidget(QtGui.QLabel(
            QtGui.QApplication.translate("pychemqt", "Head")), 1, 4)
        self.headCalculada = Entrada_con_unidades(Length, retornar=False)
        self.headCalculada.setReadOnly(True)
        layout.addWidget(self.headCalculada, 1, 5)
        layout.addWidget(QtGui.QLabel(
            QtGui.QApplication.translate("pychemqt", "Efficiency")), 2, 0)
        self.rendimientoCalculado = Entrada_con_unidades(float, width=60)
        self.rendimientoCalculado.setReadOnly(True)
        layout.addWidget(self.rendimientoCalculado, 2, 1)
        layout.addItem(QtGui.QSpacerItem(
            40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum),
            0, 3)
        lyt.addWidget(group, 9, 1, 1, 6)
        lyt.addItem(QtGui.QSpacerItem(
            20, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding),
            10, 1, 1, 6)

        # Design tab
        self.tabDiseno = QtGui.QWidget()
        lyt = QtGui.QGridLayout(self.tabDiseno)
        lyt.addWidget(QtGui.QLabel(QtGui.QApplication.translate(
            "pychemqt",
            "Not implemented\n\nRef: Gülich - Centrifugal Pumps", None,
            QtGui.QApplication.UnicodeUTF8)), 0, 0)
        self.tabWidget.insertTab(
            2, self.tabDiseno,
            QtGui.QApplication.translate("pychemqt", "Design"))

        # Cost tab
        lyt = QtGui.QGridLayout(self.tabCostos)
        lyt.addWidget(QtGui.QLabel(
            QtGui.QApplication.translate("pychemqt", "Pump type")), 1, 1)
        self.tipo_bomba = QtGui.QComboBox()
        for txt in self.Equipment.TEXT_BOMBA:
            self.tipo_bomba.addItem(txt)
        self.tipo_bomba.currentIndexChanged.connect(
            self.bomba_currentIndexChanged)
        lyt.addWidget(self.tipo_bomba, 1, 2)
        lyt.addWidget(QtGui.QLabel(
            QtGui.QApplication.translate("pychemqt", "Centrifuge type")), 2, 1)
        self.tipo_centrifuga = QtGui.QComboBox()
        for txt in self.Equipment.TEXT_CENTRIFUGA:
            self.tipo_centrifuga.addItem(txt)
        self.tipo_centrifuga.currentIndexChanged.connect(
            partial(self.changeParamsCoste, "tipo_centrifuga"))
        lyt.addWidget(self.tipo_centrifuga, 2, 2)
        lyt.addWidget(QtGui.QLabel(
            QtGui.QApplication.translate("pychemqt", "Material")), 3, 1)
        self.material = QtGui.QComboBox()
        for txt in self.Equipment.TEXT_MATERIAL:
            self.material.addItem(txt)
        self.material.currentIndexChanged.connect(
            partial(self.changeParamsCoste, "material"))
        lyt.addWidget(self.material, 3, 2)
        lyt.addWidget(QtGui.QLabel(
            QtGui.QApplication.translate("pychemqt", "Motor type")), 4, 1)
        self.motor = QtGui.QComboBox()
        for txt in self.Equipment.TEXT_MOTOR:
            self.motor.addItem(txt)
        self.motor.currentIndexChanged.connect(
            partial(self.changeParamsCoste, "motor"))
        lyt.addWidget(self.motor, 4, 2)
        lyt.addWidget(QtGui.QLabel(
            QtGui.QApplication.translate("pychemqt", "Motor RPM")), 5, 1)
        self.rpm = QtGui.QComboBox(self.tabCostos)
        for txt in self.Equipment.TEXT_RPM:
            self.rpm.addItem(txt)
        self.rpm.currentIndexChanged.connect(
            partial(self.changeParamsCoste, "rpm"))
        lyt.addWidget(self.rpm, 5, 2)

        self.Costos = CostData(self.Equipment)
        self.Costos.valueChanged.connect(self.changeParamsCoste)
        lyt.addWidget(self.Costos, 6, 1, 2, 4)

        lyt.addItem(QtGui.QSpacerItem(
            20, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding),
            7, 1, 1, 4)
        group = QtGui.QGroupBox(
            QtGui.QApplication.translate("pychemqt", "Stimated costs"))
        lyt.addWidget(group, 8, 1, 1, 4)
        layout = QtGui.QGridLayout(group)
        layout.addWidget(QtGui.QLabel(
            QtGui.QApplication.translate("pychemqt", "Pump")), 0, 0)
        self.C_bomba = Entrada_con_unidades(Currency, retornar=False)
        self.C_bomba.setReadOnly(True)
        layout.addWidget(self.C_bomba, 0, 1)
        layout.addWidget(QtGui.QLabel(
            QtGui.QApplication.translate("pychemqt", "Motor")), 1, 0)
        self.C_motor = Entrada_con_unidades(Currency, retornar=False)
        self.C_bomba.setReadOnly(True)
        layout.addWidget(self.C_motor, 1, 1)
        layout.addWidget(QtGui.QLabel(
            QtGui.QApplication.translate("pychemqt", "Purchase cost")), 0, 4)
        self.C_adq = Entrada_con_unidades(Currency, retornar=False)
        self.C_adq.setReadOnly(True)
        layout.addWidget(self.C_adq, 0, 5)
        layout.addWidget(QtGui.QLabel(
            QtGui.QApplication.translate("pychemqt", "Installed cost")), 1, 4)
        self.C_inst = Entrada_con_unidades(Currency, retornar=False)
        self.C_inst.setReadOnly(True)
        layout.addWidget(self.C_inst, 1, 5)
        lyt.addItem(QtGui.QSpacerItem(
            20, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed),
            9, 1, 1, 4)

        if equipment:
            self.setEquipment(equipment)

    def cambiar_data(self, parametro, valor):
        if parametro == "Pout":
            self.Carga.clear()
            self.deltaP.clear()
        elif parametro == "deltaP":
            self.Pout.clear()
            self.Carga.clear()
        else:
            self.Pout.clear()
            self.deltaP.clear()
        self.changeParams(parametro, valor)

    def bomba_currentIndexChanged(self, int):
        self.tipo_centrifuga.setDisabled(int)
        self.changeParamsCoste("tipo_bomba", int)

    def usarCurvaToggled(self, int):
        self.groupBox_Curva.setEnabled(int)
        self.rendimiento.setReadOnly(int)
        self.changeParams("usarCurva", int)

    def bottonCurva_clicked(self):
        dialog = bombaCurva.Ui_bombaCurva(
            self.Equipment.kwargs["curvaCaracteristica"], self)
        if dialog.exec_():
            self.curva = dialog.curva
            self.diametro.setValue(dialog.curva[0])
            self.velocidad.setValue(dialog.curva[1])
            self.changeParams("curvaCaracteristica", dialog.curva)


if __name__ == "__main__":
    import sys
    from lib.corriente import Corriente
    app = QtGui.QApplication(sys.argv)
    agua = Corriente(T=300, P=101325, caudalMasico=1, fraccionMolar=[1.])
    bomba = Pump(entrada=agua, rendimiento=0.75, deltaP=2001325, tipo_bomba=1)
    dialogBomba = UI_equipment(equipment=bomba)
    dialogBomba.show()
    sys.exit(app.exec_())
