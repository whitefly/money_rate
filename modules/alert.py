from modules.database import Database
import json


class Alert(object):
    collection_name = "Alerts"

    def __init__(self, user_email, current, rate_kind, price):
        self.email = user_email
        self.current = current
        self.rate_kind = rate_kind
        self.price = price

    @staticmethod
    def create_alert(email, current, rate_kind, price):
        """
        功能:插入新的监控信息
        每一行: email,货币,汇率种类,价格
        """
        data_result = Database.find_one(collection=Alert.collection_name,
                                        query={"email": email, "current": current, "rate_kind": rate_kind})
        if data_result is not None:
            return False
        Alert(email, current, rate_kind, price).save_to_DB()
        return True

    @staticmethod
    def find_user_alert(email, rate_kind) -> dict:
        """
        功能:返回 用户的关注的所有货币
        """
        return Database.find(Alert.collection_name, query={"email": email, "rate_kind": rate_kind})

    @staticmethod
    def update_user_alert(email, current, rate_kind, price):
        """
        功能:修改 货币监控价格
        """
        return Database.update_one(Alert.collection_name, query={"email": current, "rate_kind": rate_kind},
                                   data={"$set": {"email": price}})

    def __get_info(self) -> json:
        # 封装为json格式进行插入
        return {
            "email": self.email,
            "current": self.current,
            "rate_kind": self.rate_kind,
            "price": self.price}

    def save_to_DB(self):
        Database.insert(collection=Alert.collection_name, data=self.__get_info())
