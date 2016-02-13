""" definitions and config used to detect and initialise runtimes """

from . import runner_source

class RuntimeNames(object):
    javascriptcore = 'JavaScriptCore'
    jscript = 'JScript'
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
]

config = {
    RuntimeNames.javascriptcore: {
        'commands_to_try': ["/System/Library/Frameworks/JavaScriptCore.framework/Versions/A/Resources/jsc"],
        'kwargs': {
            'name': RuntimeNames.javascriptcore,
            'runner_source': runner_source.javascriptcore
        },
    },

    RuntimeNames.jscript: {
        'commands_to_try': [ ["cscript", "//E:jscript", "//Nologo"] ],
        'kwargs': {
            'encoding': 'ascii',
            'name': RuntimeNames.jscript,
            'runner_source': runner_source.jscript,
        },
    },

    RuntimeNames.node: {
        'commands_to_try': ["nodejs", "node"],
        'kwargs': {
            'encoding': 'UTF-8',
            'name': "Node.js (V8)",
            'runner_source': runner_source.node
        },
    },

    RuntimeNames.phantomjs: {
        'commands_to_try': [ 'phantomjs' ],
        'kwargs': {
            'name': RuntimeNames.phantomjs,
            'runner_source': runner_source.phantomjs,
        },
    },

    RuntimeNames.pyv8:  {
        'commands_to_try': [None], # TODO
        'kwargs': {},
        'runtime_type': 'PyV8Runtime',
    },

    RuntimeNames.slimerjs: {
        'commands_to_try': [ 'slimerjs' ],
        'kwargs': {
            'name': RuntimeNames.slimerjs,
            'runner_source': runner_source.slimerjs,
        },
    },

    RuntimeNames.spidermonkey: {
        'commands_to_try': ['js'],
        'kwargs': {
            'name': RuntimeNames.spidermonkey,
            'runner_source': runner_source.spidermonkey,
        },
        'alternate_names': ['Spidermonkey']
    },
}
