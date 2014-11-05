from PyQt4.QtCore import QProcess, QIODevice, Qt
from PyQt4.QtGui import QCursor, QPixmap, QMessageBox

from qgis.core import QgsMapLayer
from qgis.gui import QgsMapTool

from GdalTools.tools import GdalTools_utils

import xml.etree.ElementTree as ET
import json

from gdallocationinfo_dialog import GDALLocationInfoForm

class GDALLocationInfoMapTool(QgsMapTool):
  def __init__(self, canvas):  
    QgsMapTool.__init__(self, canvas)
    
    self.canvas = canvas
    self.cursor = QCursor(QPixmap(":/plugins/AGSInfo/icons/cursor.png"), 1, 1)

  def activate(self):
    self.canvas.setCursor(self.cursor)

  def parseJSON(self, jsonLocationInfo):
    if jsonLocationInfo.has_key("error"):
        err_msg = ""
        err_msg += "Error code: " + str(jsonLocationInfo["error"]["code"]) + "\n"
        err_msg += "Error message: \n" + jsonLocationInfo["error"]["message"] + "\n"
        
        QMessageBox.warning(self.canvas,
                      self.tr("Error"),
                      str(err_msg)
                     )
        
    else:
        results = jsonLocationInfo["results"]
        
        if (len(results) == 0):
            QMessageBox.warning(self.canvas,
                          self.tr("Warning"),
                          self.tr("Not found any objects")
                         )
            return
    
        #locationInfoPure = ""
        locationInfoPure = {}
        #i = 1
        for result in results:
            attrs = {}
            #locationInfoPure += str(i) + ".\n"
            #locationInfoPure += "\tlayerName: " + result["layerName"] + "\n"
            #locationInfoPure += "\tvalue: " + result["value"] + "\n"
            #locationInfoPure += "\tattributes: " + str(result["attributes"]) + "\n"
            #i += 1
            attrs.update({"layerName": result["layerName"]})
            attrs.update({"Shape": result["attributes"]["Shape"]})
            attrs.update({"DESCRIPTION": result["attributes"]["DESCRIPTION"]})
            
            locationInfoPure.update({result["attributes"]["OBJECTID"]: attrs})
        
        #QMessageBox.information(self.canvas,
        #                  self.tr("Info"),
        #                  locationInfoPure
        #                 )
        
        self.a = GDALLocationInfoForm(locationInfoPure)
        self.a.show()
    
  def parseXML(self, xmlLocationInfo):
    #locationInfoPure = u""
    locationInfoPure = {}
    
    #i = 1
    for child in xmlLocationInfo:
        attrs = {}
        #locationInfoPure += u"" + str(i) + u".\n"
        #locationInfoPure += u"\t" + string.join([string.join( (k, str(child.attrib[k])), ":") for k in child.attrib.keys() ],",") + u".\n"
        #locationInfoPure += string.join([ string.join( (k, child.attrib[k]), ":") for k in child.attrib.keys() ],"\n") + u".\n"
        #i += 1
        for k in child.attrib.keys():
            attrs.update({k: child.attrib[k]})
        
        locationInfoPure.update({child.attrib["OBJECTID"]: attrs})
        
    #QMessageBox.information(self.canvas,
    #                      self.tr("Info"),
    #                      locationInfoPure
    #                     )
    self.a = GDALLocationInfoForm(locationInfoPure)
    self.a.show()
        
  def canvasReleaseEvent(self, event):
    
    
    #self.a = GDALLocationInfoForm({"a":{"asd1":"xcvsdfvss", "asd2":"xcvsdfvss", "asd3":"xcvsdfvss"}, "b":{"asd1":"xcvsdfvss", "asd2":"xcvsdfvss", "asd3":"xcvsdfvss"}})
    #self.a.show()
    
    currentlayer = self.canvas.currentLayer()

    if currentlayer is None:
      QMessageBox.warning(self.canvas,
                          self.tr("No active layer"),
                          self.tr("To identify features, you must choose an active layer by clicking on its name in the legend")
                         )
      return

    if currentlayer.type() != QgsMapLayer.RasterLayer:
      QMessageBox.warning(self.canvas,
                          self.tr("Wrong layer type"),
                          self.tr("This tool works only for vector layers. Please select another layer in legend and try again")
                         )
      return

    self.canvas.setCursor(Qt.WaitCursor)
    point = self.canvas.getCoordinateTransform().toMapCoordinates(event.x(), event.y())
    
    self.process = QProcess(self)
    GdalTools_utils.setProcessEnvironment(self.process)

    self.process.start("gdallocationinfo", ["-xml","-b", "1" ,"-geoloc", currentlayer.source(), str(point[0]),  str(point[1])], QIODevice.ReadOnly)
    self.process.waitForFinished()
    
    self.canvas.setCursor(self.cursor)
    
    
    if(self.process.exitCode() != 0):
        err_msg = str(self.process.readAllStandardError())
        if err_msg != '':
            QMessageBox.warning(self.canvas,
                          self.tr("Error"),
                          err_msg
                         )
        else:
            QMessageBox.warning(self.canvas,
                          self.tr("Error"),
                          str(self.process.readAllStandardOutput())
                         )
    else:
        data = str(self.process.readAllStandardOutput());
        
        root = ET.fromstring(data)
        
        alert_node = root.find('Alert')
        if (alert_node != None):
            QMessageBox.warning(self.canvas,
                          self.tr("Warning"),
                          alert_node.text
                         )
            return
        
        
        location_info_node = root.find('BandReport').find('LocationInfo')
        
        try:
            jsonLocationInfo = json.JSONDecoder().decode(location_info_node.text.encode("utf-8"))
            self.parseJSON(jsonLocationInfo)
            return
        except ValueError as err:
            print "json parse error"
            pass
        
        try:
            data = location_info_node.text.encode("utf-8")
            #data.decode("cp1251").encode("utf-8")
            xmlLocationInfo = ET.fromstring(data)
            self.parseXML(xmlLocationInfo)
            return
        except ValueError as err:
            print "xml parse error: ", err
            pass