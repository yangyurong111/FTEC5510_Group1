import math
import chardet
from FTEC5510_tool import *
def readfile(file):
    try:
        string=open(file,'r',encoding='utf8').read()
        return string
    except UnicodeDecodeError as e:
        pass
    try:
        string = open(file, 'r', encoding='gbk').read()
        return string
    except UnicodeDecodeError as e:
        pass
    try:
        encode = chardet.detect(open(file, 'rb').readline())['encoding']
        string = open(file, 'r', encoding=encode).read()
        return string
    except UnicodeDecodeError as e:
        pass
    # 都不行
    print('读取文件出错！utf\gbk\chardet都试过了：',file)
def iskong(o):
    if o is None: return True
    if o!=o:return True#np.nan会出现这种情况
    #int类型返回非空
    if str(type(o)).find('int') != -1:return False#int是不能用len()方法的
    if str(type(o)).find('long') != -1: return False
    if str(type(o)).find('float')!=-1: return False #可能出现numpy.float64 这种鬼。
    if len(o)==0:return True
    #if o=='':return True
    return False
def csvStr_to_arr_table(csv_str,delimiter=','):
    if iskong(csv_str):
        return None
    arr=[]
    text=csv_str
    text=text.replace('\r\n','\n')
    for line in text.split('\n'):
        arr2=line.split(delimiter)
        arr.append(arr2)
    return arr
def csv_to_arr(csvfile,delimiter=','):
    text=readfile(csvfile)
    return csvStr_to_arr_table(csv_str=text,delimiter=delimiter)
'''
index可以是数字也可以是list
例如：arr_table：[[1, 2, 3], [3, 4, 5]]
get_columns_of_table(1,arr_table)
返回：[2, 4]
get_columns_of_table([1,2],arr_table)
返回：[[2, 3], [4, 5]]

'''
#获取arr_table的特定column，可以是数组或者数字
def get_columns_of_table(index,arr_table):
    new_arr_table=[]
    if try_once(lambda:index[0],False,None) is None:
        #index是一个数
        new_arr=[]
        for arr in arr_table:
            new_arr.append(arr[index])
        return new_arr
    else:
        indexs=index
    for arr in arr_table:
        new_arr=[]
        for index in indexs:
            new_arr.append(arr[index])
        new_arr_table.append(new_arr)
    return new_arr_table
'''
例如：arr_table=[['5575', 'Womenswear', '-1'],['55', 'Womenswear', '77']]
def panduan(a):
    if int(a)>-2:return True
    else:return False
find_items_by_func(panduan,arr_table,on=2)
返回：[['5575', 'Womenswear', '-1']]

参数on设置为-1，就是对整个row施加func，这个可以用来判断列A大于列B的row
找不到返回None
'''
#根据函数判断抓取某些行
def find_items_by_func(func, arr_table, on=0):
    new_arr_table=[]
    for arr in arr_table:
        if on<0:
            if func(arr):
                new_arr_table.append(arr)
        elif func(arr[on])==True:
            new_arr_table.append(arr)
    if iskong(new_arr_table):
        return None
    return new_arr_table
def try_once(func,needPrint=False,return_when_error=None,ignore_conflict=False):

    try:
        a=func()
        if a ==return_when_error :
            pass
        else:
            return a
    except BaseException as e:
        if needPrint:print('错误代码：' + str(e) )
        return return_when_error
    #处理a是None或者a和设定的错误返回值一样的情况
    if ignore_conflict==False:
        raise Exception('函数未出错情况下返回值和错误返回值相同，请注意！返回值为：'+str(return_when_error))
    else:
        return a








#——————————正式的业务代码——————————————————
'''
'''



#print(f'第{i+1}种更好')


