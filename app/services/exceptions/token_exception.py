from app.config.logger import logger

class TokenException(Exception):
    def __init__(self, description):
        super().__init__(description)
        logger.exception(description)