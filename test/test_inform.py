a = [5, '-']

buy, sell = a
if buy != '-' and sell != '-':
    if buy > 4 and sell > 5:
        print("通知:\n    购买价格:{} 卖出价格:{}".format(buy, sell))
    else:
        print("pass")
else:
    print("pass")
