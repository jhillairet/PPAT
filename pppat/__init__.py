# convenience import shortcuts
from . control_room import signals
from . control_room import control_room
from . control_room.signals import *

# Setup the logging style
import logging
from logging.config import dictConfig

logging_config = dict(
    version=1,
    disable_existing_loggers=False,
    formatters={
        'f': {'format':
              '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'}
        },
    handlers={
        'h': {'class': 'logging.StreamHandler',
              'formatter': 'f',
              'level': logging.DEBUG}
        },
    root={
        'handlers': ['h'],
        'level': logging.INFO,  # change to DEBUG here is needed
        },
)

dictConfig(logging_config)
logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# create file handler which logs even debug messages
fh = logging.FileHandler('pppat.log', mode='w') # overwrite the log file (append otherwise)
fh.setFormatter(formatter)
logger.addHandler(fh)