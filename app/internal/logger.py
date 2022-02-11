import logging
import os
import sys

logging.basicConfig(level=os.environ.get("LOGLEVEL", "DEBUG"))

for name in ['boto', 'boto3', 'urllib3', 'botocore', 'nose']:
    logging.getLogger(name).setLevel(logging.ERROR)
    # logging.getLogger(name).propagate = False


def logger(name=None):
    logger = logging.getLogger(name)
    s_handler = logging.StreamHandler(sys.stdout)
    s_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    s_handler.setFormatter(s_format)
    
    logger.addHandler(s_handler)

    return logger