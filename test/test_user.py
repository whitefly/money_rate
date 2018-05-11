from modules.user import User
from modules.database import Database

old_email = "416447677@qq.com"
new_email = "516447677@qq.com"

Database.inti()
print(User.exist_user(new_email))
