import logging

class Logger():
    def __init__(self, loglevel: str ):
        self.logger = logging.getLogger()
        self.logger.setLevel(loglevel)
        log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        handler = logging.StreamHandler()
        handler.setLevel(loglevel)
        handler.setFormatter(log_format)

        self.logger.addHandler(handler)

    def getLogger(self):
        return self.logger