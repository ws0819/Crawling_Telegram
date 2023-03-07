from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from .settings import logger, now

class Make_Data():
    def __init__(self):
        self.last_year = (now - relativedelta(years=1)).strftime('%yY')
        self.now_year = now.strftime('%yY')
    
    def data_remodel(self, crawling_dict, hscode, tag, db):
        select_month, last_w_money = db.select_db(hscode)
        now_w_money = [int(crawling_dict[i][1].replace(',','')) for i in crawling_dict] # 원화
        w_money = last_w_money + now_w_money
        MoM = [None]
        YoY = []
        MoM_now = []
        MoM_now.append((now_w_money[0] / last_w_money[-1]) - 1)

        for i in range(len(now_w_money)): # MoM_now
            try:
                MoM_now.append((now_w_money[i + 1] / now_w_money[i]) - 1)
            except:
                break  
        
        if len(now_w_money) < len(last_w_money):
            for i in range(len(last_w_money) - len(now_w_money)):
                now_w_money.append(0)

        for i in range(len(last_w_money)): # MoM
            if i == len(last_w_money) - 1:
                break
            MoM.append((last_w_money[i + 1] / last_w_money[i]) - 1)

        for i in range(len(last_w_money)): # YoY
            if now_w_money[i]:
                YoY.append((now_w_money[i] / last_w_money[i]) - 1)
            else:
                YoY.append(None)
    
        template = self.make_template(select_month, w_money, MoM, YoY, MoM_now, tag)
        df = pd.DataFrame({self.last_year : last_w_money, self.now_year : now_w_money, self.last_year+'_MoM(%)' : MoM, self.now_year+'_YoY(%)' : YoY}, index = select_month)
        return df, template, select_month
    
    def make_template(self, month, w_money, MoM, YoY, MoM_now, tag):
        template = ""
        ttt = 0
        for idx, _ in enumerate(w_money):
            if idx < 12:
                tmp_MoM_last = ' ,MoM >>' + ' {:.0%}'.format(float(MoM[idx])) if MoM[idx] else ''
                template += self.last_year + str(month[idx]) + ': ' + '{:,.0f}'.format(int(w_money[idx])) + tmp_MoM_last
            else:
                tmp_MoM_now = ' ,MoM >>' + ' {:.0%} ,'.format(float(MoM_now[ttt])) if MoM_now[ttt] else ''
                tmp_YoY_now = ' ,YoY >>' + ' {:.0%}'.format(float(YoY[ttt])) if YoY[ttt] else ''
                template += self.now_year + str(month[ttt]) + ': ' + '{:,.0f}'.format(int(w_money[idx])) + tmp_MoM_now + tmp_YoY_now
                ttt += 1
            template += '\n'          
        template += tag
        return template
    
    def make_photo(self, df, title, hscode, photo_name, month):
        try:
            plt.rcParams['font.family'] = 'NanumGothicCoding' # 한글깨짐 방지

            fig = plt.figure(figsize=(12, 8))
            index = np.arange(len(month))
            bar_width = 0.3
            title_hscode = title + ' - ' + str(hscode)

            ax1 = fig.add_subplot()
            ax1.plot(index, df[self.last_year + '_MoM(%)'], markersize=7, linewidth=5, color='#ff7f0e', alpha=0.7, label=self.last_year + '_MoM(%)', marker='o')
            ax1.plot(index, df[self.now_year + '_YoY(%)'], markersize=7, linewidth=5, color='#820eff', alpha=0.7, label=self.now_year + '_YoY(%)', marker='o')
            ax1.tick_params(axis='y', labelcolor='#d62728')
            ax1.set_yticklabels(['{:.0%}'.format(x) for x in ax1.get_yticks()])
            ax1.legend(loc='upper left')

            ax2 = ax1.twinx()
            ax2.bar(index, df[self.last_year], width = 0.6, alpha=1, color='#1f77b4', label=self.last_year)
            ax2.bar(index + bar_width, df[self.now_year], width = 0.6, alpha=1, color='#2ca02c', label=self.now_year)
            ax2.set_xticks(np.arange(bar_width, 12 + bar_width, 1), month)
            ax2.set_yticklabels(['{:,.0f}'.format(x) for x in ax2.get_yticks()])
            ax2.legend(loc='upper right')

            ax1.set_zorder(ax2.get_zorder() + 10)
            ax1.patch.set_visible(False)

            #워터마크
            #test_wm = plt.imread("./wm.jpg")
            #plt.figimage(test_wm, xo=250, yo=80, resize=False, alpha=0.3)

            plt.title(title_hscode, fontdict = {'fontsize' : 30})
            plt.savefig(photo_name)
            plt.close()
        except Exception as e:
            logger(e)