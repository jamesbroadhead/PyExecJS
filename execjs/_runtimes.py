import os.path

try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict

import execjs
import execjs._external_runtime as external_runtime
import execjs._pyv8runtime as pyv8runtime


class RuntimeNames(object):
    javascriptcore = 'JavaScriptCore'
    jscript = 'JScript'
    nashorn = 'Nashorn'
    node = 'Node'
    phantomjs = 'PhantomJS'
    pyv8 = 'PyV8'
    slimerjs = 'SlimerJS'
    spidermonkey = 'SpiderMonkey'


runtime_preferred_order = [
    RuntimeNames.pyv8,
    RuntimeNames.node,
    RuntimeNames.javascriptcore,
    RuntimeNames.spidermonkey,
    RuntimeNames.jscript,
    RuntimeNames.phantomjs,
    RuntimeNames.slimerjs,
    RuntimeNames.nashorn,
]


def register(name, runtime):
    '''Register a JavaScript runtime.'''
    _runtimes[name] = runtime


def get(name=None):
    """
    Return a appropriate JavaScript runtime.
    If name is specified, return the runtime.
    """
    if name is None:
        return _auto_detect()

    try:
        runtime = runtimes()[name]
    except KeyError:
        raise execjs.RuntimeUnavailable("{name} runtime is not defined".format(name=name))
    else:
        if not runtime.is_available():
            raise execjs.RuntimeUnavailable(
                "{name} runtime is not available on this system".format(name=runtime.name))
        return runtime


def runtimes():
    """return a dictionary of all supported JavaScript runtimes."""
    return dict(_runtimes)


def available_runtimes():
    """return a dictionary of all supported JavaScript runtimes which is usable"""
    return dict((name, runtime) for name, runtime in _runtimes.items() if runtime.is_available())


def _auto_detect():
    runtime = get_from_environment()
    if runtime is not None:
        return runtime

    for runtime in _runtimes.values():
        if runtime.is_available():
            return runtime

    raise execjs.RuntimeUnavailable("Could not find a JavaScript runtime.")


def get_from_environment():
    '''
        Return the JavaScript runtime that is specified in EXECJS_RUNTIME environment variable.
        If EXECJS_RUNTIME environment variable is empty or invalid, return None.
    '''
    try:
        name = os.environ["EXECJS_RUNTIME"]
    except KeyError:
        return None

    if not name:
        return None
    return get(name)


def _setup_runtime_map():
    runtime_map = {
        RuntimeNames.javascriptcore: external_runtime.jsc,
        RuntimeNames.jscript: external_runtime.jscript,
        RuntimeNames.nashorn: external_runtime.nashorn,
        RuntimeNames.phantomjs: external_runtime.phantomjs,
        RuntimeNames.pyv8: pyv8runtime.PyV8Runtime(),
        RuntimeNames.slimerjs: external_runtime.slimerjs,
    }
    if external_runtime.node.is_available():
        runtime_map[RuntimeNames.node] = external_runtime.node
    else:
        runtime_map[RuntimeNames.node] = external_runtime.nodejs

    return runtime_map


def _setup_runtimes(runtime_map):
    __runtimes = OrderedDict()

    for runtime_name in runtime_preferred_order:
        __runtimes[runtime_name] = runtime_map[runtime_name]

    return __runtimes

_runtimes = _setup_runtimes(_setup_runtime_map())
