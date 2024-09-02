from importlib import import_module

from thinking_runtime.defaults.configure_logging import ConfigureLogging
from thinking_runtime.defaults.recognise_runtime import RecogniseRuntime
from thinking_runtime.model import BootstrapAction
from thinking_runtime.setup import SetupBootstrapping, register_action

BOOTSTRAPPED = False

def run(action: BootstrapAction):
    action.prepare()
    for r in action.requirements():
        mod = None
        for n in r.module_names:
            if mod is not None:
                break
            try:
                mod = import_module(n)
            except ModuleNotFoundError:
                pass
        assert mod is not None or not r.required #todo msg
    action.perform()

def bootstrap():
    global BOOTSTRAPPED
    if not BOOTSTRAPPED:
        register_action(RecogniseRuntime)
        register_action(ConfigureLogging)
        #todo add ConfigureResources action/module
        setup_action = SetupBootstrapping(run)
        run(setup_action)
        BOOTSTRAPPED = True