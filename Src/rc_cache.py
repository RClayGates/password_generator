# imports: std
import os
import pickle
import platform
from time import perf_counter
from datetime import datetime
import hashlib


# imports: non-std
from rc_logger import logger, cd_up


# consts
log = logger()

# main


def main():
    log.debug("func enter")
    # add_hash_components('youtube.com')
    del_hash_components('youtube.com')
    for hash_key in generate_hashes():
        print(hash_key)
        



    log.debug("func exit")
    pass


# code blocks

def generate_hashes(_primary_pw:str):
    with Cache('PW') as cache:
        for key in cache.keys():
            time_salt = datetime.ctime(datetime.now())
            if not cache.get(key, None):
                cache[key] = time_salt
            if type(cache[key]) is not str:
                continue
            hash_obj = hashlib.md5(bytes((_primary_pw+key+cache[key]), encoding = 'utf-8'))
            yield (key, hash_obj.hexdigest())

def add_hash_components(_account_url):
    with Cache('PW') as cache:
        if not cache.get(_account_url, None):
                time_salt = datetime.ctime(datetime.now())
                cache[_account_url] = time_salt

def del_hash_components(_account_url):
    with Cache('PW') as cache:
        if cache.get(_account_url,None):
            cache.pop(_account_url)

def update_hash_components(_account_url):
    with Cache('PW') as cache:
        if cache.get(_account_url, None):
                time_salt = datetime.ctime(datetime.now())
                cache[_account_url] = time_salt



class Cache:
    def __init__(self, target_cache) -> None:
        self.filepath = os.path.join(
            (cd_up(cd_up(__file__))),
            ".env",
            platform.uname()[1] + "_" + target_cache + ".pkl",
        )
        if not os.path.exists(os.path.dirname(self.filepath)):
            os.makedirs(os.path.dirname(self.filepath))
        log.debug(self.filepath)
        pass

    def __enter__(self) -> dict:
        try:
            self._filestream = open(self.filepath, "rb")
        except FileNotFoundError as _FNFError:
            log.exception(_FNFError)
            with open(self.filepath, "xb") as byte_stream:
                pickle.dump({"CreationDate": datetime.now()}, byte_stream)
            self._filestream = open(self.filepath, "rb")
        try:
            self.data = pickle.load(self._filestream)
            self._filestream.close()
            log.debug("Data retrieved")
            return self.data
        except EOFError as _EOFError:
            # TODONE: error handle pickle bug
            log.error(
                f"{_EOFError = } \n\tCorrupted Local Cache Pickle, must recreate cache"
            )
            self._filestream.close()
            with open(self.filepath, "wb") as byte_stream:
                pickle.dump({"CreationDate": datetime.now()}, byte_stream)
            raise _EOFError
        except Exception as _E:
            log.exception(_E.__class__.mro())

    def __exit__(self, exc_type, exc_value, exc_tb):
        with open(self.filepath, "wb") as file_obj:
            pickle.dump(self.data, file_obj)
        log.debug("Data stored")


if __name__ == "__main__":
    log.debug(f'{"Program Start", datetime.now()}')
    start = perf_counter()
    os.chdir(os.path.dirname(__file__))
    main()
    log.debug(f"Program Time= {perf_counter() - start:.4f}")
    log.debug(datetime.now())
