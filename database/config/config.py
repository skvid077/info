from dotenv import dotenv_values


class DbError(Exception):
    def __str__(self):
        return 'not test'


class Settings:
    __AWS_ACCESS_KEY_ID: str
    __AWS_SECRET_ACCESS_KEY_ID: str

    __TOKEN_TELEGRAM_BOT: str

    __DB_HOST: str
    __DB_PORT: str
    __DB_USER: str
    __DB_PASS: str
    __DB_NAME: str

    __OWNER_ID: str

    __MODE: str

    def __init__(self):
        self.__MODE = config.get('MODE')
        self.__DB_USER = config.get('DB_USER')
        self.__DB_PASS = config.get('DB_PASS')
        self.__DB_HOST = config.get('DB_HOST')
        self.__DB_PORT = config.get('DB_PORT')
        self.__DB_NAME = config.get('DB_NAME')
        self.__OWNER_ID = config.get('OWNER_ID')
        self.__AWS_ACCESS_KEY_ID = config.get('AWS_ACCESS_KEY_ID')
        self.__AWS_SECRET_ACCESS_KEY_ID = config.get('AWS_SECRET_ACCESS_KEY_ID')
        self.__TOKEN_TELEGRAM_BOT = config.get('TOKEN_TELEGRAM_BOT')

    @property
    def database_url(self):
        return f'mysql+aiomysql://{self.__DB_USER}:{self.__DB_PASS}@{self.__DB_HOST}:{self.__DB_PORT}/{self.__DB_NAME}'

    @property
    def mode(self):
        return self.__MODE

    @property
    def owner(self):
        return self.__OWNER_ID

    @property
    def aws_access_key_id(self):
        return self.__AWS_ACCESS_KEY_ID

    @property
    def aws_secret_access_key_id(self):
        return self.__AWS_SECRET_ACCESS_KEY_ID

    @property
    def token_telegram_bot(self):
        return self.__TOKEN_TELEGRAM_BOT


# config = dotenv_values('C:\\work\\project\\info\\.env')
config = dotenv_values('C:\\work\\project\\info\\.test.env')  # test
settings = Settings()
# assert settings.mode == 'test', 'not test'
if settings.mode != 'test':
    raise DbError
