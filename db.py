import sqlite3

class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS classes (название text PRIMARY KEY)")
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS features (название text PRIMARY KEY, тип text, область_значений text)")
        self.conn.commit()
    
    def fetch_features(self):
        self.cur.execute("SELECT * FROM features")
        rows=self.cur.fetchall()
        return rows

    def fetch_classes(self):
        self.cur.execute("SELECT * FROM classes")
        rows=self.cur.fetchall()
        return rows

    def columns_features(self):
        self.cur.execute("SELECT * FROM features")
        columns = [description[0] for description in self.cur.description]
        return columns

    def columns_classes(self):
        self.cur.execute("SELECT * FROM classes")
        columns = [description[0] for description in self.cur.description]
        return columns

    def insert_feature(self, args):
        # create dynamic string request
        request_string = list("INSERT INTO features VALUES (")
        for element in args:
            request_string+="?,"
        request_string[len(request_string)-1] = ')' # change last ',' to ')'
        self.cur.execute("".join(request_string),tuple(args)) # make sql request
        self.conn.commit()  # commit
        self.__add_column(args[0])

    def select_Cfeature(self, class_name, feature_name):
        self.cur.execute("SELECT "+feature_name+" FROM classes WHERE название= \""+class_name+"\"")
        return self.cur.fetchone()
    
    def update_Cfeature(self, class_name, feature_name, value):
        print("UPDATE classes SET "+feature_name+" = "+value+" WHERE название=\""+class_name+"\"")
        self.cur.execute("UPDATE classes SET "+feature_name+" = \""+value+"\" WHERE название=\""+class_name+"\"")
        self.conn.commit()

    def __add_column(self, col_name):
        self.cur.execute("ALTER TABLE classes ADD COLUMN "+col_name)
        self.conn.commit()  # commit
    
    def __add_column_two(self, col_name):
        self.cur.execute("ALTER TABLE new_classes ADD COLUMN "+col_name)
        self.conn.commit()  # commit

    def insert_class(self, args):
        # create dynamic string request
        request_string = list("INSERT INTO classes VALUES ( ")
        print("SQL:",args)
        for element in args:
            request_string+="?,"
        request_string[len(request_string)-1] = ')' # change last ',' to ')'
        print("".join(request_string))
        self.cur.execute("".join(request_string),tuple(args)) # make sql request
        self.conn.commit()  # commit
    
    def remove_feature(self, feature_name):
        self.__remove_column_from_classes(feature_name)
        self.cur.execute("DELETE FROM features WHERE название=?",(feature_name,))
        self.conn.commit()
        
    def __rename_column(self, old, new):
        self.cur.execute("ALTER TABLE classes RENAME COLUMN "+old+" TO "+new)
        self.conn.commit()

    def __remove_column_from_classes(self, feature_name):
        self.cur.execute("SELECT название FROM features WHERE название=?",(feature_name,))
        column_name = self.cur.fetchone()[0]
        print("col_name:",column_name)
        old_names = self.columns_classes()[1:]
        print(old_names)
        self.cur.execute("CREATE TABLE IF NOT EXISTS new_classes (название text PRIMARY KEY)")
        self.conn.commit()
        self.cur.execute("SELECT * FROM new_classes")
        print(self.cur.fetchall())
        old_names.remove(column_name)
        print("removed:",old_names)
        for element in old_names:
            self.__add_column_two(element)
        request_string = "INSERT INTO new_classes SELECT название, "
        for element in old_names:
            request_string += element + ", "
        request_string = request_string[:-2]
        request_string += " FROM classes"
        self.cur.execute(request_string)
        self.conn.commit()
        self.cur.execute("DROP TABLE IF EXISTS classes")
        self.conn.commit()
        self.cur.execute("ALTER TABLE new_classes RENAME TO classes")
        self.conn.commit()

    def remove_class(self, name):
        self.cur.execute("DELETE FROM classes WHERE название=?",(name,))
        self.conn.commit()

    def get_columns_and_types(self):
        columns = self.columns_classes()
        types = []
        for element in columns:
            self.cur.execute("SELECT тип FROM features WHERE название=?",(element,))
            types.append(self.cur.fetchone())
        return columns, types

    def update_feature(self, name, args):
        self.__rename_column(name, args[0])
        columns = self.columns_features()
        request_string = list("UPDATE features SET ")
        for i in range(0,len(args)):
            request_string+=columns[i]+" = ?,"
        request_string[len(request_string)-1] = ' '
        request_string+= "WHERE название = \""+str(name)+"\";"
        print("".join(request_string), tuple(args))
        self.cur.execute("".join(request_string),tuple(args)) # make sql request
        self.conn.commit()

    def get_class(self, name):
        self.cur.execute("SELECT * FROM classes WHERE название=?",(name,))
        return self.cur.fetchone()

    def get_feature(self, name):
        self.cur.execute("SELECT * FROM features WHERE название=?",(name,))
        return self.cur.fetchone()

    def __del__(self):
        self.conn.close()

