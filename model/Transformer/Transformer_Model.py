import sqlite3

class TransformerModel:
    def insert_data(data_config, global_var, data_insert):
        try:
            global_var["CUR"].execute("INSERT INTO cache_data (result_data) VALUES (?)", (data_insert,))
            global_var["CON"].commit()
            return global_var["CUR"].lastrowid
        except sqlite3.Error as error:
            print("Error Insert with Error : ", error)
            return None
    
    def get_data(data_config, global_var, id:int):
        try:
            global_var["CUR"].execute("SELECT * from cache_data where id = ?", (id,))
            return global_var["CUR"].fetchall()
        except sqlite3.Error as error:
            print("Error Insert with Error : ", error)
            return None