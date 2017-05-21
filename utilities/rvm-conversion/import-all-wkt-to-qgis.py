# Start qGIS, then copy and paste ALL lines of this script into the Python Console (Ctrl+Alt+P)
# Note: You will need to change the value of `directoryContainingWktFiles` to the correct folder

from qgis.core import QgsVectorLayer, QgsMapLayerRegistry
import os, PyQt4

# Remember, no backslashes '\' in paths, only forward slashes '/'
directoryContainingWktFiles = 'D:/Dropbox/VATSIM/ZDC/vSTARSZDC/vSTARS Facility - Potomac TRACON (PCT)/Video Map WKTs'

for root, dirs, files in os.walk(directoryContainingWktFiles):
    for file in files:
        fullname = os.path.join(root, file).replace('\\', '/')
        filename = os.path.splitext(os.path.basename(fullname))[0]
        uri = PyQt4.QtCore.QUrl.fromLocalFile(fullname)
        uri.addQueryItem('delimiter', '|')
        uri.addQueryItem('useHeader', 'yes')
        uri.addQueryItem('wktField', 'wkt')
        uri.addQueryItem('crs', 'ESPG:4326')
        layer = QgsVectorLayer(str(uri.toEncoded()), filename, 'delimitedtext')
        if layer.isValid():
            QgsMapLayerRegistry.instance().addMapLayer(layer)
        else:
            print('file invalid')
