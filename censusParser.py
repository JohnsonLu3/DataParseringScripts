
input  = open("CensusData/North_Carolina.csv", 'r')
output = open("NorthCarolinaCensus.csv", 'w')

COMMMA  = ','
NEWLINE = '\n'
OFFSET  = 2


for line in input:
    line = line.split(",")
    data = []
    newLine = ''
    if(line[0] == "People"):
        if(line[2] == "Total population" and line[1] != "Race"):
            data.append("Total population")
            for i in range(len(line)):
                if i%2 != 0 and i + OFFSET < len(line):
                    data.append(line[i + OFFSET])

        elif (line[1] == "Race" and line[2] != "Total population"):
            if line[2] != "One race" and line[2] != "Some other race" and line[2] != "Two or more races":
                data.append(line[2])

                for i in range(len(line)):
                    if i % 2 != 0 and i + OFFSET < len(line):
                        data.append(line[i + OFFSET])

        for i in range(len(data)):
            if i != len(data)-1:
                newLine += data[i] + COMMMA
            else:
                newLine += data[i] + NEWLINE

        if len(newLine) > 1:
            output.write(newLine)

