# -*- coding: utf-8 -*-
"""
/***************************************************************************
 AGSInfo
                                 A QGIS plugin
 test
                             -------------------
        begin                : 2014-10-29
        copyright            : (C) 2014 by nextgis.ru
        email                : nextgis.ru
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load AGSInfo class from file AGSInfo.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .gdallocationinfo_plugin import GDALLocationInfoPlugin
    return GDALLocationInfoPlugin(iface)
