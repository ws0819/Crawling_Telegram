import datetime, json, os, sys
from lib.crawling import Crawling
from lib.database import DB
from lib.telegram import TeleGram
from lib.make_data import Make_Data
from lib.settings import logger, make_folder, args_check, json_check, now, photo_path

def run(hscode_dict, crawling, db, tele, make):
    menus = ''
    menus += '#수출입데이터 ' + now.strftime('#%Y년%m월%d일') + '\n'

    for title in hscode_dict:
        tag = '#수출입데이터' + ' ' + '#' + title + ' ' + now.strftime('#%Y년%m월%d일')    
        photo_name = photo_path + str(hscode_dict[title]) + '_' + str(now.year) + str(now.month) + str(now.day) + '.png'
        crawling_dict = crawling.get_search(hscode_dict[title])
        df, template, month = make.data_remodel(crawling_dict, hscode_dict[title], tag, db)
        make.make_photo(df, title, hscode_dict[title], photo_name, month)
        tele.send_photo(photo_name, template)
        db.insert_update_db(title, hscode_dict[title], crawling_dict)
        menus += '#' + title + '\n'
    tele.send_message(menus)

def main():
    crawling = Crawling()
    db = DB()
    tele = TeleGram()
    make = Make_Data()

    for json_file in json_list:
        with open(json_path + json_file, 'r', encoding='utf-8') as f:
            hscode_dict = json.load(f)
        run(hscode_dict, crawling, db, tele, make)
        f.close()    

    db.cs.close()

if __name__ == '__main__':
    args = sys.argv
    json_path = args_check(args)
    json_list = json_check(json_path)

    logger(f"Main started at {now}")
    make_folder()
    main()
    et = datetime.datetime.now()
    logger(f"Main finished at {et}")
    logger(f"Main time for task: {et-now}")
    os.system("sudo rm -rf {photo_path}*.png".format(photo_path=photo_path))