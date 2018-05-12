from modules.user import User
from modules.database import Database


def get_emails():
    """
    返回通知的币种
    :return:
    """

    users_list = Database.find_all("user")
    return [one['email'] for one in users_list]


Database.inti()
print(get_emails())
