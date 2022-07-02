import logging
import uvicorn

# create logger
logger = logging.getLogger('simple_example')
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)

logger.debug('debug message')
logger.info('info message')
logger.warning('warn message')
logger.error('error message')
logger.critical('critical message')

FORMAT: str = "%(levelprefix)s %(asctime)s | %(message)s"

def init_loggers(logger_name: str = "simple_example"):
    pass
#    formatter = uvicorn.logging.DefaultFormatter(FORMAT, datefmt="%Y-%m-%d %H:%M:%S")
