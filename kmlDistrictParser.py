input       = open('geoData/cb_2016_us_state_20m/cb_2016_us_state_20m.kml', 'r')
output      = open('parsedFiles/StateGeo.csv', 'w')
outputLine  = ''

stateFp = None
name    = ''
cord    = ''


for line in input:
    if "<SimpleData name=\"STATEFP\">" in line:
        if stateFp != None:
            outputLine = outputLine[:-1]
            outputLine += '\n'
            output.write(outputLine)

        stateFp     = line.replace("<SimpleData name=\"STATEFP\">", '')
        stateFp     = stateFp.replace("</SimpleData>", '')
        outputLine  = stateFp + ','

    elif "<SimpleData name=\"NAME\">" in line:
        name        = line.replace("<SimpleData name=\"NAME\">", '')
        name        = name.replace("</SimpleData>", '')
        outputLine += name + ','

    elif "<coordinates>" in line:
        cord        = line.replace("<coordinates>", '')
        cord        = cord.replace("</coordinates>", '')
        outputLine += cord + ','


input.close()
output.close()