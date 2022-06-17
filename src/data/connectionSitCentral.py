import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import asyncio
import aioodbc
from pathlib import Path

base_path = Path(__file__).parent
file_path = (base_path / "../config.json").resolve()

loop = asyncio.get_event_loop()

dbName:str = 'DataBaseSitCentral'

class Connection:    
    def __init__(self):
        
        with open(file_path, 'r') as f:
            config = json.load(f)
        self.connection_string = "DRIVER={};SERVER={};DATABASE={};UID={}; PWD={};".format(
            config[dbName]['DRIVERODBC'],
            config[dbName]['SERVER'],
            config[dbName]['DATABASE'],
            config[dbName]['UID'],
            config[dbName]['PWD'])

    async def asyncSelect(self, query: str):
        cnxn = await aioodbc.connect(dsn=self.connection_string, loop=loop, autocommit=True)
        crsr = await cnxn.cursor()
        await crsr.execute(query)
        rows = await crsr.fetchall()
        await crsr.close()
        await cnxn.close()
        return rows

    async def asyncExecute(self, query: str):
        cnxn = await aioodbc.connect(dsn=self.connection_string, loop=loop, autocommit=True)
        crsr = await cnxn.cursor()
        await crsr.execute(query)
        await crsr.close()
        await cnxn.close()
        

    with open(file_path, 'r') as f:
        config = json.load(f)
    Driver = config[dbName]['DRIVER']
    Server = config[dbName]['SERVER']
    Database = config[dbName]['DATABASE']
    UID = config[dbName]['UID']
    PWD = config[dbName]['PWD']

    conn_str = "mssql+pymssql://{user}:{pwd}@{host}/{db}".format(
        host=Server, db=Database, user=UID, pwd=PWD)
    engine = create_engine(conn_str)
    Session = sessionmaker(bind=engine)
    session = Session()
    Base = declarative_base()
