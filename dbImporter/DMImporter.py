from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
import State

# To test in memory no DB conn required right now
engine = create_engine('sqlite:///:memory:', echo=True)
conn = engine.connect()
metadata = MetaData()

def main():

    state, district, minority = buildTables()

    populateDB(state, district, minority)


def populateDB(state, district, minority):
    data = []
    conn.execute(state.insert, stateFid= data[0], stateName= data[1], polygon = data[2], year = data[3], clickCount = data[4])
    conn.execute(district.insert, districtNum= data[0], voteRep= data[1], voteDem = data[2], polygon = data[3], population = data[4], clickCount = data[5])
    conn.execute(minority.insert, name= data[0], voteRep= data[1], voteDem = data[2], population = data[3])



def buildTables():


    state = Table('state', metadata,
                  Column('id', Integer, primary_key=True),
                  Column('stateFid', String),
                  Column('stateName', String),
                  Column('polygon', String),
                  Column('year', Integer),
                  Column('clickCount', Integer)
                  )

    district = Table('district', metadata,
                     Column('id', Integer, primary_key=True),
                     Column('stateId', String, ForeignKey('state.id')),
                     Column('districtNum', String),
                     Column('voteRep', Integer),
                     Column('voteDem', Integer),
                     Column('polygon', String),
                     Column('population', String),
                     Column('clickCount', String)
                     )

    minority = Table('minority', metadata,
                     Column('id', Integer, primary_key=True),
                     Column('districtNum', Integer, ForeignKey('district.id')),
                     Column('name', String),
                     Column('voteRep', Integer),
                     Column('voteDem', Integer),
                     Column('population', Integer)
                     )

    return state, district, minority

if __name__ == "__main__":
    main()

