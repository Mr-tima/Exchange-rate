import matplotlib.pyplot as plt
from matplotlib import *
import datetime as dt
from matplotlib import dates
import cx_Oracle


def PlotGraph(coin, start=0, end=0):
    price = []
    time = []
    start *= 1000
    end *= 1000

    dsnStr = cx_Oracle.makedsn(host="localhost", port="1521", sid="dborcl")
    con = cx_Oracle.connect(user="user1", password="123", dsn=dsnStr)
    cur = con.cursor()
    if start == 0 and end == 0:
        cur.execute("SELECT * FROM id_data_price WHERE id = '%s' ORDER BY unix_time" % coin)
    elif start != 0 and end == 0:
        cur.execute("SELECT * FROM id_data_price WHERE UNIX_TIME > %d AND id = '%s' ORDER BY unix_time" % (start, coin))
    elif start == 0 and end != 0:
        cur.execute("SELECT * FROM id_data_price WHERE UNIX_TIME < %d AND id = '%s' ORDER BY unix_time" % (end, coin))
    else:
        cur.execute("SELECT * FROM id_data_price WHERE (UNIX_TIME BETWEEN %d AND %d) AND (id = '%s') ORDER BY unix_time" % (
        start, end, coin))

    result = cur.fetchall()

    for i in result:
        time.append(dt.datetime.strptime('%s' % dt.datetime.fromtimestamp(int(i[2]) / 1000), "%Y-%m-%d %H:%M:%S"))
        price.append(i[3])

    cur.close()
    con.close()

    rcParams['toolbar'] = 'None'
    fmt = dates.DateFormatter('%d-%m-%Y')

    fig, ax = plt.subplots()

    ax.plot(time, price)
    ax.xaxis.set_major_formatter(fmt)
    fig.autofmt_xdate()

    return fig


if __name__ == '__main__':
    PlotGraph()
