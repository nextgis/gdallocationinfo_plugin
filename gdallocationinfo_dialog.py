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

from PyQt4.QtGui import QDialog, QTableWidgetItem, QTreeWidgetItem, QAbstractItemView, QStandardItemModel, QStandardItem
from PyQt4 import uic

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'gdallocationinfo_dialog_base.ui'))

class GDALLocationInfoForm(QDialog, FORM_CLASS):
    def __init__(self, data, parent=None):
        """Constructor."""
        super(GDALLocationInfoForm, self).__init__(parent)
        self.setupUi(self)
        
        self.treeView.setSelectionBehavior(QAbstractItemView.SelectRows)
        
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels([self.tr('object/attribute'), self.tr('value')])
        
        self.treeView.setModel(model)
        self.treeView.setUniformRowHeights(True)
        
        
        for object_name, object_attrs in data.items():
            parent = QStandardItem(object_name)
            for attr_name, attr_value in object_attrs.items():
                attr_name_item = QStandardItem(attr_name)
                attr_value_item = QStandardItem(attr_value)
                parent.appendRow([attr_name_item, attr_value_item])
            model.appendRow(parent)
            
if __name__ == "__main__":
    print "__main__"
    import sys
    from PyQt4.QtGui import QWidget, QApplication
    app = QApplication(sys.argv)
    #window = QWidget()
    #window.show()
    a = GDALLocationInfoForm({"a":{"asd1":"xcvsdfvss", "asd2":"xcvsdfvss", "asd3":"xcvsdfvss"}, "b":{"asd1":"xcvsdfvss", "asd2":"xcvsdfvss", "asd3":"xcvsdfvss"}})
    a.show()
    
    sys.exit(app.exec_())
    