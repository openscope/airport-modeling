import xml.etree.ElementTree as ET
import os, shutil

# Remember, no backslashes '\' in paths, only forward slashes '/'
rootDirectory = 'E:/Documents/openscope/KDCA/WKT'
inputXmlFileName = 'vSTARS Facility - Potomac TRACON (PCT)'
subFolderName = 'Video Map WKTs'
outputFileNameSuffix = '.wkt'

def allValuesAreZero(values):
    return all(abs(float(value)) < 1E-6 for value in values)
def getVideoMapsFromXML(xml):
    tree = ET.parse(xml)
    root = tree.getroot()
    videoMaps = root.findall('VideoMaps/VideoMap')
    print('Found ', len(videoMaps), ' video maps.\n')
    return videoMaps
def saveVideoMapAsWkt(videoMap, outputDirectory):
    lines = enumerate(videoMap.findall('Elements/Element'))
    outputWktFileName = videoMap.attrib['ShortName'] + outputFileNameSuffix
    outputWktFilePath = os.path.normpath(os.path.join(outputDirectory, outputWktFileName))
    outputFile = open(outputWktFilePath, 'w')
    outputFile.write('id|wkt\n')
    for index, line in lines:
        lat1 = line.attrib['StartLat']
        lon1 = line.attrib['StartLon']
        lat2 = line.attrib['EndLat']
        lon2 = line.attrib['EndLon']
        wkt = str(index) + '|LINESTRING(' + lon1 + ' ' + lat1 + ', ' + lon2 + ' ' + lat2 + ')\n'
        if not allValuesAreZero([lat1, lon1, lat2, lon2]):
            outputFile.write(wkt)
    outputFile.close()
    print('Created ' + outputWktFilePath)
def setupFilePaths():
    outputDirectory = os.path.join(rootDirectory, subFolderName)
    inputXmlFilePath = os.path.normpath(os.path.join(rootDirectory, inputXmlFileName))
    if os.path.exists(outputDirectory):
        shutil.rmtree(outputDirectory)
    os.mkdir(outputDirectory)
    return inputXmlFilePath, outputDirectory

# MAIN
inputXmlFilePath, outputDirectory = setupFilePaths()
videoMaps = getVideoMapsFromXML(inputXmlFilePath)
for videoMap in videoMaps:
    saveVideoMapAsWkt(videoMap, outputDirectory)
print('\nConversion complete!')
