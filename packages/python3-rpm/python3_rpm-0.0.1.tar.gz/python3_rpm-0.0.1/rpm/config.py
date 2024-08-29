import configparser
import platform
from pathlib import Path

class Config:
    def __init__(self):
        if platform.system() == "Windows":
            config_path = Path(__file__).resolve().parent / "config.ini"
        else:
            config_path = "/etc/log/config.ini"
        self.__config = configparser.ConfigParser()
        self.__config.read(config_path, "utf-8")

    @property
    def server_ip(self):
        try:
            return self.__config["server"]["server_ip"]
        except:
            return "127.0.0.1"

    @property
    def server_port(self):
        try:
            return self.__config["server"]["server_port"]
        except:
            return 22

    @property
    def server_username(self):
        try:
            return self.__config["server"]["server_username"]
        except:
            return "root"

    @property
    def server_password(self):
        try:
            return self.__config["server"]["server_password"]
        except:
            return "root@123"



config=Config()


