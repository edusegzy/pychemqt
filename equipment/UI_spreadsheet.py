#!/usr/bin/python
# -*- coding: utf-8 -*-

###############################################################################
# Spreadsheet interaction equipment dialog
###############################################################################

import os

from PyQt4 import QtCore, QtGui
try:
    import ezodf
    import openpyxl
except:
    pass

from UI.widgets import PathConfig, Tabla
from equipment.parents import UI_equip
from equipment.spreadsheet import Spreadsheet


class TableDelegate(QtGui.QItemDelegate):
    """Delegate table with combobox options"""
    def __init__(self, owner, items=None):
        super(TableDelegate, self).__init__(owner)
        if not items:
            items = {}
            for ind in range(4):
                items[ind] = []
        self.setItems(items)

    def setItems(self, items):
        self.items = items

    def setItemsByIndex(self, index, items):
        self.items[index] = items

    def createEditor(self, parent, option, index):
        if index.column() < 4:
            self.editor = QtGui.QComboBox(parent)
            self.editor.addItems(self.items[index.column()])
        else:
            self.editor = QtGui.QLineEdit(parent)
            regExp = QtCore.QRegExp("[A-Z]|[a-z]{1,3}\\d{1,5}")
            validator = QtGui.QRegExpValidator(regExp)
            self.editor.setValidator(validator)
        return self.editor

    def setEditorData(self, editor, index):
        value = unicode(index.data(QtCore.Qt.DisplayRole).toString())
        if index.column() < 4:
            try:
                num = self.items[index.column()].index(value)
            except ValueError:
                num = -1
            editor.setCurrentIndex(num)
        else:
            editor.setText(value)

    def setModelData(self, editor, model, index):
        if index.column() < 4:
            value = editor.currentText()
        else:
            value = editor.text().toUpper()

        model.setData(index, QtCore.QVariant(value), QtCore.Qt.DisplayRole)


class UI_equipment(UI_equip):
    """Spreadsheet interaction equipment edition dialog"""
    Equipment = Spreadsheet()

    def __init__(self, equipment=None, project=None, parent=None):
        """
        equipment: Initial equipment instance to model
        """
        super(UI_equipment, self).__init__(
            Spreadsheet, entrada=True, salida=True, calculo=False, parent=parent)
        self.project = project

        # Calculate tab
        layout = QtGui.QGridLayout(self.entrada)
        label = QtGui.QApplication.translate("pychemqt", "Spreadsheet path")+":"
        msg = QtGui.QApplication.translate("pychemqt", "Select Spreadsheet")
        patrones = QtCore.QStringList()
        if os.environ["ezodf"]:
            patrones.append(QtGui.QApplication.translate(
                "pychemqt", "Libreoffice spreadsheet files") + " (*.ods)")
