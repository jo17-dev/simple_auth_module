from app.config.logger import logger

class UserException(Exception):
    user_description: str = None # description that can be used to interact with users
    
    def __init__(self, description="No description found" , user_description:str = None, *args):
        super().__init__(*args, description)
        logger.exception(description)
        self.user_description = user_description