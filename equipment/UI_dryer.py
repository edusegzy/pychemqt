#!/usr/bin/python
# -*- coding: utf-8 -*-

###############################################################################
# Solid dryer equipment dialog
###############################################################################

from functools import partial

from PyQt4 import QtGui

from equipment.gas_solid_liquid import Dryer
from lib import unidades
from equipment.parents import UI_equip
from UI.widgets import Entrada_con_unidades


class UI_equipment(UI_equip):
    """Solid dryer equipment edition dialog"""
    Equipment = Dryer()

    def __init__(self, equipment=None, parent=None):
        """
        equipment: Initial equipment instance to model
        """
        super(UI_equipment, self).__init__(Dryer, parent=parent)

        # Input tab
        self.addEntrada(QtGui.QApplication.translate("pychemqt", "Humid Solid"),
                        "entradaSolido")
        self.addEntrada(QtGui.QApplication.translate("pychemqt", "Air"),
                        "entradaAire", psychro=True)

        # Calculate tab
        lyt = QtGui.QGridLayout(self.tabCalculo)
        lyt.addWidget(QtGui.QLabel(
            QtGui.QApplication.translate("pychemqt", "Mode")), 1, 1)
        self.mode = QtGui.QComboBox()
        for txt in self.Equipment.TEXT_MODE:
            self.mode.addItem(txt)
        self.mode.currentIndexChanged.connect(
            partial(self.changeParams, "mode"))
        lyt.addWidget(self.mode, 1, 2, 1, 4)
        lyt.addItem(QtGui.QSpacerItem(
            20, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed),
            2, 1, 1, 6)
        lyt.addWidget(QtGui.QLabel(QtGui.QApplication.translate(
            "pychemqt", "Air Relative Humidity")), 3, 1)
        self.HumedadAire = Entrada_con_unidades(float, max=1, spinbox=True,
                                                step=0.01)
        self.HumedadAire.valueChanged.connect(partial(self.changeParams, "HR"))
        lyt.addWidget(self.HumedadAire, 3, 2)
        lyt.addWidget(QtGui.QLabel(QtGui.QApplication.translate(
            "pychemqt", "Product moisture fraction")), 4, 1)
        self.HumedadSolido = Entrada_con_unidades(float, max=1., spinbox=True, step=0.01, textounidad=unidades.Mass(None).text()+"/"+unidades.Mass(None).text())
        self.HumedadSolido.valueChanged.connect(
            partial(self.changeParams, "HumedadResidual"))
        lyt.addWidget(self.HumedadSolido, 4, 2)
        lyt.addWidget(QtGui.QLabel(QtGui.QApplication.translate(
            "pychemqt", "Output Solid Temperature")), 5, 1)
        self.temperatura = Entrada_con_unidades(unidades.Temperature)
        self.temperatura.valueChanged.connect(
            partial(self.changeParams, "TemperaturaSolid"))
        lyt.addWidget(self.temperatura, 5, 2)
        lyt.addWidget(QtGui.QLabel(
            QtGui.QApplication.translate("pychemqt", "Heat Duty")), 6, 1)
        self.Heat = Entrada_con_unidades(unidades.Power)
        self.Heat.valueChanged.connect(partial(self.changeParams, "Heat"))
        lyt.addWidget(self.Heat, 6, 2)
        lyt.addWidget(QtGui.QLabel(
            QtGui.QApplication.translate("pychemqt", "Pressure Drop")), 7, 1)
        self.DeltaP = Entrada_con_unidades(unidades.Pressure)
        self.DeltaP.valueChanged.connect(partial(self.changeParams, "DeltaP"))
        lyt.addWidget(self.DeltaP, 7, 2)

        lyt.addItem(QtGui.QSpacerItem(
            20, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding),
            8, 1, 1, 6)
        group = QtGui.QGroupBox(
            QtGui.QApplication.translate("pychemqt", "Results"))
        lyt.addWidget(group, 9, 1, 1, 5)
        layout = QtGui.QGridLayout(group)
        layout.addWidget(QtGui.QLabel(QtGui.QApplication.translate(
            "pychemqt", "Output Temperature")), 1, 1)
        self.temperaturaCalculada = Entrada_con_unidades(unidades.Temperature, retornar=False, readOnly=True)
        layout.addWidget(self.temperaturaCalculada, 1, 2)
        layout.addWidget(QtGui.QLabel(
            QtGui.QApplication.translate("pychemqt", "Air Flow")), 2, 1)
        self.caudalVolumetrico = Entrada_con_unidades(unidades.VolFlow, "QGas", retornar=False, readOnly=True)
        layout.addWidget(self.caudalVolumetrico, 2, 2)
        layout.addWidget(QtGui.QLabel(QtGui.QApplication.translate(
            "pychemqt", "Output Air Relative Humidity")), 3, 1)
        self.HumedadCalculada = Entrada_con_unidades(float, readOnly=True, textounidad="%")
        layout.addWidget(self.HumedadCalculada, 3, 2)

        lyt.addItem(QtGui.QSpacerItem(
            20, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding),
            11, 1, 1, 6)

        # Output Tab
        self.addSalida(QtGui.QApplication.translate("pychemqt", "Air"), psychro=True)
        self.addSalida(QtGui.QApplication.translate("pychemqt", "Dry solid"))

        if equipment:
            self.setEquipment(equipment)

#    def rellenar(self):
#        self.EntradaAire.setCorriente(self.Equipment.kwargs["entradaAire"])
#        self.EntradaSolido.setCorriente(self.Equipment.kwargs["entradaSolido"])
#        if self.Equipment.status:
#            self.temperaturaCalculada.setValue(self.Equipment.SalidaSolido.T)
#            self.caudalVolumetrico.setValue(self.Equipment.entradaAire.corriente.Q)
#            self.HumedadCalculada.setValue(self.Equipment.SalidaAire.Xw*100)
#            self.SalidaAire.setCorriente(self.Equipment.SalidaAire)
#            self.SalidaSolido.setCorriente(self.Equipment.SalidaSolido)
#            if self.Equipment.kwargs["mode"]==1:
#                self.EntradaAire.setCorriente(self.Equipment.entradaAire)


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
#    from lib.corriente import Mezcla, Corriente, Solid, PsyStream
#    from lib.psycrometry import PsychroState
#    diametros=[96.5, 105, 110, 118, 125, 130, 140, 150, 170]
#    fraccion=[0.02, 0.05, 0.1, 0.15, 0.25, 0.2, 0.15, 0.05, 0.03]
#    solido=Solid(caudalSolido=[5000], distribucion_fraccion=fraccion, distribucion_diametro=diametros)
#    Solido=Corriente(T=300, P=101325., caudalMasico=50, ids=[62], fraccionMolar=[1], solido=solido)
#    Aire=PsyStream(caudalMasico=100, tdb=300, HR=50)
#    secador=Dryer(entradaSolido=Solido, entradaAire=Aire)
    dialogo = UI_equipment()
    dialogo.show()
    sys.exit(app.exec_())
