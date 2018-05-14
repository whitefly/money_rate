from modules.user import User
from modules.database import Database
from modules.money import Money
import requests


class Deliver(object):
    @staticmethod
    def __check_ok(new_prices, set_prices) -> bool:
        """
        功能:提醒策略
        :param new_prices:
        :param set_prices:
        :return:
        """
        new_buy, new_sell = new_prices
        set_buy, set_sell = set_prices
        if new_buy == '-' or new_sell == '-':
            return False
        if set_buy > new_buy and set_sell < new_sell:
            return True
        return False

    @staticmethod
    def __get_emails() -> dict:
        """
        返回通知的email和对应币种
        :return:
        """
        # 再次抓取汇率
        money_dict = Money.get_data()

        # 暴力扫符合条件的email
        users_list = Database.get_all("user")
        emails_list = [one['email'] for one in users_list]
        result = {}
        for email in emails_list:
            user_result = []
            user_all_alert = Database.find(collection="Alerts", query={"email": email})
            for user_alert in user_all_alert:
                if user_alert['rate_kind'] == 'cash':
                    current = user_alert['current']
                    new_prices = (money_dict[current].cash_in, money_dict[current].cash_out)
                    set_prices = user_alert['price']
                    if Deliver.__check_ok(new_prices, set_prices):
                        user_result.append(current)
            if len(user_result) != 0:
                result[email] = user_result
        return result

    @staticmethod
    def send_simple_message():
        result = Deliver.__get_emails()
        if len(result) != 0:
            for user in result:
                content = "您监听的 {} 已经达到目标值,请前去查看".format(",".join(result[user]))
                print(user, content)
                requests.post(
                    "https://api.mailgun.net/v3/sandboxb113c1d7cad9427bb8265e53e7f2975a.mailgun.org/messages",
                    auth=("api", "key-e10bb8f6360db3eaf252d5e21710e9f7"),
                    data={"from": "汇率监控通知 <postmaster@sandboxb113c1d7cad9427bb8265e53e7f2975a.mailgun.org>",
                          "to": [user],
                          "subject": "货币达到通知价格",
                          "text": content})


    # @staticmethod
    # def add_toList():
    #     return requests.get(
    #         "https://api.mailgun.net/v3/address/validate",
    #         auth=("api", "pubkey-4d5a2ea638a10fe49ef4cc99993ea9d4"),
    #         params={"address": ""})
