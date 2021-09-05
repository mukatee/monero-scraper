import logging

def create_logger(logger_name):
    logging.basicConfig(filename='monero_scraper.log',
                        format='%(asctime)s - %(name)s - %(message)s',
                        filemode='w',
                        level=logging.WARNING)
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    stream = logging.StreamHandler()
    stream.setLevel(logging.DEBUG)
    streamformat = logging.Formatter("%(asctime)s:%(levelname)s:%(message)s")
    stream.setFormatter(streamformat)
    logger.addHandler(stream)
    return logger

