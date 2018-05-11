import pandas as pd
import numpy as np


def change_NaN(num):
    return num if num is not np.NAN else '-'


class Money(object):
    def __init__(self, c, cash_in, cash_out, ex_in, ex_out):
        self.current = c
        self.cash_in = cash_in
        self.cash_out = cash_out
        self.ex_in = ex_in
        self.ex_out = ex_out

    @staticmethod
    def get_data() -> dict:
        """
        从人民银行来获取汇率
        return: money实例的字典
        """

        rate_url = "http://www.boc.cn/sourcedb/whpj/index.html"
        current_table = (pd.read_html(rate_url))[1]  # type:pd.DataFrame
        current_table.columns = current_table.ix[0]
        current_table.drop([0], inplace=True)  # 修改列名,删除第一行

        moneyDict = {}
        for i in range(len(current_table)):
            dollar = current_table.values[i]
            moneyDict[dollar[0]] = Money(change_NaN(dollar[0]), change_NaN(dollar[2]), change_NaN(dollar[4]),
                                          change_NaN(dollar[1]), change_NaN(dollar[3]))

        return moneyDict
