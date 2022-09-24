import logging
import os
import datetime as dt

formatter = logging.Formatter('%(asctime)s: %(levelname)s: %(funcName)s: %(message)s')

loggers = {}

def setup_logger(name, level=logging.INFO):
    global loggers

    if not os.path.isdir('tmp/log'):
        os.mkdir('tmp/log')

    if loggers.get(name):
        return loggers.get(name)
    else:
        handler = logging.FileHandler('tmp/log/' + name + '_' + dt.datetime.now().strftime('%Y%m%d') + '.log')        
        handler.setFormatter(formatter)

        logger = logging.getLogger(name)
        logger.setLevel(level)
        logger.addHandler(handler)

        loggers[name] = logger

        return logger