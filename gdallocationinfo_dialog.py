# -*- coding: utf-8 -*-
"""
/***************************************************************************
 AGSInfoDialog
                                 A QGIS plugin
 test
                             -------------------
        begin                : 2014-10-29
        git sha              : $Format:%H$
        copyright            : (C) 2014 by nextgis.ru
        email                : nextgis.ru
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os

from PyQt4.QtGui import QDialog, QTableWidgetItem
from PyQt4 import uic

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'gdallocationinfo_dialog_base.ui'))


class GDALLocationInfoForm(QDialog, FORM_CLASS):
    def __init__(self, data, parent=None):
        """Constructor."""
        super(GDALLocationInfoForm, self).__init__(parent)
        self.setupUi(self)
        
        all_attr_count = 0;
        for obj in data:
            all_attr_count += len(data[obj])
                
        self.tableWidget.clear()
        self.tableWidget.setHorizontalHeaderLabels([self.tr("Object"), self.tr("Attribute"), self.tr("Value")])
        self.tableWidget.setRowCount(all_attr_count)
        self.tableWidget.setColumnCount(3)
        row = 0;
        
        for object_name, object_attrs in data.items():
            object_name_item = QTableWidgetItem(object_name)
            for attr_name, attr_value in object_attrs.items():
                attr_name_item = QTableWidgetItem(attr_name)
                attr_value_item = QTableWidgetItem(attr_value)
                self.tableWidget.setItem(row, 0, object_name_item )
                self.tableWidget.setItem(row, 1, attr_name_item )
                self.tableWidget.setItem(row, 2, attr_value_item )
                
                row +=1
         
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        #self.tableWidget.resizeRowsToContents()
        #self.tableWidget.resizeColumnsToContents()
        #self.tableWidget.horizontalHeader().setResizeMode(1, QHeaderView.Stretch)
        #self.tableWidget.horizontalHeader().setResizeMode(2, QHeaderView.Stretch)