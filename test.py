import sys, argparse, copy, os
from pcpp.preprocessor import Preprocessor, OutputDirective

version='1.1.1'

class FileAction(argparse.Action):
    def __init__(self, option_strings, dest, **kwargs):
        super(FileAction, self).__init__(option_strings, dest, **kwargs)
        
    def __call__(self, parser, namespace, values, option_string=None):
        if getattr(namespace, self.dest)[0] == sys.stdin:
            items = []
        else:
            items = copy.copy(getattr(namespace, self.dest))
        items += [argparse.FileType('rt')(value) for value in values]
        setattr(namespace, self.dest, items)

class CmdPreprocessor(Preprocessor):
    def __init__(self, argv):
        argp = argparse.ArgumentParser(prog='pcpp',
            description=
    '''A pure universal Python C (pre-)preprocessor implementation very useful for
    pre-preprocessing header only C++ libraries into single file includes and
    other such build or packaging stage malarky.''',
            epilog=
    '''Note that so pcpp can stand in for other preprocessor tooling, it
    ignores any arguments it does not understand.''')
        argp.add_argument('inputs', metavar = 'input', default = [sys.stdin], nargs = '*', action = FileAction, help = 'Files to preprocess')
        argp.add_argument('--debug', dest = 'debug', action = 'store_true', help = 'Generate a pcpp_debug.log file logging execution')
        argp.add_argument('-I', dest = 'includes', metavar = 'path', nargs = 1, action = 'append', help = "Path to search for unfound #include's")

        args = argp.parse_known_args(argv[1:])

        self.args = args[0]

        super(CmdPreprocessor, self).__init__()

        self.define("__PCPP_VERSION__ " + version)
        self.define("__PCPP_ALWAYS_FALSE__ 0")
        self.define("__PCPP_ALWAYS_TRUE__ 1")

        self.define("PULP_CHIP_STR gap")
        # if self.args.debug:
        #     self.debugout = sys.stdout

        if self.args.includes:
            self.args.includes = [x[0] for x in self.args.includes]
            for d in self.args.includes:
                self.add_path(d)
        print("do parse")
        if len(self.args.inputs) == 1:
            self.parse(self.args.inputs[0])
        else:
            input = ''
            for i in self.args.inputs:
                input += '#include "' + i.name + '"\n'
            self.parse(input)
        # self.parse(self.args.inputs[0])
        self.write(open(os.devnull,"w"))

    def on_directive_handle(self, directive, toks, ifpassthru):
        if directive.value == 'include':
            print("include", toks[0].value)
        return None

    def on_include_not_found(self,is_system_include,curdir,includepath):
        print("......", curdir, includepath)
        raise OutputDirective()

p = CmdPreprocessor(sys.argv)

sys.exit(p.return_code)