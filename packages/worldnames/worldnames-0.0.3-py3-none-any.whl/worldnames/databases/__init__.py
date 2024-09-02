# Some comment about the program

#Python imports
from enum import Enum

# Worldnames imports
from worldnames.databases.my_sql import MySQL
from worldnames.databases.sqlite import Sqlite

class Databases(Enum):
    """

    """
    sqlite = Sqlite
    mysql = MySQL