#        if os.environ["xlwt"]:
#            patrones.append(QtGui.QApplication.translate(
#                "pychemqt", "Microsoft Excel 97/2000/XP/2003 XMLL")+ " (*.xls)")
        if os.environ["openpyxl"]:
            patrones.append(QtGui.QApplication.translate(
                "pychemqt", "Microsoft Excel 2007/2010 XML") + " (*.xlsx)")
        patron = patrones.join(";;")
        self.filename = PathConfig(label, msg=msg, patron=patron)
        self.filename.valueChanged.connect(self.changeSpreadsheet)
        layout.addWidget(self.filename, 1, 1)
        header = [QtGui.QApplication.translate("pychemqt", "Entity"),
                  QtGui.QApplication.translate("pychemqt", "Variable"),
                  QtGui.QApplication.translate("pychemqt", "Unit value"),
                  QtGui.QApplication.translate("pychemqt", "Sheet"),
                  QtGui.QApplication.translate("pychemqt", "Cell")]
        self.datamap = Tabla(
            5, filas=1, dinamica=True, horizontalHeader=header,
            verticalHeader=False, orientacion=QtCore.Qt.AlignLeft,
            num=False, delegateforRow=TableDelegate, parent=self)
        self.datamap.setEnabled(False)
        self.datamap.cellChanged.connect(self.cellChanged)
        self.datamap.rowFinished.connect(self.addRow)
        layout.addWidget(self.datamap, 2, 1)
        layout.addItem(QtGui.QSpacerItem(
            10, 10, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding),
            10, 1)

        entitys = []
        for stream in self.project.streams.keys():
            entitys.append("s%i" % stream)
        for equip in self.project.items.keys():
            if equip[0] == "e":
                entitys.append(equip)
        self.datamap.itemDelegateForRow(0).setItemsByIndex(0, entitys)
        self.entitys = entitys
        if equipment:
            self.setEquipment(equipment)

    def changeSpreadsheet(self, path):
        self.datamap.setEnabled(bool(path))
        self.changeParams("filename", str(path))
        self.datamap.blockSignals(True)
        self.datamap.clear()
        self.datamap.blockSignals(False)
        spreadsheet = ezodf.opendoc(path)
        sheets = [name for name in spreadsheet.sheets.names()]
        self.datamap.itemDelegateForRow(0).setItemsByIndex(3, sheets)

    def rellenarInput(self):
        self.blockSignals(True)
        self.datamap.itemDelegateForRow(
            self.datamap.rowCount()-1).setItemsByIndex(0, self.entitys)
        if self.Equipment.status:
            self.datamap.setEnabled(True)
            self.filename.setText(self.Equipment.kwargs["filename"])
            self.datamap.itemDelegateForRow(0).setItemsByIndex(
                3, self.Equipment.sheets)

        self.datamap.blockSignals(True)
        self.datamap.clear()
        if self.Equipment.kwargs["datamap"]:
            for i, data in enumerate(self.Equipment.kwargs["datamap"]):
                self.datamap.addRow()
                self.datamap.itemDelegateForRow(i).setItemsByIndex(
                    0, self.entitys)
                self.datamap.itemDelegateForRow(i).setItemsByIndex(
                    3, self.Equipment.sheets)
                self.datamap.setItem(i, 0,
                                     QtGui.QTableWidgetItem(data["entity"]))
                self.datamap.setItem(i, 1,
                                     QtGui.QTableWidgetItem(data["property"]))
                self.datamap.setItem(i, 2,
                                     QtGui.QTableWidgetItem(data["unit"]))
                self.datamap.setItem(i, 3,
                                     QtGui.QTableWidgetItem(data["sheet"]))
                self.datamap.setItem(i, 4,
                                     QtGui.QTableWidgetItem(data["cell"]))
            self.datamap.itemDelegateForRow(
                self.datamap.rowCount()-1).setItemsByIndex(0, self.entitys)
            self.datamap.itemDelegateForRow(
                self.datamap.rowCount()-1).setItemsByIndex(3, self.Equipment.sheets)
        self.datamap.blockSignals(False)
        self.blockSignals(False)

    def rellenar(self):
        self.rellenarInput()
        self.status.setState(self.Equipment.status, self.Equipment.msg)

    def cellChanged(self, i, j):
        obj = self.project.getObject(str(self.datamap.item(i, 0).text()))
        properties = [prop[0] for prop in obj.propertiesNames()]
        if j == 0:  # Entity cambiado, cambiar variables disponibles
            self.datamap.itemDelegateForRow(i).setItemsByIndex(1, properties)
            editor = QtGui.QComboBox()
            editor.addItems(self.datamap.itemDelegateForRow(i).items[1])
            self.datamap.setColumnWidth(1, editor.sizeHint().width())
        elif j == 1:   # Variable cambiada, cambiar unidades disponibles
            value = self.datamap.item(i, 1).text()
            ind = properties.index(value)
            if obj.propertiesUnit()[ind] == str:
                self.datamap.itemDelegateForRow(i).setItemsByIndex(2, [" "])
                self.datamap.item(i, 2).setText(" ")
            else:
                self.datamap.itemDelegateForRow(i).setItemsByIndex(
                    2, obj.propertiesNames()[ind][2].__text__)
        elif j == 3:
            self.datamap.item(i, 4).setText("")

    def addRow(self, fila):
        datamap = self.Equipment.kwargs["datamap"][:]
        data = {}
        data["entity"] = str(fila[0])
        data["property"] = unicode(fila[1])
        data["unit"] = unicode(fila[2])
        data["sheet"] = unicode(fila[3])
        data["cell"] = str(fila[4])
        datamap.append(data)
        self.changeParams("datamap", datamap)


if __name__ == "__main__":
    import sys
    from lib.corriente import Corriente
    from lib.project import Project
    from equipment.heatExchanger import Hairpin
    project = Project()
    project.addItem("i1", Corriente())
    project.addItem("i2", Corriente())
    Cambiador = Hairpin()
    project.addItem("e1", Cambiador)
    project.addStream(1, "i1", "e1", ind_down=0)
    project.addStream(2, "i2", "e1", ind_down=1)
    project.addItem("o1", Corriente())
    project.addStream(3, "e1", "o1", ind_up=0)
    project.addItem("o2", Corriente())
    project.addStream(4, "e1", "o2", ind_up=1)
    caliente = Corriente(T=140+273.15, P=361540., caudalMasico=1.36,
                         ids=[62], fraccionMolar=[1.])
    project.setInput(1, caliente)

    spreadsheet = Spreadsheet(filename="/media/datos/ejemplo.xlsx",
                              project=project)
    app = QtGui.QApplication(sys.argv)
    dialogo = UI_equipment(spreadsheet, project=project)
    dialogo.show()
    sys.exit(app.exec_())
