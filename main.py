from fastapi import FastAPI, Request
from controller.Helper.Helper_DB import *
from config.Read_Config import *
from controller.Transformer.Transformer import *

from model.Transformer.Transformer_Input import *

global_var = {}
data_config = read_config("config/base_config.ini")
data_config["MAIN_PORT"] = int(data_config["MAIN_PORT"])
data_config["QTY_WORKER"] = int(data_config["QTY_WORKER"])

app = FastAPI()

@app.post('/payload', status_code=200)
@app.post('/payload/', status_code=200)
def insert_transformers(request: Request, response: Response, data_input:TransformerInputClass):
    return transformer_function(request, response, data_config, global_var, data_input)

@app.get("/payload/{id}", status_code=200)
@app.get("/payload/{id}/", status_code=200)
def get_transformers(request: Request, response: Response, id:int):
    return get_data_cache(request, response, data_config, global_var, id)

def shutdown_routine():
    global data_config, global_var
    # make sure the connection is closed for the db
    disconnect_db_sqlmodel(data_config, global_var)

def startup_routine():
    global data_config, global_var
    # worker generate cursor after the file is generated
    connect_db_sqlmodel(data_config, global_var)

app.add_event_handler("shutdown", shutdown_routine)
app.add_event_handler("startup", startup_routine)

if __name__ == "__main__":
    import uvicorn
    # generate db file for sqlite
    init_db_sqlmodel(data_config, global_var)
    uvicorn.run("main:app", workers=data_config["QTY_WORKER"], host="0.0.0.0", port=data_config["MAIN_PORT"], log_level="error")