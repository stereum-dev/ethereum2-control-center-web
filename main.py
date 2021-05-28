import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
from pydantic import BaseModel
from typing import List, Any
import json

from fastapi.logger import logger
from ansible.module_utils.common.collections import ImmutableDict
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.utils.vars import load_extra_vars
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
        pickle.dump( self.task_results, open( "/tmp/state.p", "wb" ) )

    def v2_runner_on_failed(self, result, ignore_errors=False):
        self.task_results.append(TR(1, self.current_task_name, result._result))
        logger.info('runner_failed')
        pickle.dump( self.task_results, open( "/tmp/state.p", "wb" ) )

    def playbook_on_task_start(self, name, is_conditional):
        logger.info('runner_task_start %s' %(name))
        self.current_task_name = name

class PB(BaseModel):
    playbook: str = 'playbook.yaml'
    inventory: str = 'inventory.yaml'
    extra_vars: Any = {}

@app.get("/health")
async def health():
    return {"status": "OK"}

@app.get("/api/setup/status")
async def status():
    try:
        logger.debug('/api/setup/status called')
        task_state = pickle.load( open( "/tmp/state.p", "rb" ) )
        json_compatible_item_data = jsonable_encoder(ER(-1, task_state))
        return JSONResponse(content=json_compatible_item_data)
    except Exception as e:
        raise HTTPException(status_code=409, detail="No action running")


@app.post("/api/setup/start")
async def launch(item: PB):
    try:
        logger.debug('/api/setup/start got payload: %s' %item)
        task_results = []
        with open('/tmp/vars.json', 'w', encoding="utf-8") as varfile:
            varfile.write(json.dumps(item.extra_vars))
        logger.info('/api/setup/start got extra vars: %s' %item.extra_vars)
        inventory_file = os.path.join('/opt/app/stereum-release', item.inventory)
        logger.info('/api/setup/start inventory file: %s' %inventory_file)
        playbook_file = os.path.join('/opt/app/stereum-release', item.playbook)
        logger.info('/api/setup/start playbook file: %s' %playbook_file)

        passwords={}
        logger.debug('Setting CLIARGS')
        context.CLIARGS = ImmutableDict(
            listtags=False,
            listtasks=False,
            listhosts=False,
            syntax=False,
            connection='smart',
            verbosity=99,
            module_path=['/usr/local/lib/python3.9/site-packages/ansible/plugins','/usr/share/ansible','/opt/app/stereum-release'],
            forks=10,
            become=True,
            become_method='sudo',
            become_user='root',
            check=False,
            diff=False,
            start_at_task=None,
            extra_vars=('@/tmp/vars.json',))
        # load variables
        loader = DataLoader()
        logger.debug('loading inventory file %s' %inventory_file)
        inventory = InventoryManager(loader=loader, sources=[inventory_file])
        logger.debug('Initializing Variable manager')
        variable_manager = VariableManager(loader=loader, inventory=inventory)
        variable_manager._extra_vars = load_extra_vars(loader=loader)
        # execute playbook
        logger.debug('Executing playbook %s' %playbook_file)
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
        json_compatible_item_data = jsonable_encoder(ER(return_code, callback.task_results))
        return JSONResponse(content=json_compatible_item_data)
    except Exception as e:
        import traceback
        traceback.print_exc()
        logger.error(e)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/.*", status_code=404, include_in_schema=False)
def invalid_api():
    return None

templates = Jinja2Templates(directory="public")
@app.get("/")
async def serve_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
app.mount("/public", StaticFiles(directory=os.path.join(os.getcwd(),"public")), name="public")