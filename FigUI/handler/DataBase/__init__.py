import sqlite3
# from sqlite3.dbapi2 import connect

class SQLite:
    def __init__(self, filename, row_factory=None, col_factory=None):
        self.filename = filename
        self.LIST_ALL_TABLES = "SELECT name FROM sqlite_master WHERE type='table';"
        self.GET_ALL_ROWS = "SELECT * FRoM {}"
        def dict_factory(cursor, row):
            d = {}
            for idx, col in enumerate(cursor.description):
                d[col[0]] = row[idx]
            return d
        self.DICT_FACTORY = dict_factory
        self.row_factory = row_factory
        self.col_factory = col_factory
        self.history = []

    def SetRowFactory(self, row_factory):
        self.row_factory = row_factory

    def SetColFactory(self, col_factory):
        self.col_factory = col_factory

    def ListTables(self):
        # connect to db
        connection = sqlite3.connect(self.filename)  
        # point cursor
        cursor = connection.cursor()
        # get query result
        result = cursor.execute(self.LIST_ALL_TABLES)
        # convert from list of tupples to flat list
        table_names = [name[0] for name in result.fetchall()]
        # close connection with the db
        connection.close()
        # add query to history
        self.history.append(self.LIST_ALL_TABLES)

        return table_names

    def GetTableRows(self, table_name, query=None):
        # set query if nothing is passed
        if query is None:
            query = self.GET_ALL_ROWS.format(table_name)
        connection = sqlite3.connect(self.filename)
        # set the row_factory
        if self.row_factory:
            connection.row_factory = self.row_factory    
        cursor = connection.cursor()
        # get query result
        try:       
            result = cursor.execute(query).fetchall()
        except sqlite3.OperationalError as e:
            # e = str(e).strip()
            print("FigUI: sqlite3:\x1b[31;1m", e, "\x1b[0m")
            result = []
        # close connection with the db
        connection.close()
        # add query to history
        self.history.append(query)
        
        return result

    def __len__(self):
        '''Length of the SQLite instance is the number of tables in the db'''
        return len(self.ListTables())


if __name__ == "__main__":
    from pprint import pprint
    # create SQLite instance
    db = SQLite('/home/atharva/.config/google-chrome/Default/Cookies')
    # len of SQLite instance
    print(len(db))
    # get list of tables
    print(db.ListTables())
    # get table rows
    print(db.GetTableRows("cookies")[-1])
    # set row factory
    db.SetRowFactory(db.DICT_FACTORY)
    # get table rows after setting new row factory
    pprint(db.GetTableRows("cookies")[-1])
    