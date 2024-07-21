from dotenv import load_dotenv
import os


class Settings:
    __MODE: str
    __DB_HOST: str
    __DB_PORT: str
    __DB_USER: str
    __DB_PASS: str
    __DB_NAME: str
    __OWNER_ID: int

    def __init__(self):
        self.__MODE = os.getenv('MODE')
        self.__DB_USER = os.getenv('DB_USER')
        self.__DB_PASS = os.getenv('DB_PASSWORD')
        self.__DB_HOST = os.getenv('DB_HOST')
        self.__DB_PORT = os.getenv('DB_PORT')
        self.__DB_NAME = os.getenv('DB_NAME')
        self.__OWNER_ID = int(os.getenv('OWNER_ID'))

    @property
    def database_url(self):
        return f'mysql+aiomysql://{self.__DB_USER}:{self.__DB_PASS}@{self.__DB_HOST}:{self.__DB_PORT}/{self.__DB_NAME}'


load_dotenv()
settings = Settings()
