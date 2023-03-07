from .settings import logger, DB_info, now
from dateutil.relativedelta import relativedelta
import psycopg2

class DB:
    def __init__(self):
        conn = psycopg2.connect(host = DB_info['host'], port = DB_info['port'], user = DB_info['user'], password = DB_info['password'], database = DB_info['database'])
        self.cs = conn.cursor()

    def execute_db(self, sql):
        try:
            self.cs.execute(sql)
        except Exception as e:
            logger(e) 

    def select_db(self, hscode):
        month = []
        w_money = []
        select_sql ='''
                SELECT date, price_w FROM "test"."test" WHERE hscode = {hscode} AND date like '%{year}%' ORDER BY date 
            '''.format(hscode=hscode, year=int(now.year) -1)
        try:
            self.cs.execute(select_sql)
            rs = self.cs.fetchall()
        except Exception as e:
            logger(e) 

        for r in rs:
            month.append(str(r[0]).strip()[-2:] + 'M')
            w_money.append(int(str(r[1]).strip().replace(',','')) if ',' in str(r[1]).strip() else int(str(r[1]).strip()))
        return month, w_money
    
    def insert_update_db(self, title, hscode, crawling_dict):
        d = [str(crawling_dict[i][0].replace(',','')) for i in crawling_dict] # 달러
        w = [str(crawling_dict[i][1].replace(',','')) for i in crawling_dict] # 원
        k = [str(crawling_dict[i][2].replace(',','')) for i in crawling_dict] # 중량

        if now.strftime('%d') == '01':
            update1_sql = '''
                UPDATE "test"."test"
                SET "price_d" = '{price_d}', "price_d_late" = '{price_d_late}', "price_w" = '{price_w}', "price_w_late" = '{price_w_late}', "weight" = '{weight}', "weight_late" = '{weight_late}', "price_d_per_weight" = '{price_d_per_weight}', "price_d_per_weight_late" = '{price_d_per_weight_late}'
                WHERE "hscode" = '{hscode}' AND "date" = '{date}'
            '''.format(
                price_d = d[-1], price_d_late = d[-1],
                price_w = w[-1], price_w_late = w[-1],
                weight = k[-1], weight_late = k[-1],
                price_d_per_weight = str(int(d[-1]) / float(k[-1])), price_d_per_weight_late = str(int(d[-1]) / float(k[-1])),
                hscode = hscode, date = (now - relativedelta(month=1)).strftime('%Y-%m')
            )
            self.execute_db(update1_sql)

        elif now.strftime('%d') == '11':
            insert_sql = '''
            INSERT INTO "test"."test"
                ("name", "hscode", "date", "price_d", "price_d_early", "price_d_middle", "price_d_late", "price_w", "price_w_ealry", "price_w_middle", "price_w_late", "weight", "weigth_early", "weight_middle", "weight_late", "price_d_per_weight", "price_d_per_weight_early", "price_d_per_weight_middle", "price_d_per_weight_late")
            VALUES
                ('{name}', '{hscode}', '{date}', '{price_d}', '{price_d_early}', '{price_d_middle}', '{price_d_late}', '{price_w}', '{price_w_ealry}', '{price_w_middle}', '{price_w_late}', '{weight}', '{weigth_early}', '{weight_middle}', '{weight_late}', '{price_d_per_weight}', '{price_d_per_weight_early}', '{price_d_per_weight_middle}', '{price_d_per_weight_late}')
            '''.format(
                name = title, hscode = hscode, date = self.now.strftime('%Y-%m'),
                price_d = d[-1], price_d_early = d[-1], price_d_middle = '', price_d_late = '',
                price_w = w[-1], price_w_ealry = w[-1], price_w_middle = '', price_w_late = '',
                weight = k[-1], weigth_early = k[-1], weight_middle = '', weight_late = '',
                price_d_per_weight = str(int(d[-1]) / float(k[-1])), price_d_per_weight_early = str(int(d[-1]) / float(k[-1])), price_d_per_weight_middle = '', price_d_per_weight_late = '' # 달러 / 중량
            )
            self.execute_db(insert_sql)

        elif now.strftime('%d') == '21':
            update21_sql = '''
                UPDATE "test"."test"
                SET "price_d" = '{price_d}', "price_d_middle" = '{price_d_middle}', "price_w" = '{price_w}', "price_w_middle" = '{price_w_middle}', "weight" = '{weight}', "weight_middle" = '{weight_middle}', "price_d_per_weight" = '{price_d_per_weight}', "price_d_per_weight_middle" = '{price_d_per_weight_middle}'
                WHERE "hscode" = '{hscode}' AND "date" = '{date}'
            '''.format(
                price_d = d[-1], price_d_middle = d[-1],
                price_w = w[-1], price_w_middle = w[-1],
                weight = k[-1], weight_middle = k[-1],
                price_d_per_weight = str(int(d[-1]) / float(k[-1])), price_d_per_weight_middle = str(int(d[-1]) / float(k[-1])),
                hsdocde = hscode, date = now.strftime('%Y-%m'),
            )
            self.execute_db(update21_sql)