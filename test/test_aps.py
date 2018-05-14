from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime


def task1():
    print("我每3秒运行一次")


schedu = BlockingScheduler()
schedu.add_job(task1, "date", run_date=datetime(2018, 5, 14, 14, 54, 30))  # 间隔模式,每隔3秒执行一次,会阻塞main线程

schedu.start()
print('主线程到底了')
