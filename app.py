from flask import Flask, render_template, request, session, redirect
from modules.money import Money
from modules.user import User
from modules.database import Database
from modules.alert import Alert
from apscheduler.schedulers.background import BackgroundScheduler
from modules.deliver import Deliver

app = Flask(__name__)
app.secret_key = "wuhan"


@app.before_first_request
def inti_request():
    Database.inti()
    # 定义session['email']的功能,否则找不到会报错. 要是浏览器重启,好像也直接报错
    session['email'] = session.get('email')
    session['name'] = session.get('name')

    # 周1到周5,全天,一分钟刷新一次
    clock = BackgroundScheduler()
    clock.add_job(Deliver.send_simple_message, 'cron', day_of_week='0-4', hour="0-23", minute="0-59")
    clock.start()


# 用来显示主页面
@app.route('/')
@app.route('/home')
def home():
    """
    页面:显示汇率主页
    :return:
    """
    moneys_dict = Money.get_data()
    # 使用home页面进行背景页面
    return render_template("home.html", moneys_dict=moneys_dict)


# 用来显示/register的页面
@app.route('/register', methods=["GET", "POST"])
def register():
    """
    页面:用户注册
    :return:
    """
    if request.method == 'POST':
        # 接受表单信息,进行注册
        name = request.form["InputName"]
        email = request.form["InputEmail"]
        password = request.form["InputPassword"]

        result = User.register_user(name, email, password)
        if result is True:
            # 转跳到home页
            session['email'] = email
            session['name'] = name
            return redirect('/')
        else:
            message = "这个email已经存在"
            return render_template("register.html", message=message)
    else:
        return render_template("register.html")


@app.route('/login', methods=["GET", "POST"])
def login():
    """
    页面:用户登录
    :return:
    """
    if request.method == 'POST':
        email = request.form["InputEmail"]
        password = request.form["InputPassword"]

        result = User.check_user(email, password)
        if result is True:
            # 转跳到home页
            session['email'] = email
            session['name'] = User.get_user_data(email)['name']
            return redirect('/')
        else:
            message = "您的电子邮箱或者密码错误!"
            return render_template("login.html", message=message)
    else:
        return render_template("login.html")


@app.route('/logout')
def logout():
    """
    页面:注销用户
    :return:
    """
    session['email'] = None
    session['name'] = None
    return redirect("/")


@app.route('/change_email', methods=["GET", "POST"])
def change_email():
    """
    页面:修改账户的电子邮寄地址
    :return:
    """
    if session['email']:
        if request.method == 'POST':
            new_email = request.form["Input_newemail"]
            password = request.form["InputPassword"]

            if User.exist_user(new_email):
                message = "您输入的新email已经被人使用!"
                return render_template("change_email.html", message=message)

            result = User.check_user(session['email'], password)
            if result is True:
                User.update_user_email(session['email'], new_email)
                session['email'] = new_email
                message = "您的账号邮箱已经更改为{}".format(new_email)
                return render_template("change_email.html", message=message)
            else:
                message = "您的密码输入错误!"
                return render_template("change_email.html", message=message)
        else:
            return render_template("change_email.html")
    else:
        return redirect("/login")


@app.route('/create_alert', methods=["GET", "POST"])
def new_alert():
    """
    页面:监听新的货币
    :return:
    """
    if session['email']:
        money_dict = Money.get_data()
        if request.method == 'POST':
            # 接受表单信息
            Input_current = request.form["Input_current"]
            rate_kind = request.form["rate_kind"]
            buy_price = request.form["buy_price"]
            sell_price = request.form["sell_price"]

            result = Alert.create_alert(email=session['email'], current=Input_current, rate_kind=rate_kind,
                                        price=[buy_price, sell_price])
            if result is True:
                # 创造item成功.返回创建信息

                message = "新的货币监听已经创建成功!"
                current_msg = "货币:{}".format(Input_current)
                rate_kind_msg = "汇率类型:{}".format("现钞" if rate_kind == "cash" else "现汇")
                buy_price_msg = "买入价格:¥ {}".format(buy_price)
                sell_price_msg = "卖出价格:¥ {}".format(sell_price)

                return render_template("create_alert.html", money_dict=money_dict, message=message,
                                       current_msg=current_msg,
                                       rate_kind_msg=rate_kind_msg, buy_price_msg=buy_price_msg,
                                       sell_price_msg=sell_price_msg)
            else:
                # 创造item失败
                message = "创建失败:该货币已被您加入监听!"
                return render_template("create_alert.html", money_dict=money_dict, message=message)
        else:
            # 在登录状态下直接get,则返回创建页面
            return render_template("create_alert.html", money_dict=money_dict)
    else:
        # 没有登录信息,返回login页面
        return redirect("/login")


@app.route('/alert_manage', methods=["GET", "POST"])
def alert_manage():
    """
    功能:用来管理 全部监听卡片
    :return:
    """
    if session['email']:
        if request.method == "POST":
            pass
        alerts_data = Alert.find_user_alert(email=session['email'], rate_kind='cash')
        # alerts_data为一个字典的迭代器
        return render_template("alert_manage.html", alerts_data=alerts_data)
    else:
        return redirect("/login")


@app.route('/alert_update', methods=["POST"])
def alert_update():
    """
    功能:用来处理卡片管理上进行的更新
    :return:
    """
    if request.method == "POST":
        up_current = request.form["up_current"]
        up_rate_kind = request.form["up_rate_kind"]
        up_buy_price = request.form["up_buy_price"]
        up_sell_price = request.form["up_sell_price"]
        # 未写删除sign类型的判断
        if up_rate_kind == "cash":
            Alert.update_user_alert(session['email'], current=up_current, rate_kind=up_rate_kind
                                    , price=[up_buy_price, up_sell_price])
            return redirect('/alert_manage')


@app.route('/alert_delete', methods=["POST"])
def alert_delete():
    """
    功能:用来处理卡片管理上进行的更新
    :return:
    """
    if request.method == "POST":
        up_current = request.form["up_current"]
        up_rate_kind = request.form["up_rate_kind"]
        if up_rate_kind == "cash":
            Alert.delete_user_alert(session['email'], current=up_current, rate_kind=up_rate_kind)
            return redirect('/alert_manage')


if __name__ == '__main__':
    app.run(debug=True, port="10111")
