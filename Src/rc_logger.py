# import
import os
import logging
from time import perf_counter

# const


# main
def main():
    log = logger()
    log.debug("test")
    pass


def cd_up(path):
    return os.path.dirname(path)


def logger():
    """Initalize logging to local .env folder"""

    log_path = os.path.join((cd_up(cd_up(__file__))), ".env", "env.log")
    if not os.path.exists(log_path):
        os.makedirs(os.path.dirname(log_path))

    logging.basicConfig(
        filemode="w",
        # filename=os.path.join(file_dir, "rc_logger.log"),
        filename=log_path,
        style="{",
        format="[{levelname}: {processName}: {threadName}: {module}: {funcName}: \n\t{message}]",
        level=logging.DEBUG,
    )

    log = logging.getLogger()
    return log


src_log = logger()

# code blocks


if __name__ == "__main__":
    start = perf_counter()
    os.chdir(os.path.dirname(__file__))
    main()
    print(f"Program Time= {perf_counter() - start:.2f}")
