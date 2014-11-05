# -*- coding: utf-8 -*-
"""
/***************************************************************************
 AGSInfo
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

from PyQt4.QtCore import QSettings, QTranslator, QCoreApplication, qVersion
from PyQt4.QtGui import QAction, QIcon

from qgis.core import QgsMapLayer

from gdallocationinfo_maptool import GDALLocationInfoMapTool
import resources_rc

class GDALLocationInfoPlugin:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'GDALLocationInfoPlugin_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&GDALLocationInfo')

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        
        return QCoreApplication.translate('AGSInfo', message)

    def initGui(self):            
        self.actionRun = QAction(QCoreApplication.translate("GDALLocationInfo", "GDALLocationInfo"), self.iface.mainWindow())
        self.actionRun.setIcon(QIcon(":/plugins/AGSInfo/icons/icon.png"))
        self.actionRun.setWhatsThis("Identify tool for raster layer")
        self.actionRun.setCheckable(True)

        self.iface.addRasterToolBarIcon(self.actionRun)
        self.iface.addPluginToRasterMenu(QCoreApplication.translate("GDALLocationInfo", "GDALLocationInfo"),self.actionRun)
        
        self.actionRun.triggered.connect(self.run)

        # prepare map tool
        self.mapTool = GDALLocationInfoMapTool(self.iface.mapCanvas())
        self.iface.mapCanvas().mapToolSet.connect(self.mapToolChanged)

        # handle layer changes
        self.iface.currentLayerChanged.connect(self.toggleTool)

    def unload(self):
        self.iface.removeRasterToolBarIcon(self.actionRun)

        if self.iface.mapCanvas().mapTool() == self.mapTool:
            self.iface.mapCanvas().unsetMapTool(self.mapTool)

        del self.mapTool

    def mapToolChanged(self, tool):
        if tool != self.mapTool:
            self.actionRun.setChecked(False)

    def run(self):
        self.iface.mapCanvas().setMapTool(self.mapTool)
        self.actionRun.setChecked(True)

    def toggleTool(self, layer):
        if layer is None:
            return

        if layer.type() != QgsMapLayer.RasterLayer:
            self.actionRun.setEnabled(False)
            if self.iface.mapCanvas().mapTool() == self.mapTool:
                self.iface.mapCanvas().unsetMapTool(self.mapTool)
            else:
                self.actionRun.setEnabled(True)

