from enum import Enum

class PlayerID(Enum):
    AI1 = 0
    AI2 = 1
    AI3 = 2
    HUMAN = 100

# 文件路径
ACCOUNT_FILE = r"data/account/account.txt"
DUMP_DIR = r"data/dumps/"

# 网络配置
SERVER_HOST = 'localhost'
SERVER_PORT = 14315