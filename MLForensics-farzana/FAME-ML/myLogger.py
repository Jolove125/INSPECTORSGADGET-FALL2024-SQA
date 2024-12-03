import logging


def giveMeLoggingObject():
    format_str = '%(asctime)-15s %(levelname)-2s %(message)s'
    file_name  = 'Forensic.log'
    logging.basicConfig(format=format_str, filename=file_name, level=logging.INFO)
    loggerObj = logging.getLogger('simple-logger')
    return loggerObj
