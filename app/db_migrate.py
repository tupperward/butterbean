from tabnanny import check
from modules.bobross import rossQuotes
from modules.bovonto import pitches
from sqlalchemy import create_engine, String, Integer, Table,Column, MetaData
from sqlalchemy.orm import Session

engine = create_engine("sqlite+pysqlite:///db/butterbean.db", echo=True, future=True)
meta = MetaData()

bobQuotes = Table(
  'bobQuotes', meta,
  Column('id', Integer, primary_key=True),
  Column('quote', String)
)

bovontoPitches = Table(
  'bovontoPitches', meta,
  Column('id',Integer, primary_key=True),
  Column('pitch',String)
)

meta.create_all(engine)

with Session(engine) as session:
  session.begin()
  for row in rossQuotes:
    statement = "INSERT INTO bobQuotes (quote) VALUES ('{}')".format(row)
    session.execute(statement)
  session.commit()

with Session(engine) as session:
  session.begin()
  for row in pitches:
    statement = "INSERT INTO bovontoPitches (pitch) VALUES ('{}')".format(row)
    session.execute(statement)
  session.commit()
