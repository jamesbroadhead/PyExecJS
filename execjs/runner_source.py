""" javascript source used in runtime setup / exec """

javascriptcore = r"""(function(program, execJS) { execJS(program) })(function() {
  return eval(#{encoded_source});
}, function(program) {
  var output;
  try {
    result = program();
    print("");
    if (typeof result == 'undefined' && result !== null) {
      print('["ok"]');
    } else {
      try {
        print(JSON.stringify(['ok', result]));
      } catch (err) {
        print('["err"]');
      }
    }
  } catch (err) {
    print(JSON.stringify(['err', '' + err]));
  }
});
"""


jscript = r"""(function(program, execJS) { execJS(program) })(function() {
  return eval(#{encoded_source});
}, function(program) {
  #{json2_source}
  var output, print = function(string) {
    string = string.replace(/[^\x00-\x7f]/g, function(ch){
      return '\\u' + ('0000' + ch.charCodeAt(0).toString(16)).slice(-4);
    });
    WScript.Echo(string);
  };
  try {
    result = program();
    print("")
    if (typeof result == 'undefined' && result !== null) {
      print('["ok"]');
    } else {
      try {
        print(JSON.stringify(['ok', result]));
      } catch (err) {
        print('["err"]');
      }
    }
  } catch (err) {
    print(JSON.stringify(['err', err.name + ': ' + err.message]));
  }
});
"""

node = r"""(function(program, execJS) { execJS(program) })(function() { #{source}
}, function(program) {
  var output;
  var print = function(string) {
    process.stdout.write('' + string + '\n');
  };
  try {
    result = program();
    print('')
    if (typeof result == 'undefined' && result !== null) {
      print('["ok"]');
    } else {
      try {
        print(JSON.stringify(['ok', result]));
      } catch (err) {
        print('["err"]');
      }
    }
  } catch (err) {
    print(JSON.stringify(['err', '' + err]));
  }
});"""

phantomjs = r"""
(function(program, execJS) { execJS(program) })(function() {
  return eval(#{encoded_source});
}, function(program) {
  var output;
  var print = function(string) {
    console.log('' + string);
  };
  try {
    result = program();
    print('')
    if (typeof result == 'undefined' && result !== null) {
      print('["ok"]');
    } else {
      try {
        print(JSON.stringify(['ok', result]));
      } catch (err) {
        print('["err"]');
      }
    }
  } catch (err) {
    print(JSON.stringify(['err', '' + err]));
  }
});
phantom.exit();
"""

slimerjs = phantomjs

spidermonkey = r"""(function(program, execJS) { execJS(program) })(function() { #{source}
}, function(program) {
  #{json2_source}
  var output;
  try {
    result = program();
    print("");
    if (typeof result == 'undefined' && result !== null) {
      print('["ok"]');
    } else {
      try {
        print(JSON.stringify(['ok', result]));
      } catch (err) {
        print('["err"]');
      }
    }
  } catch (err) {
    print(JSON.stringify(['err', '' + err]));
  }
});
"""
