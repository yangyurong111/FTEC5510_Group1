from mytool import *
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
        encode=chardet.detect(open(file, 'rb').readline())['encoding']
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

def fetch_data(path,name='',date=''):
    data = csv_to_arr(path)
    if name!='' and date!='':
        for j in range(len(data[0])):
            if data[0][j] == date:
                for i in range(len(data)):
                    if data[i][0] == name:
                        return data[i][j]
    if name != '':
        for i in range (len(data)):
            if data[i][0]==name:
                return data[i]
    if date!='':
        for j in range(len(data[0])):
            if data[0][j] == date:
                l=[]
                for i in range (1,len(data)):
                    try:
                        l.append(data[i][j])
                    except:
                        pass
                return l
        # for i in range (len(data)):
        #     if data[i][0]==name:
        #         return data[i]
# data=fetch_data(name='Bob',date='20190101')
# print(data)
# data=fetch_data(name='Bob')
# print(data)
# data=fetch_data(date='20190101')
# print(data)
def total_deposit(username):
    data=fetch_data("5510_user_data_deposit.csv",name=username)
    for i in range(len(data)-1,-1,-1):
        if data[i] != '':
            temp=data[i].split('+')[-1].split('@')[-1].split(':')[-1]
            return temp

def total_invest(username):
    data=fetch_data("5510_user_data_invest.csv",name=username)
    for i in range(len(data)-1,-1,-1):
        if data[i] != '':
            temp=data[i].split('+')[-1].split('@')[-1].split(':')[-1]
            return temp
def deposit(username,amount):
    data = csv_to_arr("5510_user_data_deposit.csv")
    date=xianzai_shijian(string=True)[:10].replace('-','')
    for j in range(len(data[0])):
        if data[0][j] == date:
            for i in range(len(data)):
                if data[i][0] == username:
                    total=str(int(total_deposit(username))+int(amount))
                    data[i][j]=data[i][j]+'+'+'c:%s@q:0@d:%s'%(amount,total)
                    arr_to_csv(data,"5510_user_data_deposit.csv")
                    return "Deposit Successfully!"
    return "Fail to Deposit!"

def withdraw(username,amount):
    data = csv_to_arr("5510_user_data_deposit.csv")
    date=xianzai_shijian(string=True)[:10].replace('-','')
    for j in range(len(data[0])):
        if data[0][j] == date:
            for i in range(len(data)):
                if data[i][0] == username:
                    total=str(int(total_deposit(username))-int(amount))
                    if int(total)<0:
                        return "Fail to Withdraw, Money Is Not Enough!"
                    data[i][j]=data[i][j]+'+'+'c:0@q:%s@d:%s'%(amount,total)
                    #print(data[i][j])
                    arr_to_csv(data,"5510_user_data_deposit.csv")
                    return "Withdraw Successfully!"
    return "Fail to Withdraw!"

def transfer(username1,username2,amount):
    temp=withdraw(username1, amount)
    if temp=="Withdraw Successfully!":
        deposit(username2, amount)
        return "Transfer Successfully!"
    else:
        return "Fail to Transfer!"



# print(total_deposit('Alice'))
# print(total_invest('sandy'))
# print(withdraw('Alice','50000000'))
#print(transfer('Alice','Bob','5000'))
'''下面你就要自己写了,data传入的就是用户的数据，然后return一个收益率，
如果根本不适用这种理财产品比如中途存款小于0，那直接return 0 就行了'''
def licai_chanpin1(data):
    pass
def licai_chanpin2(data):
    pass

def deposit_detail(username,date_start,date_end):
    temp=fetch_data('5510_user_data_deposit.csv', name='Date')
    temp2 = fetch_data('5510_user_data_deposit.csv', name=username)
    l=[]
    date_start=datetime.datetime.strptime(date_start, '%Y%m%d')
    date_end = datetime.datetime.strptime(date_end, '%Y%m%d')
    for i in range(2,len(temp2)):
        date = datetime.datetime.strptime(temp[i], '%Y%m%d')
        if date>=date_start and date<=date_end:
            if temp2[i]=='':
                pass
            else:
                temp3=temp2[i].split('+')
                for j in temp3:
                    if j=='':
                        pass
                    else:
                        j_list=j.split('@')
                        cun=j_list[0].split(':')[1]
                        qu = j_list[1].split(':')[1]
                        if qu=='0':
                            l.append(temp[i]+'@'+cun)
                        if cun=='0':
                            l.append(temp[i]+'@-'+qu)


    s=r'<div class="mui-col-xs-3 mui-text-center">Name</div><div class="mui-col-xs-3 mui-text-center">Rate</div><div class="mui-col-xs-3 mui-text-center">Amount</div><div class="mui-col-xs-3 mui-text-center">Trading Date</div>'
    for j in range(len(l)-1,-1,-1):
        i=l[j]
        s=s+r'<div class="mui-col-xs-3 mui-text-center">%s</div>'%"Deposit"
        s = s + r'<div class="mui-col-xs-3 mui-text-center">%s</div>' % "0%"
        amount=i.split('@')[1]
        if amount[0]!='-':
            amount='+'+amount
        s = s+ r'<div class="mui-col-xs-3 mui-text-center">%s</div>' % amount
        s = s + r'<div class="mui-col-xs-3 mui-text-center">%s</div>' % i.split('@')[0]
    return s
