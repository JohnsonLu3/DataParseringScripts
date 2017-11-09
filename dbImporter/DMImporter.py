from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import Sequence
from sqlalchemy import inspect

# To test in memory no DB conn required right now
connection_string = "mysql+pymysql://johnsonlu:abc123@cse308.ch4xgfzmcq2l.us-east-1.rds.amazonaws.com:3306/gerrymandering"
engine = create_engine(connection_string, echo=True)
conn = engine.connect()
metadata = MetaData()
metadata.reflect(bind=engine)

StateBoundaries = []
states = []
districts = []
DistrictBoundaries = []
boundaries = []
users = []
population = []
votes = []


def main():

    # print database tables
    inspector = inspect(engine)

    # printTables()


    importVotingData()

        # # fill state info
        # ins = state.insert().values(stateName = data[0] , year = int(data[1]), clickCount = 0)
        # result = conn.execute(ins)
        # # get state PK for FK in district
        # stateId = result.inserted_primary_key
        # # fill district info
        # ins = district.insert().values(stateId=stateId, districtNum = int(data[2]), voteRep= int(data[3]), voteDem= int(data[4]), clickCount = 0)
        # result = conn.execute()
        # districtId = result.inserted_primary_key

def importVotingData():
    # populate voting data
    #
    voteData  = open("../parsedFiles/votingData.csv", 'r')
    stateData = open("../parsedFiles/StateGeo.csv", 'r')


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
            sId     = -1
            polygons = []
            sName   = data[0]
            year    = data[1]
            dId     = data[2]
            rVote   = data[3]
            dVote   = data[4]

            for line in stateData:
                line = line.split(';')
                if line[1] == sName:
                    sId = int(line[0])
                    # get polygons
                    for i in range(2,len(line)):
                        polygon = "POLYGON" + line[i]
                        polygon = polygon[:-1]
                        polygons.append(polygon)
                    break

            # import State Data
            ins = metadata.tables['States'].insert().values(StateName = sName , Year = int(year), ClickCount = 0)
            result = conn.execute(ins)
            statePKId = result.inserted_primary_key

            # import State Boundaries
            boundaryPKId = []

            for polygon in polygons:
                ins = metadata.tables['Boundaries'].insert().values(Shape=polygon)
                result = conn.execute(ins)
                boundaryPKId.append(result.inserted_primary_key)

            # import StateBoundaries
            for pkId in boundaryPKId:
                ins = metadata.tables['StateBoundaries'].insert().values(BoundaryId = pkId, StateId = statePKId, )
                result = conn.execute(ins)

            # import district Data






def printTables():
    for t in metadata.tables:
        for x in engine.execute(metadata.tables[t].select()):
            print(x)

    return


if __name__ == "__main__":
    main()

