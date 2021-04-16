import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, RedirectResponse
from pydantic import BaseModel
from typing import List
import json

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

app = FastAPI()

class TR():
    def __init__(self, state, msg):        
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

    def v2_runner_on_ok(self, result, **kwargs):        
        self.task_results.append(TR(0, result._result))

    def v2_runner_on_failed(self, host, result, ignore_errors=False):
        self.task_results.append(TR(1, result._task))

class EV(BaseModel):
    name: str = 'name'
    value: str = 'value'

class PB(BaseModel):
    playbook: str = 'playbook.yaml'
    inventory: str = 'inventory.yaml'
    extra_vars: List[EV] = []

#@app.get("/")
#async def root():
#    response = RedirectResponse(url='/public/index.html')
#    return response

@app.get("/health")
async def health():
    return {"status": "OK"}

@app.get("/api/.*", status_code=404, include_in_schema=False)
def invalid_api():
    return None

@app.post("/api/startsetup")
async def launch(item: PB):
    extra_vars = {}
    for ev in item.extra_vars:        
        extra_vars[ev.name] = ev.value
    inventory_file = os.path.join(os.getcwd(), item.inventory)
    playbook_file = os.path.join(os.getcwd(), item.playbook)

    loader = DataLoader()    
    inventory = InventoryManager(loader=loader, sources=[inventory_file])
    variable_manager = VariableManager(loader=loader, inventory=inventory)        
    variable_manager._extra_vars = extra_vars
    print(extra_vars)
    passwords={}    
    context.CLIARGS = ImmutableDict(
        connection='local', 
        module_path=['/to/mymodules', '/usr/share/ansible'], 
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

    json_compatible_item_data = jsonable_encoder(ER(return_code, callback.task_results))
    return JSONResponse(content=json_compatible_item_data)

templates = Jinja2Templates(directory="public")
@app.get("/")
async def serve_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
app.mount("/public", StaticFiles(directory=os.path.join(os.getcwd(),"public")), name="public")

    
