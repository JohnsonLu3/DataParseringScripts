input       = open('geoData/cb_2014_us_cd114_20m/cb_2014_us_cd114_20m.kml', 'r')
output      = open('parsedFiles/DistrictGeo_2014.csv', 'w')
outputLine  = ''

stateFp = None
congressionalNum = "\"CD114FP\""
districtTag = "<SimpleData name=" + congressionalNum +">"
name    = ''
cord    = ''


for line in input:
    if "<SimpleData name=\"STATEFP\">" in line:
        if stateFp != None:
            outputLine = outputLine[:-1]
            outputLine += '\n'
            output.write(outputLine)

        stateFp     = line.replace("<SimpleData name=\"STATEFP\">", '')
        stateFp     = stateFp.replace("</SimpleData>\n", '')
        outputLine  = stateFp + ','

    elif districtTag in line:
        name        = line.replace(districtTag, '')
        name        = name.replace("</SimpleData>\n", '')
        outputLine += name + ','

    elif "<coordinates>" in line:
        cord        = line.replace("<coordinates>", '')
        cord        = cord.replace("</coordinates>\n", '')
        outputLine += '['+cord+']' + ','


input.close()
output.close()