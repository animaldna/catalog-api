import logging
import logging.handlers

""" Examples:
    # LOG.debug('YO: This is a debug message.')
    # LOG.info('YO: This is an info message.')
    # LOG.warning('YO: This is a warning message.')
    # LOG.error('YO: This is an error message')
    # LOG.critical('YO: This is a critical message')
"""

def logger(name=None):
    logger = logging.getLogger(name)
    s_handler = logging.StreamHandler()
    #f_handler = logging.FileHandler(f'{name}.error.log')

    s_handler.setLevel(logging.DEBUG)
    #f_handler.setLevel(logging.WARNING)

    s_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    #f_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    s_handler.setFormatter(s_format)
    #f_handler.setFormatter(f_format)

    logger.addHandler(s_handler)
    #LOG.addHandler(f_handler)

    return logger