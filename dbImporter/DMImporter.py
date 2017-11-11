from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.sql import select
from sqlalchemy import text
from sqlalchemy.ext.automap import automap_base


# To test in memory no DB conn required right now
connection_string = "mysql+pymysql://johnsonlu:abc123@cse308.ch4xgfzmcq2l.us-east-1.rds.amazonaws.com:3306/gerrymandering"
engine = create_engine(connection_string, echo=True)
conn = engine.connect()
metadata = MetaData()
metadata.reflect(bind=engine)
Base = automap_base()
Base.prepare(engine, reflect=True)

Boundaries = Base.classes.Boundaries
States = Base.classes.States
Districts = Base.classes.Districts
Population = Base.classes.Population


stateFPs = {}

def main():

    # printTables()
    buildStateFPMap()
    #importStateData()
    importStateBoundaryData()


def buildStateFPMap():
    stateData = open("../parsedFiles/StateGeo.csv", 'r')

    for line in stateData:
        line = line.split(';')
        if line[1] not in stateFPs.keys():
            stateFPs[line[1]] = line[0]


    stateData.close()


def importStateData():
    # populate voting data
    #
    voteData  = open("../parsedFiles/votingData.csv", 'r')
    importedStatesYear = []

    for line in voteData:
        data = []
        line = line.split(',')
        for item in line:
            if '\n' in item:
                data.append(item[:-1])
            else:
                data.append(item)

        if len(data) == 5:
            # import data into database
            sName   = data[0]
            year    = data[1]

            stateYear = sName+str(year)
            if stateYear not in importedStatesYear:
                # get StateFp
                sId = stateFPs[sName]

                # import State Data
                ins = metadata.tables['States'].insert().values(StateId=sId, StateName=sName, Year=int(year), ClickCount=0)
                conn.execute(ins)
                importedStatesYear.append(sName+year)

    voteData.close()

def importStateBoundaryData():
    # import State Boundaries
    stateData = open("../parsedFiles/StateGeo.csv", 'r')

    for line in stateData:
        boundaryPKId = []

        line = line.split(';')
        sId = int(line[0])
        polygons = line[2:]

        for polygon in polygons:
            polygon = "PolygonFromText(\'POLYGON(" + polygon + ")\')"

            # sql = text('insert into Boundaries(Shape) VALUES(' + polygon +')')
            # conn.execute(sql)

            ins = metadata.tables['Boundaries'].insert().values(Shape=text(polygon))
            result = conn.execute(ins)
            boundPKId = result.inserted_primary_key

            # get pkId from last inserted for StateBoundary FK
            boundaryPKId.append(boundPKId)

        # import StateBoundaries
        for pkId in boundaryPKId:
            ins = metadata.tables['StateBoundaries'].insert().values(BoundaryId=pkId[0], StateId=sId)
            result = conn.execute(ins)


    stateData.close()

def importDistricts(statePKId, year, sId):

    # Districts
    # `DistrictId`
    # `Area`
    # `clickCount`
    # `StateId` FK
    area = None
    districtPKs = []
    districtData = None

    if year == 2013:
        districtData = open('../parsedFiles/DistrictGeo_2013.csv', 'r')
    elif year == 2014:
        districtData = open('../parsedFiles/DistrictGeo_2014.csv', 'r')

    elif year == 2016:
        districtData = open('../parsedFiles/DistrictGeo_2016.csv', 'r')
    else:
        pass

    if districtData != None:
        for line in districtData:
            line = line.split(';')
            if line[0] == sId and line[1] == dId:
                # Insert District Data
                ins = metadata.tables['Districts'].insert().values(DistrictId = dId, Area= area, clickCount = 0, StateId=statePKId)
                result = conn.execute(ins)
                boundPKId = result.inserted_primary_key

                # get pkId from last inserted for StateBoundary FK
                districtPKs.append(boundPKId)
    else:
        # No district data
        pass

    return districtPKs


def importPopulationData(year, sName, sFp, district):
    # Population
    # `Id`
    # `Name` ENUM('Total', 'White', 'Black', 'Hispanic', 'Asian', 'PacificIslander', 'AmericanIndian', 'Other', 'Mixed')
    # `Population`
    # `DistrictId`
    if year in range(2010, 2020):               # range of the census data we have
        if sName == 'Virginia':
            vaCensus = open('../parsedFiles/VirginiaCensus.csv', 'r')
        elif sName == 'North Carolina':
            ncCensus = open('../parsedFiles/NorthCarolinaCensus.csv', 'r')
        elif sName == 'New York':
            nyCensus = open('../parsedFiles/nyCensus.csv', 'r')

        ins = metadata.tables['Population'].insert().values(Name='', Population=-1, DistrictId=district)
        result = conn.execute(ins)




def importVotingData(dId, party, vote):
    ins = metadata.tables['Votes'].insert().values(DistrictId=dId, Party=party, voteCount=vote)
    result = conn.execute(ins)


def printTables():
    for t in metadata.tables:
        for x in engine.execute(metadata.tables[t].select()):
            print(x)

    return


if __name__ == "__main__":
    main()

