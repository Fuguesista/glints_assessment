from model.Transformer.Transformer_Input import *
from model.Transformer.Transformer_Model import *
from fastapi import Request, Response, status

def transformer_function(request_client:Request, response:Response, data_config:dict, global_var:dict, data_input:TransformerInputClass):
    temp_return = []
    for i, data in enumerate(data_input.list_1):
        temp_return.append(data.upper())
        temp_return.append(data_input.list_2[i].upper())
    temp_result = ", ".join(temp_return)
    id_data = TransformerModel.insert_data_sqlmodel(data_config, global_var, temp_result)
    if (id_data != None):
        return {
            "error" : 0,
            "id" : id_data,
            "output" : temp_result,
            "message" : "OK"
        }
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {
            "error" : 1,
            "message" : "Error"
        }
    
def get_data_cache(request_client:Request, response:Response, data_config:dict, global_var:dict, id:int):
    temp_return = TransformerModel.get_data_sqlmodel(data_config, global_var, id)
    is_fail = False
    if (temp_return == None):
        is_fail = True
    if (is_fail):
        response.status_code = status.HTTP_404_NOT_FOUND
        return {
            "error" : 1,
            "message" : "id not found"
        }
    else:
        return {
            "error" : 0,
            "output" : temp_return.result_data,
            "message" : "OK"
        }