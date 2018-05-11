from modules.alert import Alert
from modules.database import Database

Database.inti()

data = Alert.find_user_alert("316447675@qq.com", rate_kind="cash")
print(data)
for i in data:
    print(i['price'][0])
