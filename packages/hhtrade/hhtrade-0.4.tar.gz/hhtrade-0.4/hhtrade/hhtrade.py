import time
import pandas as pd
from tqsdk import TqApi, TqAuth, TqKq, TargetPosTask
from tqsdk.datetime import _cst_now,_get_trade_timestamp,_datetime_to_timestamp_nano,_convert_user_input_to_nano
from datetime import datetime,timedelta
import math
import numpy as np
from itertools import groupby
import random
import os
import csv


class orderclass:
    def __init__(self,api = None , targetposition = None ):
        self.api = api
        self.targetposition = targetposition
        assert self.checkcorrectcode(), "请检查品种代码"
        self.oldposition = self.get_initposition()
        self.printposition()
        self.get_orderquote()


    def checkcorrectcode(self):
        for k in self.targetposition.keys():
            try:
                quote = self.api.get_quote(k)
            except:
                print(f"{k} 查询合约服务报错 ,请检查品种代码")
                return False
        return True





    def printposition(self):
        initialholdings = self.api.get_position()
        for k in initialholdings.keys():
            p = self.api.get_position(f"{k}")
            print(
                f"{p.instrument_id} 历史多头持仓 {p.pos_long_his}, 今日多头持仓 {p.pos_long_today}, 历史空头持仓 {p.pos_short_his} , 今日空头持仓 {p.pos_short_today}, 当前多头总持仓 {p.pos_long}, 当前空头总持仓 {p.pos_short}")

    def get_initposition(self):
        initialholdings = self.api.get_position()
        initialholdingdict = {}
        for k in initialholdings.keys():
            initialholdingdict[k] = initialholdings[k].volume_long - initialholdings[k].volume_short
        return initialholdingdict


    def get_orderquote(self):
        order_diff, order_direction = self.calculate_order(self.oldposition, self.targetposition )
        self.orderqueue = self.order_to_queue(dict_data=order_diff.copy())
        self.orderplan =  self.orderplanset( oldposition = self.oldposition,targetposition = self.targetposition,\
                                             orderqueue = self.orderqueue,\
                                             order_direction = order_direction, \
                                             maxvol=5)


    def calculate_order(self,dict1, dict2):
        """
        计算交割单的差异和方向
        """
        all_keys = set(dict1.keys()).union(set(dict2.keys()))
        difference = {}
        direction = {}
        for key in all_keys:
            difference[key] = abs(dict2.get(key, 0) - dict1.get(key, 0))
            direction[key] = int(np.sign(dict2.get(key, 0) - dict1.get(key, 0)))
        return difference, direction

    def order_to_queue(self, dict_data):
        """
        将订单dict 变为执行序列 完全随机
        """
        # 获取股指期货序列
        queue = []
        for key, value in dict_data.items():
            queue.extend([key] * value)
        # 打乱股指期货序列
        random.shuffle(queue)
        # 到这里，理论上应该 dict_data 全是 0
        return queue

    def dictmatch(self,dict1, dict2):
        newdict = dict1.copy()
        for k in dict2:
            if k not in dict1:
                newdict[k] = 0
        return newdict

    def orderplanset(self, oldposition, targetposition, orderqueue, order_direction, maxvol=5):
        """
        这一步的目的是，限定了单次调仓的最大笔数。因为可能出现国债太多，尽管已经均匀切分，但是对市场冲击还是很大，通过maxvol，设定最大下单手数
        """
        grouped_order = [(key, len(list(group))) for key, group in groupby(orderqueue)]
        result_order = []
        for key, count in grouped_order:
            while count > maxvol:
                result_order.append((key, maxvol))
                count -= maxvol
            if count > 0:
                result_order.append((key, count))
        orderplan = []

        recorddict = self.dictmatch(oldposition, targetposition)
        targetpositiondict = self.dictmatch(targetposition, oldposition)

        for k,v in recorddict.items():
            if v==0:
                orderplan.append([k, 0])

        for order_tp in result_order:
            recorddict[order_tp[0]] = recorddict[order_tp[0]] + order_direction[order_tp[0]] * order_tp[1]
            orderplan.append([order_tp[0], recorddict[order_tp[0]]])

        orderplan = pd.DataFrame(orderplan, columns=['sid', 'targetvol'])

        last_tg = pd.DataFrame(oldposition.items(), columns=['sid', 'targetvol'])._append(orderplan).drop_duplicates(
            subset='sid', keep='last')

        # 检查经过目标调仓序列是不是可以完成调仓目标
        if targetpositiondict == last_tg.set_index('sid').to_dict()['targetvol']:
            print("目标调仓序列可以达到最终持仓目标")
        else:
            assert False, "目标调仓序列不可以达到最终持仓目标"
        return orderplan

    def dynamic_sendorder(self, dforderplan = None, timestart = None, timeend =None ):
        """
        datetime.strptime(timestart, '%Y-%m-%d %H:%M:%S.%f')
        """
        print("开始执行交易")
        if len(dforderplan) == 0:
            print("无需调仓")
            return 0
        timestart = datetime.strptime(timestart, '%Y%m%d %H:%M:%S')
        timeend = datetime.strptime(timeend, '%Y%m%d %H:%M:%S')
        timestart_nano, timeend_nano = _convert_user_input_to_nano(timestart,timeend )

        #每次成交中间间隔纳秒
        timedaly = int((timeend_nano - timestart_nano) / (len(dforderplan)) / 1000000000)

        unfinishorder = []

        for index, orderrow in self.orderplan.iterrows():
            # break
            # print(orderrow)
            newsetposition = self.get_initposition()

            if orderrow.sid in newsetposition:
                # print(index, orderrow)
                # "ACTIVE" 对价下单，在持仓调整过程中，若下单方向为买，对价为卖一价；若下单方向为卖，对价为买一价。
                # "昨开" 表示先平昨仓，再开仓，禁止平今仓，适合股指这样平今手续费较高的品种
                target_pos_active = TargetPosTask(self.api, orderrow.sid, price="ACTIVE",offset_priority="昨开")
                target_pos_active.set_target_volume(orderrow.targetvol)
                nethold = target_pos_active._pos.volume_long -  target_pos_active._pos.volume_short
                t = time.time()
                ifhavetime = True
                while (nethold)!= orderrow.targetvol and ifhavetime:
                    self.api.wait_update()
                    nethold = target_pos_active._pos.volume_long -  target_pos_active._pos.volume_short
                    # print(f"当前{orderrow.sid} 目标变动 {orderrow.targetvol}  当前持仓 空 {target_pos_active._pos.volume_short} 多 {target_pos_active._pos.volume_long}" )
                    costtime = time.time() - t
                    if costtime>timedaly:
                        print(f"交易花费时间{costtime} 超过阈值时间{timedaly}")
                        ifhavetime = False
                        unfinishorder.append([orderrow.sid, orderrow.targetvol , nethold ]  )

            else:
                directioni = "BUY" if orderrow.targetvol >0 else "SELL"
                quote = self.api.get_quote(orderrow.sid)
                if directioni == "BUY":
                    lc = quote.ask_price1
                else:
                    lc = quote.bid_price1
                order = api.insert_order(symbol = orderrow.sid, direction=directioni, offset="OPEN",
                                         limit_price=lc,
                                         volume = orderrow.targetvol)
                ifhavetime = True
                t = time.time()
                while order.status != "FINISHED":
                    self.api.wait_update()
                    print("单状态: %s, 已成交: %d 手" % (order.status, order.volume_orign - order.volume_left))
                    costtime = time.time() - t
                    if costtime>timedaly:
                        print(f"交易花费时间{costtime} 超过阈值时间{timedaly}")
                        ifhavetime = False
                        unfinishorder.append([orderrow.sid, orderrow.targetvol, order.volume_orign - order.volume_left])

            timestart_nano_s, timeend_nano_e = _convert_user_input_to_nano( _cst_now(), timeend )
            timedaly = int(( timeend_nano_e  - timestart_nano_s)/ (len(dforderplan)-index) /1000000000 )
            time.sleep(timedaly )

        print("调仓完成")
        return unfinishorder

    def tradeorder(self, timestart = None, timeend = None , delaydt = 60):

        timestart = self.checktimestart(inputtime=timestart)
        timeend = self.checktimeend(inputtime=timeend, delaydt=delaydt)
        self.unfinishorder =  self.dynamic_sendorder( dforderplan= self.orderplan , timestart=timestart, timeend=timeend)
        if len(self.unfinishorder) == 0:
            self.printposition()
        else:
            assert False,"重大错误，存在未成交订单"


    def checktimeend(self, inputtime = None, delaydt = 60):
        """
        检查输入时间是不是晚于当前时间
        inputtime 格式需要满足 '%Y%m%d %H:%M:%S' 例如 '20240815 10:10:00'
        """
        if inputtime is None:
            inputtime = datetime.now() +  timedelta(seconds=delaydt)
            return inputtime.strftime( '%Y%m%d %H:%M:%S')
        deltat = (datetime.now() - datetime.strptime(inputtime, '%Y%m%d %H:%M:%S')).total_seconds()
        assert (deltat < 0 ),'输入时间 应该晚于当前时间'



    def checktimestart(self, inputtime = None):
        """
        检查输入时间是不是晚于当前时间
        inputtime 格式需要满足 '%Y%m%d %H:%M:%S' 例如 '20240815 10:10:00'
        """
        if inputtime is None:
            inputtime = time.strftime('%Y%m%d %H:%M:%S', time.localtime())
            return inputtime
        else:
            deltat = (datetime.now() - datetime.strptime(inputtime, '%Y%m%d %H:%M:%S')).total_seconds()
            if deltat >0 :
                inputtime = time.strftime('%Y%m%d %H:%M:%S', time.localtime())
                print("调整输入时间为当前时间")
                return inputtime
            else:
                while deltat<0:
                    deltat = (datetime.now()- datetime.strptime(inputtime, '%Y%m%d %H:%M:%S')).seconds
                    print(f"未到下单时间 需要等待 {deltat}")
                    time.sleep(1)
                inputtime = time.strftime('%Y%m%d %H:%M:%S', time.localtime())
                return inputtime

    def downloader_orders(self):
        order_cols = ["order_id", "exchange_order_id", "exchange_id", "instrument_id", "direction", "offset", "status",
                      "volume_orign", "volume_left", "limit_price", "price_type", "volume_condition", "time_condition",
                      "insert_date_time", "last_msg"]
        trade_cols = ["trade_id", "order_id", "exchange_trade_id", "exchange_id", "instrument_id", "direction",
                      "offset", "price", "volume", "trade_date_time"]
        def write_csv(file_name, cols, datas):
            file_exists = os.path.exists(file_name) and os.path.getsize(file_name) > 0
            with open(file_name, 'a', newline='') as csvfile:
                csv_writer = csv.writer(csvfile, dialect='excel')
                if not file_exists:
                    csv_writer.writerow(['datetime'] + cols)
                for item in datas.values():
                    if 'insert_date_time' in cols:
                        dt = datetime.fromtimestamp(item['insert_date_time'] / 1e9).strftime('%Y-%m-%d %H:%M:%S.%f')
                    elif 'trade_date_time' in cols:
                        dt = datetime.fromtimestamp(item['trade_date_time'] / 1e9).strftime('%Y-%m-%d %H:%M:%S.%f')
                    else:
                        dt = None
                    row = [dt] + [item[k] for k in cols]
                    csv_writer.writerow(row)
        with self.api as api:
            # 将当前账户下全部委托单、成交信息写入 csv 文件中
            write_csv("orders.csv", order_cols, api.get_order())
            write_csv("trades.csv", trade_cols, api.get_trade())

