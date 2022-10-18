import array
from ctypes import Array
from sqlalchemy import create_engine, table, text, Table, Column, CheckConstraint, DefaultClause, String, Integer, MetaData
from sqlalchemy.orm import Session

engine = create_engine("sqlite+pysqlite:///db/butterbean.db", echo=True, future=True)
meta = MetaData()

# Table for permissions management
permissions = Table(
    'permissions', meta,
    Column('user', String, unique=True, nullable=True, ), # A user name, Tupperward#5115 for example. One entry per user.
    Column('role', String, unique=True, nullable=True, server_default=None), # A role name, she/her for example. One entry per role.
    # -- We use Integer because Sqlite does not know Booleans and represents it with 1 and 0.
    Column('manage_memes', Integer, server_default=0), # User may add/remove memes
    Column('assign_roles', Integer, server_default=0), # User may add/remove roles on users
    Column('bot_admin', Integer, server_default=0), # Has admin bot permissions. Probably should not guarantee right to assign roles.
    # -- This role is not assignable by users on themselves
    Column('is_user_settable', Integer, nullable=False, server_default=0),
    # Ensure this is only set on roles
    CheckConstraint('(("is_user_settable" == 1) AND ("role" IS NOT NULL)) OR ("is_user_settable" == 0)', name='is_user_settable requires a role'),
    # This role can be set on users by someone with the assign_roles permission
    # Note that this will not override permissions on the discord side, the bot is bound by which roles it as permissions to assign there 
    Column('is_assignable', Integer, nullable=False, server_default=0),
    # Ensure this is only set on roles
    CheckConstraint('(("is_assignable" == 1) AND ("role" IS NOT NULL)) OR ("is_assignable" == 0)',name='is_assignable_requires_a_role'),
    CheckConstraint('(("user" IS NOT NULL) AND ("role" IS NULL)) OR(("user" IS NULL) AND ("role" IS NOT NULL))',name='provide only one of: user or role'),
)

def create_all_tables(): # Prevents the table from being created unless it needs to be. Can be imported and called from main app.
  meta.create_all(engine) # Creates the above table.

async def checkPerms(name: list, column: str, perm: str) -> bool: 
  with Session(engine) as session:
    for item in name: 
      initStatement: str = 'SELECT EXISTS(SELECT 1 FROM permissions WHERE {}="{}");'.format(column, item)
      lookupStmnt: str = 'SELECT {} FROM permissions WHERE {}="{}"'.format(perm, column, item)
      # Check to see if the user or role is in the database already.
      returning = session.execute(text(initStatement)).fetchone() #Python will also natively interpret Sqlite's 1 as True. Thanks, Python!
      # If this is a novel user or role, create a new entry in the database to track their permission state in the future.
      if not returning: 
          # Because all permission levels default to 0, creating a new row for a user or role guarantees that role has minimum permissions unless explicitly changed by an admin.
          createNewRow: str = 'INSERT INTO permissions ({}) VALUES ("{}");'.format(column, item)
          session.execute(text(createNewRow))
          return False #If you didn't exist before now, you sure as hell didn't have permissions set.
      result = session.execute(text(lookupStmnt)) # Save the lookup to result
      if result: # If result for any item in the list is 1 
        return result # return True (1)
  return result # If it gets to this point, result must be False.

async def addPerms(name: str, column: str, perm: str): # Should only be called on one role at a time.
  # ? Should this be an UPDATE or INSERT? @JinxedFeline
  addPermStmnt: str = 'INSERT INTO {} VALUES (1) WHERE {}="{}";'.format(perm,column,name)
  with Session(engine) as session:
    session.execute(text(addPermStmnt))

async def removePerms(name: str, column: str, perm: str): # Should only be called on one role at a time. 
  # ? Similar question about formating @JinxedFeline
  removePermStmt: str = 'INSERT INTO {} VALUES (0) WHERE {}="{}";'.format(perm,column,name)
  with Session(engine) as session:
    session.execute(text(removePermStmt))