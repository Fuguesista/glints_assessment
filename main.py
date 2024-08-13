from fastapi import FastAPI
from Helper.Helper_DB import *
from config.Read_Config import *

global_var = {}
data_config = read_config("config/base_config.ini")
data_config["MAIN_PORT"] = int(data_config["MAIN_PORT"])
data_config["QTY_WORKER"] = int(data_config["QTY_WORKER"])

app = FastAPI()

def shutdown_routine():
    global data_config, global_var
    # make sure the connection is closed for the db
    disconnect_db(data_config, global_var)

def startup_routine():
    global data_config, global_var
    # worker generate cursor after the file is generated
    connect_db(data_config, global_var)

app.add_event_handler("shutdown", shutdown_routine)
app.add_event_handler("startup", startup_routine)

if __name__ == "__main__":
    import uvicorn
    # generate db file for sqlite
    init_db(data_config, global_var)
    uvicorn.run("main:app", workers=data_config["QTY_WORKER"], host="0.0.0.0", port=data_config["MAIN_PORT"], log_level="error")