def xuanze(username):
    # 天数、利率、最低投入金额
    products=[[2,0.001,100],[4,0.0025,1000],[8,0.0055,5000],[20,0.02,18000]]
    r=readfile('5510_invest_name.txt')
    products=[]
    for i in r.split('\n'):
        temp=i.split('@')
        rate=float(temp[1].strip('%'))/100/360*int(temp[3])
        products.append([int(temp[3]),rate,int(temp[4])])
    #print(products)
    #data = csv_to_arr('5510_user_data_dashuang.csv')
    data2=[]
    temp1=fetch_data("5510_user_data_deposit.csv", name='Date')
    temp2=fetch_data("5510_user_data_deposit.csv", name=username)
    for i in range(1,366):
        if temp2[i]:
            k1=temp2[i].split('@')[0].split(':')[1]
            k2 = temp2[i].split('@')[1].split(':')[1]
            if k1=='0':
                data2.append([temp1[i],'-'+k2])
            else:
                data2.append([temp1[i],k1])
        else:
            data2.append([temp1[i], ""])
        #i[1]=fetch_data("5510_user_data_deposit.csv", name=username, date=i[0])
    data = find_items_by_func(lambda row: True if len(row) >= 2 else False, data2)  # 去空

    # 增加一列，表示当前时点的最小余额
    a = 0
    for row in data.copy():
        if iskong(row[1]):
            rmb = 0
        else:
            rmb = int(row[1])
        if rmb >= 0:
            min_balance = 0
        else:
            min_balance = -rmb
        row.append(min_balance)

    # print(data)

    def cal_profit(product):
        asset = {'cash': 0, 'invest': 0, 'invest_due': 10000, 'profit': 0}  # 现金、投资、投资剩余到期时间、利润
        for row in data:
            if iskong(row[1]) == False:
                if int(row[1]) > 0:
                    # print(f'{row[0]} 存入现金{row[1]}')
                    asset['cash'] += int(row[1])
                if int(row[1]) < 0:
                    # print(f'{row[0]} 取出现金{row[1]}')
                    asset['cash'] += int(row[1])  # 注意也是加号
            # 如果投资已经到期的，转回cash
            if asset['invest_due'] > 0:
                asset['invest_due'] -= 1
            if asset['invest_due'] <= 0 and asset['invest'] > 0:
                profit = asset['invest'] * product[1]
                asset['profit'] += profit
                # print(f'{row[0]} 卖出投资:{asset["invest"]}，赚了{profit}')
                asset['cash'] += asset['invest']
                asset['invest'] = 0
                asset['invest_due'] = 100000

            # 开始计算是否应该买入投资

            # 首先看有没有现金，没有现金那还说个啥
            if (asset['cash']) <= 0:
                continue

            # 如果投资期限超过了年底，也不用投了
            row_index = data.index(row)

            if row_index + product[0] >= len(data):
                continue

            # 然后看后面几天要求余额的最高值
            min_balance = max(get_columns_of_table(2, data[row_index:row_index + product[0]]))
            available_cash = asset['cash'] - min_balance
            if available_cash <= 0:
                continue

            # 然后看看钱够不够投资的最低要求
            if available_cash < product[2]:
                # print(f'{row[0]} 没到投资的最低金额，不能买')
                continue

            # 如果到了年底

            # 买invest
            # print(f'{row[0]} 买投资:{available_cash}')
            asset['invest'] += available_cash
            asset['cash'] -= available_cash
            asset['invest_due'] = product[0]

        # print(f'总共赚了：{asset["profit"]}元')
        return asset["profit"]
    l = []
    for product in products:
        # print(products.index(product)+1)
        l.append(cal_profit(product))
    #print(l)
    l1=l.copy()
    l1.sort(reverse=True)
    #print(l1)
    s=''
    for i in range(0,len(l)):
        s+=str(l.index(l1[i])+1)
    #print(s)
    if s=='111111':
        s='123456'
    return (s,str(round(l1[0], 2)))

#print(xuanze('Bob'))
# #设置起始日期和结束日期，结束日期可以更改，初始日期要改的话表里面对应的初始日期也要改。
# t0=datetime_f_str2('2019-01-01 00:00:00')
# t1=datetime_f_str2('2019-12-31 00:00:00')
#
# current_product_index=0
# current_product_period=product_period_list[current_product_index]
# current_product_ratio=profit_ratio[current_product_index]
#
#
# total_asset=0 # 总的资产
# total_cun=0 # 总的存储金额
# for transaction in data:
#     if iskong(transaction):
#         #无交易
#         continue
#     if transaction.find('c:')!=-1:
#         rmb=int(re.findall('c:(\d+)',transaction)[0])
#         print(f'存{rmb}')
#         total_cun+=rmb
#         total_asset+=rmb
#
#
# get_timedelta_seconds(t1-t0)/3600/24
#
