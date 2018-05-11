from modules.database import Database
import json
from passlib.hash import pbkdf2_sha512


class User(object):
    collection_name = "user"

    def __init__(self, user_name, user_email, user_password):
        self.user_name = user_name
        self.user_email = user_email
        self.user_password = user_password

    @staticmethod
    def register_user(name, email, passowrd) -> bool:
        """
        用户注册功能
        处理已经注册 和 新注册
        """
        user_data = Database.find_one(collection=User.collection_name, query={"email": email})
        if user_data is not None:
            # 用户已经注册,新注册失败
            return False

        # 注册新用户
        new_user = User(name, email, User.hash_password(passowrd))
        new_user.save_to_DB()
        return True

    @staticmethod
    def check_user(email, password) -> bool:
        """
        用户登录功能
        进行用户不存在和密码错误的验证
        """
        user_data = Database.find_one(collection=User.collection_name, query={"email": email})
        # 不存在的用户
        if user_data is None:
            return False

        # 密码错误
        if User.check_hash_password(password, user_data["password"]) is False:
            return False

        return True

    @staticmethod
    def exist_user(email) -> bool:
        user_data = Database.find_one(collection=User.collection_name, query={"email": email})
        return (user_data is not None)

    @staticmethod
    def get_user_data(email) -> dict:
        """
        用户登录后,返回用户信息
        """
        return Database.find_one(User.collection_name, query={"email": email})

    @staticmethod
    def hash_password(password):
        return pbkdf2_sha512.hash(password)

    @staticmethod
    def check_hash_password(password, hash_password) -> bool:
        # 用户输入密码和数据库的hash密码进行对比
        return pbkdf2_sha512.verify(password, hash_password)

    @staticmethod
    def update_user_email(old_email, new_email):
        """
        用来修改用户的邮箱
        """
        return Database.update_one(User.collection_name, query={"email": old_email},
                                   data={"$set": {"email": new_email}})

    def __get_info(self) -> json:
        # 用来进行用户信息存储
        return {"name": self.user_name, "email": self.user_email, "password": self.user_password}

    def save_to_DB(self):
        Database.insert(collection=User.collection_name, data=self.__get_info())
