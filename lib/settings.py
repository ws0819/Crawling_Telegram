import datetime, os, sys

DB_info = {
    "host": "127.0.0.1",
    "port": 5432,
    "user": "",
    "password": "",
    "database": "",
}
TeleGram_info = {
    "telegram_token": "", # bot_token
    "telegram_chat_id": -1, # chat_id

}
path = os.getcwd()
log_path = path + "/tc_logs"
photo_path = path + "/tmp_photo/"
base_json_path = path + "/tmp_json/"

now = datetime.datetime.now()

def logger(msg):
    open(log_path, 'a').write(str(datetime.datetime.today()) + str(' -> ') + repr(msg) + '\n')

def make_folder():
    if not os.path.exists(photo_path):
        os.makedirs(photo_path)

def args_check(args):
    if len(args) != 2:
        return base_json_path
    else:
        check_path = args[1]
        if not os.path.isdir(check_path):
            logger(str(check_path + " path error // base_json_path"))
            return base_json_path
        else:
            logger(str(check_path + " json_path"))
            if check_path[-1] != '/':
                check_path += '/'
            return check_path

def json_check(json_path):
    a = [i for i in os.walk(json_path)]
    file_list = a[0][2]
    if len(file_list) == 0:
        logger("no json")
        return sys.exit()
    for j in file_list:
        if j[:4] != 'json':
            logger("file error. // only json file")
            return sys.exit()
    return file_list