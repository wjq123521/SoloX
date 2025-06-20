from __future__ import absolute_import
import fire as fire
import sys
from solox import __version__
from solox.web import main
from solox.debug import main as debug_main

if __name__ == '__main__':
    
    if len(sys.argv) > 1 and sys.argv[1] == 'debug':
        fire.Fire(debug_main)
    else:
        fire.Fire(main)