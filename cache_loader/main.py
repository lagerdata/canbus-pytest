from os import listdir
from os.path import dirname, abspath
from lager.cache import PersistentCache

CWD = dirname(abspath(__file__))
def main():
    cache = PersistentCache()

    for filename in listdir(CWD):
        if filename.endswith('.zip'):
            key = filename.split('.')[0].encode()
            cache.store(key, open(filename, 'rb').read())

if __name__ == '__main__':
   main()
