import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, RedirectResponse
from pydantic import BaseModel
from typing import List
import json

from fastapi.logger import logger
from ansible.module_utils.common.collections import ImmutableDict
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.plugins.callback import CallbackBase 
from ansible import context
from fastapi.encoders import jsonable_encoder
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from logging.config import dictConfig

import pickle
import logging
logger = logging.getLogger("uvicorn.error")

app = FastAPI(debug = True)

global return_code
return_code = 0
global task_results
task_results = []

class TR():
    def __init__(self, state, name, msg):        
        self.name = name
        self.status = state
        self.message = msg

class ER():
    status: int = 0
    tasks: List[TR] = []

    def __init__(self, state, tasks):        
        self.status = state
        self.tasks = tasks        

class RestCallback(CallbackBase):
    """Callback for Task output creation"""

    def __init__(self):
        super(RestCallback, self).__init__()        
        self.task_results = []
        task_results = self.task_results
        self.current_task_name = None

    def v2_runner_on_ok(self, result, **kwargs):
        self.task_results.append(TR(0, self.current_task_name, result._result))                
        logger.info('runner_ok')
        pickle.dump( self.task_results, open( "state.p", "wb" ) ) 

    def v2_runner_on_failed(self, result, ignore_errors=False):            
        self.task_results.append(TR(1, self.current_task_name, result._result))        
        logger.info('runner_failed')         
        pickle.dump( self.task_results, open( "state.p", "wb" ) ) 

    def playbook_on_task_start(self, name, is_conditional):
        logger.info('runner_task_start %s' %(name))
        self.current_task_name = name

class EV(BaseModel):
    name: str = 'name'
    value: str = 'value'

class PB(BaseModel):
    playbook: str = 'playbook.yaml'
    inventory: str = 'inventory.yaml'
    extra_vars: List[EV] = []

@app.get("/health")
async def health():
    return {"status": "OK"}

@app.get("/api/setup/status")
async def status():
    logger.debug('/api/setup/status called')  
    task_state = pickle.load( open( "state.p", "rb" ) )    
    json_compatible_item_data = jsonable_encoder(ER(-1, task_state))
    return JSONResponse(content=json_compatible_item_data)    

@app.post("/api/setup/start")
async def launch(item: PB):
    task_results = []
    logger.debug('/api/setup/start got payload: %s' %item)    
    extra_vars = {}
    for ev in item.extra_vars:                
        extra_vars[ev.name] = ev.value
    logger.info('/api/setup/start got extra vars: %s' %extra_vars)
    inventory_file = os.path.join(os.getcwd(), item.inventory)
    logger.info('/api/setup/start inventory file: %s' %inventory_file)
    playbook_file = os.path.join(os.getcwd(), item.playbook)
    logger.info('/api/setup/start playbook file: %s' %playbook_file)

    loader = DataLoader()    
    inventory = InventoryManager(loader=loader, sources=[inventory_file])
    variable_manager = VariableManager(loader=loader, inventory=inventory)        
    variable_manager._extra_vars = extra_vars    
    passwords={}    
    context.CLIARGS = ImmutableDict(
        connection='local', 
        module_path=['/usr/share/ansible',], 
        forks=10, 
        become=None,                                    
        become_method=None, 
        become_user=None, 
        check=False, 
        diff=False,
        syntax=None,
        start_at_task=None)
    playbook = PlaybookExecutor(
        playbooks=[playbook_file],
        inventory=inventory,
        variable_manager=variable_manager,
        loader=loader,        
        passwords=passwords)

    callback = RestCallback()
    playbook._tqm._stdout_callback = callback
    return_code = playbook.run()    
    
    logger.info('Got RC %s' %return_code)
    er = ER(return_code, callback.task_results)
    #for task in er.tasks:
    #    logger.info('Got Task-Message: %s:%s ' %(task.status, task.message))            
    json_compatible_item_data = jsonable_encoder(ER(return_code, callback.task_results))
    return JSONResponse(content=json_compatible_item_data)    

@app.get("/api/.*", status_code=404, include_in_schema=False)
def invalid_api():
    return None

templates = Jinja2Templates(directory="public")
@app.get("/")
async def serve_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
app.mount("/public", StaticFiles(directory=os.path.join(os.getcwd(),"public")), name="public")

    
