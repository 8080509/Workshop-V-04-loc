def day_date_int(str):
    return 10 * int(str[-2]) + int(str[-1])


lastdayofmonth = {'01-31', '02-28', '03-31', '04-30', '05-31', '06-30', '07-31', '08-31', '09-30', '10-31', '11-30',
                  '12-31'}


def datetodayssincelastpayday(str):
    if str == '2016-02-28':
        return 13
    if str == '2016-02-29':
        return 0
    if str[-5:] in lastdayofmonth:
        return 0
    else:
        if day_date_int(str) >= 15:
            return day_date_int(str) - 15
        else:
            return day_date_int(str)


arr = [0] * len(data['date'])
for i in range(len(data['date'])):
    arr[i] = datetodayssincelastpayday(data['date'][i])
data['dayssincepaid'] = arr