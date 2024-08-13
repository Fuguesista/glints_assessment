import sqlite3
import os
from sqlmodel import SQLModel, create_engine

#initialize the sqllite db
def init_db(data_config, global_var):
    is_file_db_present = os.path.isfile(data_config["SQLLITE_FILE_NAME"])
    global_var["CON"] = sqlite3.connect(data_config["SQLLITE_FILE_NAME"])
    global_var["CUR"] = global_var["CON"].cursor()
    if (not is_file_db_present):
        try:
            global_var["CUR"].execute('''CREATE TABLE cache_data (id integer primary key autoincrement ,
                                    result_data varchar(1000))''')
        except Exception as e:
            print(e)
            pass
    global_var["CON"].close()

def init_db_sqlmodel(data_config, global_var):
    sqlite_url = f'sqlite:///{data_config["SQLLITE_FILE_NAME"]}'
    global_var["engine"] = create_engine(sqlite_url, echo=False, pool_size=10, max_overflow=20)
    SQLModel.metadata.create_all(global_var["engine"])


#connecting db
def connect_db(data_config, global_var):
    global_var["CON"] = sqlite3.connect(data_config["SQLLITE_FILE_NAME"], check_same_thread=False)
    global_var["CUR"] = global_var["CON"].cursor()

def connect_db_sqlmodel(data_config, global_var):
    sqlite_url = f'sqlite:///{data_config["SQLLITE_FILE_NAME"]}'
    global_var["engine"] = create_engine(sqlite_url, echo=False)

#disconnect db for shutdown worker
def disconnect_db(data_config, global_var):
    global_var["CON"].close()

def disconnect_db_sqlmodel(data_config, global_var):
    pass