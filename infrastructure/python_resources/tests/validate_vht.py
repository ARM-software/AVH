import logging
from vht import vht

# Logging
VERBOSITY = 'INFO'
level = { "DEBUG": 10, "INFO": 20, "WARNING" : 30, "ERROR" : 40 }
logging.basicConfig(format='[%(levelname)s]\t%(message)s', level = VERBOSITY)
logging.debug(f"Verbosity level is set to {VERBOSITY}")

vht.VHTClient("aws").run()
