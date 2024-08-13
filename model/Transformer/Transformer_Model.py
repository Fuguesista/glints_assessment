import sqlite3
from typing import Optional
from sqlmodel import Field, SQLModel, Session, select

class cache_data(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    result_data: str

class TransformerModel:
    def insert_data(data_config, global_var, data_insert):
        try:
            global_var["CUR"].execute("INSERT INTO cache_data (result_data) VALUES (?)", (data_insert,))
            global_var["CON"].commit()
            return global_var["CUR"].lastrowid
        except sqlite3.Error as error:
            print("Error Insert with Error : ", error)
            return None
    
    def insert_data_sqlmodel(data_config, global_var, data_insert):
        temp_class = cache_data(result_data=data_insert)
        with Session(global_var["engine"]) as session:
            session.add(temp_class)
            session.commit()
            session.refresh(temp_class)
        return temp_class.id
    
    def get_data_sqlmodel(data_config, global_var, id):
        with Session(global_var["engine"]) as session:
            statement = select(cache_data).where(cache_data.id == id)
            cache_data_temp = session.exec(statement).first()
            return cache_data_temp

    def get_data(data_config, global_var, id:int):
        try:
            global_var["CUR"].execute("SELECT * from cache_data where id = ?", (id,))
            return global_var["CUR"].fetchall()
        except sqlite3.Error as error:
            print("Error Insert with Error : ", error)
            return None
            