def invest_detail(username,date_start,date_end):
    temp=fetch_data('5510_user_data_invest.csv', name='Date')
    temp2 = fetch_data('5510_user_data_invest.csv', name=username)
    l=[]
    date_start=datetime.datetime.strptime(date_start, '%Y%m%d')
    date_end = datetime.datetime.strptime(date_end, '%Y%m%d')
    for i in range(2,len(temp2)):
        date = datetime.datetime.strptime(temp[i], '%Y%m%d')
        if date>=date_start and date<=date_end:
            if temp2[i]=='':
                pass
            else:
                temp3=temp2[i].split('+')
                for j in temp3:
                    if j=='':
                        pass
                    else:
                        j_list=j.split('@')
                        cun=j_list[0].split(':')[1]
                        qu = j_list[1].split(':')[1]
                        name_index = int(j_list[2].split(':')[1])-1
                        r=readfile('5510_invest_name.txt')
                        name=""
                        name1=r.split('\n')[name_index].split('@')[0]
                        name_l=name1.split(' ')
                        if len(name_l)>2:
                            for i in range(0,len(name_l)-1):
                                name=name+name_l[i][0]
                            name=name+' '+name_l[-1]
                        else:
                            name=name1
                        rate=r.split('\n')[name_index].split('@')[1]
                        if qu=='0':
                            l.append(temp[i]+'@'+cun+'@'+name+'@'+rate)
                        if cun=='0':
                            l.append(temp[i]+'@-'+qu+'@'+name+'@'+rate)
    s=r'<div class="mui-col-xs-3 mui-text-center">Name</div><div class="mui-col-xs-3 mui-text-center">Rate</div><div class="mui-col-xs-3 mui-text-center">Amount</div><div class="mui-col-xs-3 mui-text-center">Trading Date</div>'
    for j in range(len(l)-1,-1,-1):
        i=l[j]
        #print(i)
        s=s+r'<div class="mui-col-xs-3 mui-text-center">%s</div>'%i.split('@')[2]
        s = s + r'<div class="mui-col-xs-3 mui-text-center">%s</div>' % i.split('@')[3]
        amount=i.split('@')[1]
        if amount[0]!='-':
            amount='+'+amount
        s = s+ r'<div class="mui-col-xs-3 mui-text-center">%s</div>' % amount
        s = s + r'<div class="mui-col-xs-3 mui-text-center">%s</div>' % i.split('@')[0]
    return s
# s=invest_detail('Alice','20190101','20201116')
# print(s)
# #l=invest_detail('Alice','20190101','20210303')
# print(s)
#print('2020-19-36-588'.replace('-','')[:8])

# def invest_page():
#     result=""
#     count=0
#     rate='214536'
#     biaoyu='Return No.1, simulated profit can reach to 1000 HKD per year!'
#     s=readfile('5510_invest_name.txt')
#     l=s.split('\n')
#     for i in rate:
#         count=count+1
#         l2=l[int(i)-1].split('@')
#         if count==1:
#             result=result+'%s<em>%s Bank</em><em>%s</em>'%(l2[0],l2[0].split(' T')[0],biaoyu)
#         else:
#             result = result + '%s<em>%s Bank</em>' % (l2[0], l2[0].split(' T')[0])
#         result+='@'
#         result+=r'<font color="red">%s<em>'%l2[1].replace('%','')+'%'+'</em> </font>'
#         result+='@'
#         result += l2[2]
#         result+='@'
#         result += l2[3]+r' <em>days</em>'
#         result+='@'
#         result+=r'>%s | low/medium risk'%l2[4]
#         result=result+'#'
#     return result
#print(invest_page())
def invest(username,amount,code):
    w=withdraw(username, amount)
    if w=="Withdraw Successfully!":
        pass
    else:
        return "Fail to Invest, Money Is Not Enough!"
    r=readfile("5510_invest_name.txt")
    l=r.split('\n')
    for i in range(0,len(l)):
        if code==l[i].split('@')[2]:
            leixing=str(i+1)
            jine=l[i].split('@')[4]
            break
    if int(amount)<int(jine):
        return "This product needs at least %s HKD to invest, the amount you input is not enough!"%jine
    data = csv_to_arr("5510_user_data_invest.csv")
    date=xianzai_shijian(string=True)[:10].replace('-','')
    for j in range(len(data[0])):
        if data[0][j] == date:
            for i in range(len(data)):
                if data[i][0] == username:
                    total=str(int(total_invest(username))+int(amount))
                    data[i][j]=data[i][j]+'+'+'c:%s@q:0@l:%s@d:%s'%(amount,leixing,total)
                    arr_to_csv(data,"5510_user_data_invest.csv")
                    return "Invest Successfully!"
    return "Fail to Invest!"

#print(invest('Bob','100','01004'))