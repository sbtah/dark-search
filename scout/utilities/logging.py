import logging
import sys
from logging import Formatter, StreamHandler


logger = logging.getLogger('SCOUT')
logger.setLevel(logging.INFO)
handler = StreamHandler(stream=sys.stdout)
handler.setFormatter(Formatter(fmt="[%(asctime)s: %(levelname)s] %(message)s"))
logger.addHandler(handler)
logger.propagate = False