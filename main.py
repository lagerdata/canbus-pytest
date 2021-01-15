import sys
import pytest

if __name__ == '__main__':
   args = sys.argv
   if args[-1].startswith('::'):
      args = args[1:]
      args[-1] = __file__ + args[-1]
   sys.exit(pytest.main(args))

