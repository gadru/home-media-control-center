import pkgutil 
import sys
import inspect

__path__ = pkgutil.extend_path(__path__, __name__)

classes = dict()
for importer, modname, ispkg in pkgutil.walk_packages(path=__path__, prefix=__name__+'.'):
    __import__(modname)
    for name, obj in inspect.getmembers(sys.modules[modname]):
        if inspect.isclass(obj):
            if name != "BaseEventListener":
                classes[name] = obj