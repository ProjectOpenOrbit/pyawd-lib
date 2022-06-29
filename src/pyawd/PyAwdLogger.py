import logging

# create a logger
import sys

logger = logging.getLogger('main')
# set logging level
logger.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)

# create a logging format
formatter = logging.Formatter(fmt='%(message)s',
                              datefmt="%H:%M:%S")

handler.setFormatter(formatter)
logger.addHandler(handler)
