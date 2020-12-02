# encoding:UTF-8
import re,builtins, os, html, requests, pickle,send2trash,chardet,sys,subprocess,threading,random,base64,shutil,ntplib
import ctypes, sys,traceback
import pytz,qrcode#pytz大概能多占4m空间吧，但是在qt生成的时候没区别，要是想极限压缩再说吧...leancloud一样的，比pytz多个2m吧？
#两种import etree的方法，3.6是第一种，3.3是第二种
from lxml import etree
from io import BytesIO
#from lxml import html
#etree=html.etree

from os.path import *
from datetime import timedelta
from datetime import datetime
import time,json
from random import randint




temppath='/tmp'
default_pickle_path=r'/tmp/python_pickles'
exe_file=sys.executable#非常可靠，测试过通过popen，通过cmd，都是显示exe的真正路径
exe_dir=dirname(exe_file)





def send_to_trash(file_path):
    send2trash.send2trash(file_path)



def cleanStr(s):
    # 2333\n\r90\r\n0\t709——>2333900709
    try:return "".join(s.split())
    except:
        return ''

def is_chong(element, list):
    try:
        list.index(element)
        return True
    except Exception as e:
        return False

#出错返回None，若函数未出错情况下返回None，就抛出异常。
'''
return_when_error代表默认出错返回什么，默认是None
ignore_conflict=True表示函数未出错情况下返回值和错误返回值相同 并不抛出异常。
'''
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


def nodeToStr(node):
    return html.unescape(etree.tostring(node, encoding='unicode'))

def postParamStrToDict(paramStr):
    dict = {}
    for str in paramStr.split('&'):
        try:
            a = re.findall('([\s\S]+?)=([\s\S]*)', str)
            key = a[0][0]
            value = a[0][1]
            dict[key] = value
        except Exception as e:
            print(e)
    return dict
'''
输入：{'jk':'jkll','jkl':9080}
输入的map中的值可以是int
输出：'jkl=9080&jk=jkll'
'''
def dictToPostParamStr(map):
    content = '&'.join(['='.join([str(key),str(value)]) for key,value in map.items()])
    return content

# 返回：dict；  空格会自动全部处理掉；
def cookieStrToDict(cookieStr):
    # Cookie: __dxca=14d46b97-bef5-44de-a34a-4b6c6f4f708d; msign=1480949245796%2d3; JSESSIONID=0F1D06B5993B9FA33454952A1E317D38.tomcat133; route=5958c386bf5e9109ac10d2a628645aea; CNZZDATA2088844=cnzz_eid%3D133551680-1480946725-http%253A%252F%252Fbook.zhizhen.com%252F%26ntime%3D1480946725
    # cookieStr='__dxca=14d46b97-bef5-44de-a34a-4b6c6f4f708d; msign=1480949245796%2d3; JSESSIONID=0F1D06B5993B9FA33454952A1E317D38.tomcat133; route=5958c386bf5e9109ac10d2a628645aea; CNZZDATA2088844=cnzz_eid%3D133551680-1480946725-http%253A%252F%252Fbook.zhizhen.com%252F%26ntime%3D1480946725'
    cookieStr = cookieStr.replace(' ', '')
    strList = cookieStr.split(';')
    dict1 = {}
    for s in strList:
        if iskong(s):
            continue
        l = re.findall(r'(.+?)=(.*)$', s)
        key = l[0][0]
        value = l[0][1]
        dict1[key] = value
    return dict1

'''
如返回：
{'BAIDUID': '74A1CC15BB1A38CDAA7E4CCD356C0B25:FG=1', 'BDRCVFR[x4e6higC8W6]': 'mk3SLVN4HKm', 'BIDUPSID': '74A1CC15BB1A38CDAA7E4CCD356C0B25', 'H_PS_PSSID': '1459_21102_20719', 'PSINO': '7', 'PSTM': '1540582238', 'delPer': '0', 'BDSVRTM': '9', 'BD_CK_SAM': '1'}
type选择str可以变成string
string的话返回：
BAIDUID=1C8FF400C07B790054C937EC3B6A247B:FG=1;BDRCVFR[x4e6higC8W6]=mk3SLVN4HKm;BIDUPSID=1C8FF400C07B790054C937EC3B6A247B;H_PS_PSSID=1428_21100_27401;PSINO=7;PSTM=1540582501;delPer=0;BDSVRTM=9;BD_CK_SAM=1;
'''
#从session中取出所有的cookie并组合成dict
def extract_cookie_f_session(s,type='dict'):
    if type=='dict':
        arr_table=s.cookies.items()
        d=arr_table_to_map(arr_table)
        return d
    elif type=='str':
        arr_table = s.cookies.items()
        string=''
        for key,value in arr_table:
            line=key+'='+value+';'
            string+=line
        return string
    raise Exception('参数错误！')

'''
status_obj是一个对象，用来存储不断变化的属性
length_mb:总大小，mb为单位
speed：速度，kb为单位
percent：百分比，例如：75
need_time：分钟为单位
'''
def download(url, filePath,show_state=True,status_obj=None):
    # https://video-subtitle.tedcdn.com/talk/podcast/2015Z/None/JasondeCairesTaylor_2015Z-480p-en.mp4
    #默认覆盖！

    if status_obj is not None:
        status_obj.speed = 0
        status_obj.percent = 1
        status_obj.need_time = 0
    #首先可能要新建文件夹
    mkdir(dirname(filePath))

    res = requests.get(url, stream=True)
    res.raise_for_status()
    contentLength = int(res.headers.get('Content-Length'))
    if show_state:print('总大小：' + str(round(contentLength / 1024 / 1024, 2)) + " mb")
    if status_obj is not None:
        status_obj.length_mb=round(contentLength / 1024 / 1024, 2)

    spots = [time.time()]
    display = 0

    playFile = open(filePath+'.tmp', 'wb')
    a = time.time()
    for chunk in res.iter_content(102400):
        display = display + 1
        playFile.write(chunk)
        spots.append(time.time())
        if len(spots) > 10 and display == 10:
            v = round(500 / (spots[len(spots) - 1] - spots[len(spots) - 6]), 2)
            percent = round(len(spots) * 102400 / contentLength * 100, 2)
            yuji = round((spots[len(spots) - 1] - spots[0]) / percent * 100 / 60 * (1 - percent / 100), 2)
            if show_state:print('速度：' + str(v) + ' kb/s  百分比：' + str(percent) + "%  预计剩余：" + str(yuji) + '分钟')
            if status_obj is not None:
                status_obj.speed=v
                status_obj.percent=percent
                status_obj.need_time= yuji
            display = 0
    playFile.close()
    try:
        os.rename(filePath+'.tmp',filePath)
    except FileExistsError as e:
        send_to_trash(to_qt_path(filePath).replace('/','\\'))#send_to_trash方法只能识别 \ 这种破折号的路径
        if exists(filePath):#那个删不掉就只能用这个了。
            os.remove(filePath)
        os.rename(filePath + '.tmp', filePath)

    if show_state:print('下载完成！')
    if status_obj is not None:
        status_obj.speed = 0
        status_obj.percent = 100
        status_obj.need_time = 0

#用来做pool调节线程个数用。
class MyPool():
    maxThreadAM=1
    __threadAlive__=[]
    __threadWaiting__=[]

    def __init__(self,maxThreadAM=1):
        self.maxThreadAM=maxThreadAM

    def addThread(self,newThread):
        self.__threadWaiting__.append(newThread)

    def __checkAlive__(self):
        for thread in self.__threadAlive__:
            if thread.is_alive()==False:
                self.__threadAlive__.remove(thread)
                newThread=self.__threadWaiting__.pop(0)
                newThread.start()
                self.__threadAlive__.append(newThread)
                break #害怕index出错。

    def start(self):
        for thread in self.__threadWaiting__[0:self.maxThreadAM]:
            thread.start()
        for thread in self.__threadWaiting__[0:self.maxThreadAM]:
            self.__threadWaiting__.remove(thread)
            self.__threadAlive__.append(thread)
        while len(self.__threadWaiting__)>0:
            self.__checkAlive__()

def mergeVedios(source_files, target_file):
    i = 1
    for f in source_files:
        dir = os.path.dirname(f)
        command = r'ffmpeg -i "%s" -y -c copy -f mpegts %d.ts' % (f, i)
        os.system(command)
        i += 1
    string = ''
    for ii in range(1, i):
        string += '%d.ts|' % ii
    string = string[0:-1]
    command = r'ffmpeg -i "concat:%s" -y -c copy -movflags +faststart "%s"' % (string, target_file)
    os.system(command)

    for ii in range(1, i):
        try:
            os.remove('%d.ts'%ii)
        except Exception as e:
            print(str(e))

def iskong(o):
    o=try_once(lambda:o,ignore_conflict=True)#如果传入的这个参数根本没有定义，就在这里返回None,也是一种“空” #这个好像没用，用try_once判断参数定义没有吧。
    if o is None: return True
    if o!=o:return True#np.nan会出现这种情况
    #int类型返回非空
    if str(type(o)).find('int') != -1:return False#int是不能用len()方法的
    if str(type(o)).find('long') != -1: return False
    if str(type(o)).find('float')!=-1: return False #可能出现numpy.float64 这种鬼。
    if len(o)==0:return True
    #if o=='':return True
    return False

#对arr进行去空,后面一个参数表示是否把\n\r之类的也算作空
def qukong(arr,is_space_chars_kong=False):
    new_arr=[]
    if is_space_chars_kong:
        for a in arr:
            if iskong(a.strip()) == False:
                new_arr.append(a)
        return new_arr

    for a in arr:
        if iskong(a)==False:
            new_arr.append(a)
    return new_arr

#用utf8和gbk和chardet读取文件
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

def get_with_encode(url,default='utf8'):
    bytes=requests.get(url).content
    if default.find('utf')!=-1:
        try:
            return str(bytes, 'utf8')
        except:
            pass
        try:
            return str(bytes,'gbk')
        except:
            pass
    else:
        try:
            return str(bytes,'gbk')
        except:
            pass
        try:
            return str(bytes, 'utf8')
        except:
            pass
    try:
        encode=chardet.detect(bytes)['encoding']
        return str(bytes,encode)
    except:pass
    return str(bytes,default,'ignore')


#按照某种编码写入文件（自动创建文件夹）
def writefile(string,file,encoding='utf-8'):
    if exists(file)==False:
        mkdir(dirname(file))
    open(file,'wb').write(string.encode(encoding=encoding))

#该方法已弃用！！！由于系统默认是gbk，所以我们把string以gbk方式写入文件，这样excel之类的才不会乱码
def writefile_gbk(string,file):
    open(file, 'w').write(str(string.encode('gbk', 'ignore'), encoding='gbk'))

def readfile_b(file):
    return open(file, 'rb').read()
def writefile_b(file,bytes):
    open(file, 'wb').write(bytes)


#是否包含中文
def contain_zhong(string):
    if iskong(re.findall(r'[\u4E00-\u9FA5]',string)):
        return False
    return True

#arr必须是二维的。此方法将arr变为csv存储下来。
def arr_table_to_csv(arr_table,csvfile,delimiter=',',line_spliter='\n'):
    string=''
    for arr in arr_table:
        line=''
        for a in arr:
            line+=str(a)+delimiter
        line=line[0:-1]
        string+=line+line_spliter
    string=string[0:-1]
    writefile(string,csvfile)
#将csv读入为arr_table  行以换行符为界，列以逗号为界
def csv_to_arr_table(csvfile,delimiter=','):
    arr=[]
    text=readfile(csvfile)
    return csvStr_to_arr_table(csv_str=text,delimiter=delimiter)

'''
如果csv_str是空，那么返回None
'''
#将csv_str读入为arr_table  行以换行符为界，列以逗号为界
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
#将csv读入为map<string,string> 或者map<string,list> 行以换行符为界，列以逗号为界
def csv_to_map(csvfile,delimiter=','):
    map={}
    text=readfile(csvfile)
    text=text.replace('\r\n','\n')
    for line in text.split('\n'):
        arr2=line.split(delimiter)
        if len(arr2)==1:
            map[arr2[0]] = ''
        elif len(arr2)==2:
            map[arr2[0]]=arr2[1]
        else:
            map[arr2[0]] = arr2[1:]

    return map
#向csv输入一行数据
#这个方法有个问题就是输完了之后，最后一行有个\n，这样的话，用csv_to_arr的时候，最后就有个空的arr。暂时没有解决这个问题。
def csv_add_arr(csvfile,arr,delimiter=','):
    # 写入
    string = ''
    for a in arr:
        string += str(a) + delimiter
    string = string[0:-1] + '\n'
    open(csvfile, 'a').write(string)

#是否是数字或者小数
def is_digit_decimal(string):
    try:
        float(string)
        return True
    except Exception as e:
        return False

#尝试makedir,可以多级目录
def mkdir(target_dir):
    try_once(lambda: os.makedirs(target_dir), False,-1)

#四舍五入
def round2(f,i=0):
    a=round((f + 0.00000001), i)
    return a

class mytime:
    '''
    使用方法：
    d=mytime('2014-09-1')
    print(d.plus(2).time1)
    '''
    def __init__(self,obj):#obj可以是%Y-%m-%d字符串，也可以是datetime
        if isinstance(obj,str):
            try:
                self.datetime1=datetime.strptime(obj,'%Y-%m-%d')
                self.time1 = datetime.strftime(self.datetime1, '%Y-%m-%d')
            except Exception as e:
                print('时间string输入错误，无法转换为datetime格式')
        elif isinstance(obj,datetime):
            self.datetime1 = obj
            self.time1 = datetime.strftime(self.datetime1, '%Y-%m-%d')
        else:
            raise ('时间输入既不是string又不是datetime，出错！')

    def plus(self,i):#返回一个新的mytime，原来的mytime不变
        tmp=mytime(self.datetime1+timedelta(i))
        return tmp

    def minus(self, obj):
        #如果obj是天数  返回一个新的mytime，原来的mytime不变
        #如果obj是另一个mytime，返回天数
        if isinstance(obj, int):
            tmp=mytime(self.datetime1-timedelta(obj))
        if isinstance(obj, mytime):
            tmp = (self.datetime1 - obj.datetime1).days

        return tmp



'''
zip，rar都可以
zip_rar_file可以是完整该路径，也可以是一个文件名，如果是文件名，就默认创建到arr file中第一个文件的所在目录
使用的是1st文件，这样可以添加文件夹。
使用：addxxx(文件夹，123.rar)；(文件夹，c:/123.rar);([文件1,文件2,文件3]，123.rar)；（文件，123.rar）
password是压缩密码。压缩密码的方式是文件名都不可见的加密方式。
'''
#添加到压缩文件
def add_to_zip_rar(arr_file, zip_rar_file, password='',rar_exe_path='rar'):
    #如果是rar.exe 的绝对路径，就需要先cd到rar.exe 的目录，再运行 Rar.exe balabala.  "c:\xxx\Rar.exe" balabala 是不行的。
    if rar_exe_path!='rar':
        rar_exe_path='cd "%s" & %s'%(dirname(rar_exe_path),basename(rar_exe_path))
    if password == '':
        ps_str = ''
    else:
        ps_str = '-hp'+str(password)
    # use 1st file to zip
    file_1st = join(temppath, str(int(time.time())) + '.1st')
		#判断传入的参数1是一个文件夹（or文件），还是一个列表
    if isinstance(arr_file,str):
    		#判断参数2是绝对路径还是相对路径。如果是相对路径，取参数1所在目录补成绝对路径。
        if dirname(zip_rar_file) == '':
            # zip_rar_file是一个文件名，不是一个完整的路径，那么就默认创建到arr file中第一个文件的所在目录
            zip_rar_file = join(dirname(arr_file), zip_rar_file)
        string='"%s"'%arr_file
        writefile_gbk(string, file_1st)
            # -ep1 -r 表示保存路径的层级到压缩文件中。
        cmd_string = r'%s a %s -idq -ep1 -r "%s" @"%s"' % (rar_exe_path,ps_str,zip_rar_file, file_1st)
    else:
        if dirname(zip_rar_file)=='':
            #zip_rar_file是一个文件名，不是一个完整的路径，那么就默认创建到arr file中第一个文件的所在目录
            zip_rar_file=join(dirname(arr_file[0]),zip_rar_file)

        string=''
        for file in arr_file:
            string+='"%s" \r\n'%file
        #-ep是用来排除添加路径的。比如把c:/user/desktop/123.txt添加到压缩文件，如果没有-ep，它就在压缩文件中建立层级目录user/desktop/123.txt，非常傻逼。
        #如：rar a -ep "C:\Users\Finder\Desktop\zimu\hehe.rar"  "C:\Users\Finder\Desktop\zimu\1.txt"  "C:\Users\Finder\Desktop\zimu\2.txt"
        writefile_gbk(string,file_1st)
        cmd_string=r'%s a %s -idq -ep1 -r "%s" @"%s"'%(rar_exe_path,ps_str,zip_rar_file,file_1st)

    print(cmd_string)
    os.system(cmd_string)


r'''
例如：
rar_file=r'C:\Users\Administrator\Desktop\SmsLog\1.rar'
t=extract_from_zip_rar(rar_file,dirname(rar_file))
返回：[True]或者[False,msg]
一般出错都是有程序在使用中，无法覆盖。
'''
#解压缩
def extract_from_zip_rar(zip_rar_file,target_dir,overwrite=True,rar_exe_path='rar'):
    tmp_overwrite='-o+' if overwrite else '-o-'
    cmd_string='"%s" x -idq %s "%s" "%s"'%(rar_exe_path,tmp_overwrite,zip_rar_file,target_dir)
    err,out=cmd2(cmd_string)
    if err is not None:
        raise Exception('解压出错：\n'+err)


#数组转list
def tuple2arr(tu):
    arr=[]
    for t in tu:
        arr.append(t)
    return arr

#按照index删除元素
def delete_item(li, index):
    li = li[:index] + li[index+1:]
    return li

#pickle读入写入，p_path可以是一个完整的路径也可以是一个文件名，如：DataFrame_01.txt
#如果是文件名，自动用  default_pickle_path 来补全，另外后缀名最好就是txt吧。
#本来protocol=3是默认的，就是说导出的pickle文件给python3用，如果要给python2用，就请设置为2。所以我默认是2了。
def write_pickle(obj,p_path,protocol=2):
    dir1=dirname(p_path)
    if dir1=="":
        #说明传入的只是一个文件名
        dir1=default_pickle_path
        f=p_path
    else:
        dir1=dirname(p_path)
        f=basename(p_path)
    mkdir(dir1)
    pickle.dump(obj,open(join(dir1,f),'wb'),protocol=protocol)
#    open(join(dir1,f),'wb').write(pickle.dumps(obj,protocol=2))

def is_runnning_py2():
    if(sys.version[0:1]=='3'):
        return False
    else:
        return True

#encoding默认是空，也就是不加encoding。如果手动设置了encoding，将会将encoding添加到参数中，而只有python3可以添加encoding。
#在测试中，pycharm中的python2.7生成的pickle用utf-8编码即可。
def read_pickle(p_path,encoding=""):
    dir1=dirname(p_path)
    if dir1=="":
        #说明传入的只是一个文件名
        dir1=default_pickle_path
        f=p_path
    else:
        dir1=dirname(p_path)
        f=basename(p_path)

    if is_runnning_py2():
        #python2无法设置encoding，直接运行
        obj = pickle.load(open(join(dir1,f),'rb'))
    else:
        if iskong(encoding)==False:
            #强制指定了encoding
            obj = pickle.load(open(join(dir1,f),'rb'), encoding=encoding)
        else:
            obj=try_once(lambda :pickle.load(open(join(dir1,f),'rb'), encoding='utf-8'),False)
            if obj is not None:
                return obj
            obj = try_once(lambda: pickle.load(open(join(dir1,f),'rb'), encoding='iso-8859-1'),False)
            if obj is not None:
                return obj
            obj = try_once(lambda: pickle.load(open(join(dir1,f),'rb'), encoding='gbk'),False)
            if obj is not None:
                return obj
    return obj


#获取不带后缀的文件名，绝对路径或者相对路径都可以
def get_name_without_houzhui(f):
    return os.path.splitext(os.path.basename(f))[0]
#获取后缀名，绝对路径或者相对路径都可以,带点号
def get_houzhui(f):
    return os.path.splitext(f)[1]

'''
获取cmd运行出来的全部输出，包括运行错误的时候的错误信息。如果用os.popen 不能截取到错误输出
encoding表示用什么编码读取cmd命令行的输出，默认encoding是gbk,可以选择"auto_detect"，就是用chardet自动检测
没有输出返回None，有输出返回“out\nerr”。
阻塞方法
'''
def cmd(cmd_string,encoding='gbk',ignore=True):

    ignore_str='ignore'if ignore else 'strict'
    proc = subprocess.Popen(cmd_string, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=True)
    out, err = proc.communicate()
    if out is None:out=b''
    if err is None:err=b''
    if out==b'' and err==b'':
        return None
    if encoding=='auto_detect':
        if len(err)>len(out):
            encoding=chardet.detect(err)['encoding']
        else:
            encoding=chardet.detect(out)['encoding']
        if iskong(encoding):
            encoding='gbk'
    string=str(out,encoding,ignore_str)+'\n'+str(err,encoding,ignore_str)
    string=string.replace('\r\r','\r')#'\r\r\n导致打印不出来，不知道是什么bug...可能是pycharm的bug'
    return string

'''
cmd方法以后要淘汰了，这个方法的不同在于将out和err分开返回了。
获取cmd运行出来的全部输出，包括运行错误的时候的错误信息。如果用os.popen 不能截取到错误输出
encoding表示用什么编码读取cmd命令行的输出，默认encoding是gbk,可以选择"auto_detect"，就是用chardet自动检测
没有输出返回None，有输出返回“out\nerr”。

阻塞方法。 os.popen是非阻塞方法，但是用这个方法运行的exe内部代码需要是绝对路径。具体看笔记。

'''
def cmd2(cmd_string,encoding='gbk',ignore=True):

    ignore_str='ignore'if ignore else 'strict'
    proc = subprocess.Popen(cmd_string, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=True)
    out, err = proc.communicate()

    if encoding=='auto_detect':
        if len(err)>len(out):
            encoding=chardet.detect(err)['encoding']
        else:
            encoding=chardet.detect(out)['encoding']
        if iskong(encoding):
            encoding='gbk'

    if out==b'':
        out_msg=None
        err_msg=str(err,encoding,ignore_str)
    if err==b'':
        err_msg=None
        out_msg=str(out, encoding, ignore_str)
    return [err_msg,out_msg]

#下面四个方法中，前面两个是之前的，后面两个是之后的，有点重复，看喜欢哪个用哪个吧
#查找正则表达式所有匹配的开始和结束的位置
def search_all(reg_str,string,return_type='span'):
    #return_type='span' 返回很多个[1,2] 前面是一个匹配的start，后面是end
    #return_type='start'返回[2,5,7,23] 所有匹配的start
    # return_type='end'返回[2,5,7,23] 所有匹配的end
    arr=[]
    cut_index=0
    while True:
        m=re.search(reg_str,string)
        if iskong(m)==True:
            break
        start=m.span()[0]
        end=m.span()[1]
        arr.append([start+cut_index,end+cut_index])
        string=string[end:]
        cut_index+=end
    if return_type=='span':
        return arr
    if return_type=='start':
        arrtmp=[]
        for a in arr:
            arrtmp.append(a[0])
        return arrtmp
    if return_type == 'end':
        arrtmp = []
        for a in arr:
            arrtmp.append(a[1])
        return arrtmp

#通过正则表达式切割，切割时保留正则表达式部分本身，从正则的头部切割，不丢任何数据
def cut_by_reg(reg_str,string):
    #在正则表达式的头部切割
    arr=[0]
    search_res=search_all(reg_str,string,return_type='start')
    arr.extend(search_res)
    arr.append(len(string))

    sections=[]
    for i in range(0,len(arr)-1):
        str_tmp=string[arr[i]:arr[i+1]]
        if iskong(str_tmp):
            continue
        sections.append(str_tmp)
    return sections

#找正则表达式的起始位置
#find_regex_index(r'\d','uier3uio5')——[4, 8]
def find_regex_index(regex_str,content):
    a = [m.start() for m in re.finditer(regex_str,content)]
    return a

'''
  和subn 不一样的地方在于，可以通过关键词 '###finded_str_by_regex###' 来将搜索到的str放到
new_str里面去。
  例如：
  replace_by_reg('\d+','[digit:###finded_str_by_regex###]','uoi34ioiou333')
  Out[10]: 'uoi[digit:34]ioiou[digit:333]'
  同样是替换所有的。不是替换第一个哈。
  不用加括号，加了也没意义。例如：
  replace_by_reg('3(\d+)','[digit:###finded_str_by_regex###]','uoi34ioiou333')
    Out[4]: 'uoi[digit:34]ioiou[digit:333]'
'''
#根据正则来进行替换
def replace_by_reg(regex_str,new_str,content):
    pattern=re.compile(regex_str)
    match = pattern.search(content)
    while match is not None:
        new_str2=new_str.replace('###finded_str_by_regex###',content[match.start():match.end()])
        content=content[0:match.start()]+new_str2+content[match.end():len(content)]
        match = pattern.search(content,match.start()+len(new_str2))
    return content

'''
不用加括号，加了也没意义。
replace_by_reg2('\d+',lambda x: '[digit:%s]'%x,'uoi34ioiou333')
uoi[digit:34]ioiou[digit:333]
有个bug，就是有些时候，re.compile('.*logging.*')这样的话，有可能在debug里会看到pattern是：re.compile('\ufeff.*logging.*')就tm的很神奇了。
这种就检测不到。关键还是自动加的。。。草。后来我发现，只要连着把引号都去掉，重新手打，不要复制，就没问题。真tm绝了。
'''
#根据正则来进行替换,更高档了
def replace_by_reg2(regex_str,new_str_or_func,content):
    pattern=re.compile(regex_str)
    match = pattern.search(content)
    while match is not None:
        old_str=content[match.start():match.end()]
        if isinstance(new_str_or_func,str):
            new_str2=new_str_or_func
        elif hasattr(new_str_or_func,'__call__'):#判断new_str_or_func是否是函数。不能用isinstance判断。
            new_str2=new_str_or_func(old_str)
            if isinstance(new_str2,str)==False:
                raise Exception('new_str_or_func是函数的时候返回值应该是string！')
        else:
            raise Exception('传入的参数类型错误！要么是str要么是function！')
        content=content[0:match.start()]+new_str2+content[match.end():len(content)]
        match = pattern.search(content,match.start()+len(new_str2))
    return content

#通过一串数字index来切割字符串，返回切割好的字符串list
#如：cut_text_by_index([1,2,3],'uierue')
#返回：['u', 'i', 'e', 'rue']
#参数index_list可以是数组。index_list的第一个可以是0，也可以不是。最后一个可以是len(text)也可以不是。反正我们会检测的。
def cut_text_by_index(index_list,text):
    index_list=list(index_list)#如果是数组格式，转化成list
    #先标准化，第一个是0，最后一个是总长度。
    if(index_list[0]!=0):
        index_list.insert(0,0)
    if (index_list[len(index_list)-1] != len(text)):
        index_list.append(len(text))

    str_list=[]
    for i in range(1,len(index_list)):
        str_list.append(text[index_list[i-1]:index_list[i]])
    return str_list

'''
返回：1519811151117_32702  前面一段表示格林时间微秒，后面是1-10万random
'''
def get_random_name():
    t=int(time.time()*1000)#微秒
    t2=random.randint(1,100000)
    name=str(t)+'_'+str(t2)
    return name

#返回线程id （字符串形式）
def get_cur_thread_id():
    return str(threading.current_thread().ident)

'''
不知道上面那个方法有什么用，反正在qt界面用这个打印最好。
'''
#打印thread的名字
def print_cur_thread_name():
    print(threading.currentThread().name)

#对list去重。
'''
# list的元素可以是数组。
'''
def drop_list_duplicates(arr):
    new_li=[]
    for i in arr:
        if i not in new_li:
            new_li.append(i)
    return(new_li)

#对map去空，判断标准：iskong(key)
def drop_map_void_items(map):
    new_m={}
    for key,value in map.items():
        if iskong(key)==False:
            new_m[key]=value
    return new_m


# 获取不重复的带index的文件名
'''
例如：dir文件夹中已经存在123.txt文件，就返回123_2.txt。如果没有，直接返回123.txt
之后返回123_3.txt   123_4.txt以此类推。
'''
def get_name_with_index(dir,filename):
    if os.path.exists(join(dir, filename)) == False:
        return filename
    name1 = splitext(basename(filename))[0]
    houzhui = splitext(basename(filename))[1]
    for i in range(2, 10000000):
        filename2 = '%s_%s%s' % (name1, i, houzhui)
        if os.path.exists(join(dir, filename2)) == False:
            return filename2

# 获取不重复的带index的文件名2
'''
返回123_01.txt   123_02.txt以此类推。
zfill 控制填充的位数
'''
def get_name_with_index2(dir,filename,zfill=2):
    name1 = splitext(basename(filename))[0]
    houzhui = splitext(basename(filename))[1]
    for i in range(1, 10000000):
        filename2 = '%s_%s%s' % (name1, str(i).zfill(zfill), houzhui)
        if os.path.exists(join(dir, filename2)) == False:
            return filename2



'''
# 返回list<list>如：[['5575', 'Womenswear', '-1']]
失败返回None
对返回值的改变会影响原arrtable！！！相信我，测试过了！！！例如下面这个程序：
b=[[1,2],[3,4],[1,4]]
a=find_items(1,b)
a[0][1]=12
a[1][1]=12
print(a)
print(b)
'''
#从arrtable中筛选某一列等于某个对象的所有行
def find_items(find_obj, arr_table, on=0):
    new_arr_table=[]
    for arr in arr_table:
        if arr[on]==find_obj:
            new_arr_table.append(arr)
    if iskong(new_arr_table):
        return None
    return new_arr_table
'''
找不到返回None
对返回值的改变会影响原arrtable！！！相信我，测试过了！！！
'''
#找到相符的第一个
def find_item(find_obj, arr_table, on=0):
    items= find_items(find_obj, arr_table, on)
    if iskong(items):
        return None
    return items[0]


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

#求arr_table的最大宽度
def columns_size_of_arr_table(arr_table):
    max=0
    for arr in arr_table:
        l=len(arr)
        if l>max:
            max=l
    return max
#对list中的元素进行函数处理
'''
不对list直接处理，而是返回新的list
a=[2,3,4]
apply_func_to_list(lambda x:x+1,a)
Out[30]: [3, 4, 5]
'''
def apply_func_to_list(func,arr):
    arr2=[]
    for a in arr:
        arr2.append(func(a))
    return arr2

'''duplicate_add_up用来控制如果转换过程中遇到相同的key，是否把value加起来。
print(arr_table_to_map([['234',324],['234',100]],True))
返回：{'234': 424}
'''
def arr_table_to_map(arr_table,duplicate_add_up=False):
    map={}
    for arr in arr_table:
        if duplicate_add_up==False or try_once(lambda :map[arr[0]],False) is None:
            map[arr[0]]=arr[1]
        else:
            map[arr[0]]+=arr[1]
    return map

'''
type=1: [{'a1':'key1','a2':'key2'},{'a1':'key3','a2':'key4'}]——>[['key1', 'key2'], ['key3', 'key4']]
type=2: {'a1':'key1','a2':'key2'}——> [[a1,key1],[a2,key2],...]
'''
def map_to_arr_table(map,type=1):
    if type==1:
        arr_table=[]
        for m in map:
            arr_table.append(list(m.values()))
        return arr_table
    if type==2:
        arr_table=[]
        for key,value in map.items():
            arr_table.append([key,value])
        return arr_table

'''
sort_arr_table([[1,3],[2,7],[3,5]],on=1)
Out[4]: [[1, 3], [3, 5], [2, 7]]
'''
def sort_arr_table(arr_table,on=0,reverse=False):
    c=[]
    for i in range(0,columns_size_of_arr_table(arr_table)):
       c.append(i)
    on_c=[on]
    on_c.extend(c)
    new_arr_table=get_columns_of_table(on_c,arr_table)
    new_arr_table.sort(reverse=reverse)
    new_arr_table=get_columns_of_table(apply_func_to_list(lambda x:x+1,c),new_arr_table)
    return new_arr_table

'''
arr1=[[12,2,3],[3,4,3],[12,34,3]]
print(count_rows(12,arr1))
返回2
'''
#找到值为xxx的个数
def count_rows(value,arr_table,on=0):
    return len(find_items(value,arr_table,on=on))
'''例如：大于9的个数：
arr1=[[12,2,3],[3,4,3],[12,34,3]]
print(count_rows_by_func(lambda x: True if x>9 else False,arr1))

参数on设置为-1，就是对整个row施加func，这个可以用来判断列A大于列B的row
'''
#通过函数查找，返回个数
def count_rows_by_func(func,arr_table,on=0):
    return len(find_items_by_func(func, arr_table, on=on))


#获取mac地址 以注销该方法
'''08:3E:8E:E6:26:9A
这个方法居然会返回不同的mac地址。。我也不知道怎么搞了。ipconfig all里面也有好多个mac地址，不知道应该用哪一个。
'''
# def get_mac_address():
#     import uuid
#     mac=uuid.UUID(int = uuid.getnode()).hex[-12:].upper()
#     return '%s:%s:%s:%s:%s:%s' % (mac[0:2],mac[2:4],mac[4:6],mac[6:8],mac[8:10],mac[10:])

#获取主机名
'''CN2215946W1.ey.net'''
def get_pc_name():
    import socket
    pcname = socket.getfqdn(socket.gethostname())
    return pcname

#获取用户名
'''HH653AU'''
def get_windows_user():
    import getpass
    return getpass.getuser()


# #取用户名中的数字字母且变成小写
# '''
# Claire SM Ma——>clairesmma
# '''
# def get_windows_user2():
#     user=get_windows_user()
#     t = re.findall('[0-9,a-z,A-Z]', user)
#     return ''.join(t).lower()


my_timezones=['Asia/Shanghai','US/Pacific','utc']
#datetime转标准时间字符串
'''标准的是这样的：
2018-04-21 04:03:09
'''
def datetime_to_str(d):
    return d.strftime('%Y-%m-%d %H:%M:%S')

#标准时间字符串转datetime
def datetime_f_str(time_str):
    d = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
    return d

'''
need_tz表示是否需要带上timezone，如果不是为了显示，都带上!
'''
#datetime转带时区的标准时间字符串
def datetime_to_str2(d,need_tz=False):
    if need_tz:
        return d.strftime('%Y-%m-%d %H:%M:%S%z')
    else:
        return d.strftime('%Y-%m-%d %H:%M:%S')
'''
need_tz表示是否需要带上timezone，如果不是为了显示，都带上!
datetime_f_str2('2019-02-21 00:00:00',has_tz=False) 不推荐
datetime_f_str2('2019-02-21 02:32:37+0000') 推荐
datetime_f_str2('2019-02-21 00:00:00',False,my_timezones[0]) 推荐，这个相当于是给没有time zone的时间字符串加上time zone。
'''
#带时区的标准时间字符串转datetime
def datetime_f_str2(time_str, has_tz=False,specified_time_zone=None):
    if has_tz:
        d = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S%z')
    else:
        if specified_time_zone is None:
            d=datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
        else:
            d=datetime(int(time_str[0:4]),int(time_str[5:7]),int(time_str[8:10])
                              ,int(time_str[11:13]),int(time_str[14:16]),int(time_str[17:19]))
            d=pytz.timezone(specified_time_zone).localize(d)
    return d

#获取当前的utc标准时间
def get_current_time(fetch_from_server=False):
    if fetch_from_server:
        c = ntplib.NTPClient()
        response = c.request('pool.ntp.org')
        ts = response.tx_time
        return unix_time_to_datetime(ts)
    else:
        d=datetime.now(pytz.utc)
        return d


#Unix时间戳转换为datetime，单位：second
def unix_time_to_datetime(unix_time):
    unix_time=int(unix_time)
    return datetime.fromtimestamp(unix_time,pytz.utc)
#datetime转换为Unix时间戳
def datetime_to_unix_time(d):
    return d.timestamp()

#返回这天的00:00:00
def datetime_to_day_start(d,specified_time_zone):
    d=change_timezone(d,specified_time_zone)
    return datetime_f_str2(datetime_to_str(d)[0:10]+' 00:00:00',specified_time_zone=specified_time_zone)

'''
没有时区信息的datetime会返回None
'''
#获取datetime的时区信息
def get_timezone(d):
    l=try_once(lambda :(d.tzinfo.tzname(d),d.tzinfo.utcoffset(d)))
    return l

'''
t=get_current_time()
print(t)
t2=delete_timezone(t)
print(t2)
输出：
2019-05-30 05:01:19.170594+00:00
2019-05-30 05:01:19
'''
#删除timezone
def delete_timezone(d):
    return datetime_f_str2(datetime_to_str2(d,False))

'''
默认转换为北京时间
转化为utc时间：change_timezone(obj.get('createdAt'),my_timezones[2])
'''
#改变datetime的时区
def change_timezone(d:datetime,tz_name=my_timezones[0]):
    if tz_name =='utc':
        tz=pytz.utc
    else:
        tz=pytz.timezone(tz_name)
    d=d.astimezone(tz)
    return d

'''
由于我们假设我们的所有的时间都应该设置时区的，即便是str也是带时区的，因此不存在set timezone直接设置时区的方法了，就不要了。
'''



def my_encode(string):
    bytes=string.encode('utf8')
    a1=base64.encodebytes(bytes)
    a1=str(a1,'utf8')
    #a1='sm5zqt=xUt'+a1+'1x=MTItMz=' #原来的加密
    a1 = 'dGhpcyBpcyBhIGXku' + a1 + 'rlspvlkpbllaHmgZD'
    bytes = a1.encode('utf8')
    a1 = base64.encodebytes(bytes)
    a1 = str(a1, 'utf8')
    #a1 = 'diw9Ndx2k=' + a1 + '02x8kMD9xo'
    a1 = '55yL5oiR6KeJ5b6X6' + a1 + '5pWZ5biI6IqC55qE5'
    return a1

def my_decode(string):
    a1=string
    a1=a1[17:-17]
    a1=str(base64.decodebytes(a1.encode('utf8')),'utf8')
    a1 = a1[17:-17]
    a1 = str(base64.decodebytes(a1.encode('utf8')), 'utf8')
    return a1

#对bytes进行加密成string，以便传输
def b64_encode(bytes,encode='utf-8'):
    a1 = base64.encodebytes(bytes)
    a1=str(a1,encode)
    return a1

#对base64加密的string进行解码，变成bytes
def b64_decode(string,encode='utf-8'):
    a1 = string.encode(encode)
    a1=base64.decodebytes(a1)
    return a1


#获取一个临时目录（创建好了的）
def get_tmp_dir():
    name=str(int(time.time()*10000))+str(random.randint(1,10000))
    while exists(name):
        name = str(int(time.time() * 10000)) + str(random.randint(1, 10000))
    mkdir(join(temppath,name))
    return join(temppath,name)

#打开一个文件或者dir
def open_f(f_path):
    os.system('start "" "%s"'%f_path)

'''
错误返回-1
正确返回index
'''
#在一个list中查找item
def find_from_list(item,list):
    a=try_once(lambda :list.index(item),needPrint=False,return_when_error=-1)
    return a

#设置config模块~
'''
例如：font,12
每一行用\r\n来间隔
'''
#设置config
def set_config(key,value,config_file):
    if exists(config_file) ==False:
        content=''
    else:
        content=readfile(config_file)
    arr_table=csvStr_to_arr_table(content)
    if iskong(arr_table):#arr_table为空时。
        arr_table2 = [[key,value]]
    else:
        arr_table2=[]
        finded=False
        for arr in arr_table:
            if arr[0]==key:
                arr_table2.append( [key,value])
                finded=True
            else:
                arr_table2.append(arr)
        if finded==False:
            arr_table2.append([key, value])
    arr_table_to_csv(arr_table2,config_file,line_spliter='\r\n')
#读取config
def get_config(key,config_file):
    content=readfile(config_file)
    arr_table=csvStr_to_arr_table(content)
    item=find_item(key,arr_table)
    if item is None:
        return None
    return item[1]

#终止进程（名字） 用taskkill
def kill_process(process_name):
    cmd_str='taskkill /f /im %s'%process_name
    cmd(cmd_str)

#终止进程（路径）
def kill_process_by_path(exe_path):
    exe_path=exe_path.replace('\\','\\\\')#不知道为什么只有\\才能用，其他的cmd命令就不是
    cmd_str=r'wmic process where executablepath="%s" delete'%(exe_path)
    t=cmd(cmd_str)

#判断是否有名为xxx的进程在运行
def is_process_running(process_name):
    #wmic process where name="jqs.exe" get executablepath
    cmd_str=r'wmic process where name="%s" get executablepath'%process_name
    t=cmd(cmd_str)
    if t.find(process_name)!=-1:
        return True
    else:
        return False

#判断是否有路径为xxx的进程在运行
def is_process_running_by_path(exe_path):
    exe_path2=exe_path.replace('\\','\\\\')#不知道为什么只有\\才能用，其他的cmd命令就不是
    cmd_str=r'wmic process where executablepath="%s"'%(exe_path2)
    t=cmd(cmd_str)
    if t.find(exe_path)!=-1:
        return True
    else:
        return False

'''
merge=1 or 2都已经生成了exe测试过了，请放心使用。
by=path 通过路径检测
by=name 通过进程名称检测
merge参数是因为，oneExe单文件的exe一次运行会有两个一样的进程，所以其中两个merge成一个，merge参数设为2
而生成文件夹的exe一次运行就一个进程，所以merge就是1。
rmconsole对进程的个数没影响。
'''
#检测本身是否已经有实例在运行了
def is_myself_already_running(by='path',merge=1):
    name=basename(sys.executable)
    cmd_str = r'wmic process where name="%s" get executablepath' % name
    t = cmd(cmd_str)
    arr=re.findall('.+exe', t)


    if by=='path':
        if arr.count(sys.executable)>=2*merge:
            return True
        else:
            return False
    #通过名字判断是否重复
    elif by=='name':
        if len(arr)>=2*merge:
            return True
        else:
            return False
    raise Exception('输入参数by错误！当前输入：'+str(by))

'''
使用方法：
在py文件里声明：print=log_print
或者带参数的：print=lambda s:log_print(s,join(dirname(shut_down_exe_path),'prints.dat'))
声明后只对有这个声明的py文件生效，无论你怎么互相import，其他py文件里面的print方法都不会受到影响。
log模式下，所有的print方法都不仅会print，还会在当前文件目录下新建一个prints.dat的文件，log都会放在里面。
默认最大1m，超过1m就截取最近的log放了。
'''
#log模式
def log_print(s,log_file='./prints.dat',limit=1024*1024):
    def append_to_log(string, log_file, limit):
        content = try_once(lambda: readfile(log_file), return_when_error='', ignore_conflict=True)
        content = content + string
        size = len(content)
        if size > limit:
            # 截取最下面的
            content = content[size - limit, size]
        writefile(content, log_file)
    line = '[%s]输出: %s\r\n' % (datetime_to_str(datetime.now()), s)
    builtins.print(line)
    # 打入logfile
    try:
        if exists(log_file) == False:
            mkdir(dirname(log_file))
        append_to_log(line, log_file, limit)
    except Exception as e:
        builtins.print('log出错，错误代码：' + str(e))


#权限相关测试
r'''
权限相关：
1、python（或python生成的）有管理员权限时，其os.system是否具有管理员权限？
  是的。
2、python（或python生成的）有管理员权限时，其os.system所启动的exe是否具有管理员权限？
  是的。cmd2(r'start "" "C:\Users\Administrator\Desktop\1.exe"') 这样的1.exe也是有管理员权限的。
3、没有管理员权限时，Python、cmd是否可以在C:\Program Files (x86)\Run2\Run\resources中创建文件或者修改已存在
的文件？
  不可以，writefile('test',r'C:\Program Files (x86)\Run2\Run\resources\123.txt')方法将会返回Permission
Error.
4、当exe处于C:\Program Files (x86)\Run2\Run目录下时，是否可以新建、修改文件？
  不可以。
5、当exe中的路径以相对路径来表示时，是否可以修改当前目录或下级目录的文件？
  不可以。
6、把整个文件夹拷贝到Program Files (x86)\Run2\Run下覆盖，运行exe能够删改文件？
  不可以。靠。
7、直接拷贝exe文件夹到Program Files (x86)\Run2\Run下，exe能否删改文件？
  不可以。
8、是否是因为自解压后才有权限？
  不是。
9、是否是因为先读取才能写入？或者因为后缀是txt？
  不是。
10、是否是因为是QT程序才能写入？
  不是。
11、通过虚拟机编译成32位程序后能否写入？
  可以。在虚拟环境中写入成功：C:\Users\Administrator\AppData\Local\VirtualStore\Program Files (x86)\Run22\新建文件夹\resources

12、虚拟环境下，如果改变了exe或者txt，其中txt可能是备份在了virtual store的，那么这边改了以后，程序读取到的是哪一个呢？
13、直接用绝对路径是否可以出发virtual store？  


  1、先判断是否处于一个需要权限才能写入的环境

'''
#api说明
'''
两个方法都测试过了，没有问题，请放心使用
这两个方法没有放到mytools里面，因为觉得不一定会每个程序都用到。
'''
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

r'''
非阻塞方法
优点在于本身的进程结束后，启动的进程仍然继续运行。
已知bug：用这个方法来启动electron会出现参数传了但是还是无法识别的状况，第二天再次测试的时候发现根本就不能启动。。而且只有electron的exe有这个问题。但是暂时懒得搞了。
这个函数的参数参考：https://docs.microsoft.com/en-us/windows/desktop/api/shellapi/nf-shellapi-shellexecutew

'''
def run(file_path, parameters, need_admin=False, show_window=False):
    a=9 if show_window else 0
    b='runas'if need_admin else 'open'
    ctypes.windll.shell32.ShellExecuteW(None, b, file_path, parameters, dirname(file_path), a)


#私有方法，不要直接调用
def __pre_process(key_path):
    if key_path[0:1]== '\\':
        key_path= key_path[1:len(key_path)]
    l=key_path.split('\\')
    if l[0]=='Computer':
        l.pop(0)
    main_key=l.pop(0)
    path='\\'.join(l)
    return eval('winreg.'+main_key),path


#实例化一个带cookie的session
def init_session(cookieStr=None):
    session = requests.Session()
    if cookieStr is not None:
        cookies = requests.utils.cookiejar_from_dict(cookieStrToDict(cookieStr), cookiejar=None, overwrite=True)
        session.cookies = cookies
    return session

'''
type0:get_random_string(8,type=0)：
返回：urfv6884
小写字母的生成中抛弃了：i l o三个字母。
'''
#获取随机字符串
def get_random_string(size, type=0):
    def get_random_lowercase_char():
        exclude=[105,108,111]#i l o
        l = []
        for i in range(97,122+1):
            if find_from_list(i,exclude)==-1:
                l.append(i)
        return chr(l[randint(0,len(l)-1)])
    def get_random_number():
        return str(randint(0,9))

    if type==0:#生成小写字母+数字的混合,一人一半
        size2=int(size/2)
        string=''
        for i in range(0,size2):
            string=string+get_random_lowercase_char()
        for i in range(0, size2):
            string = string + get_random_number()
        return string

'''
返回：直接返回result key值对应的json，出错的话会抛出异常。
'''
#直接通过http请求得到leancloud function的返回值
def send_lencloud_func(cloud_function,appid,appkey,data=None,verify=True,proxies=None):
    url='https://%s.engine.lncld.net/1.1/functions/%s'%(appid[0:8].lower(),cloud_function)
    if data is not None:
        data=json.dumps(data)
    t=requests.post(url=url,
                  headers={'Content-Type': 'application/json','X-LC-Id':appid,'X-LC-Key':appkey},
                  data=data,verify=True,proxies=None).text
    j=try_once(lambda:json.loads(t)['result'],return_when_error='@@@tryonce方法唯一标识@@@')
    if j is '@@@tryonce方法唯一标识@@@':
        raise Exception('云函数返回值json化出错！返回值：\n'+t)
    else:
        print(j)
        return j


#生成二维码
def generate_qr_code(qr_url,target_file='temp.png',need_open=True):
    img=qrcode.make(qr_url)
    img.save(target_file)
    if need_open:
        open_f(target_file)

'''
判断是否是纯ASCII码字符
数字、大小写、英文符号都返回True，中文返回False
'''
def is_ASCII(keyword):
    return all(ord(c) < 128 for c in keyword)

'''
mode第一个字母o表示overwirte,否则填其他的，例如空格或者n。
第二个表示是send to trash 还是 直接 open 然后写入。
例如：
'os'就表示覆盖，send to trash
'oo'就表示覆盖，直接写入
'n'就表示不覆盖。
'''
def copy_tree(source_dir,target_dir,mode='os'):
    if exists(target_dir)==False:
        mkdir(target_dir)
    def copy_file(source_file,target_file,mode=mode):
        if exists(target_file) and mode[0]=='o':
            if mode[1]=='s':
                try:
                    send_to_trash(target_file)
                    shutil.copyfile(source_file,target_file)
                except Exception as e:
                    print(e)
            elif mode[1]=='o':
                try:
                   b=readfile_b(source_file)
                   writefile_b(target_file,b)
                except Exception as e:
                    print(e)
            else:
                raise Exception('参数错误！')
        else:
            try:
                shutil.copyfile(source_file, target_file)
            except Exception as e:
                print('未知错误！并非overwrite情况下出错：'+str(e))
    for file in os.listdir(source_dir):
        f=join(source_dir,file)
        if isdir(f):
            copy_tree(f,join(target_dir,file),mode)
        else:
            copy_file(f,join(target_dir,file))

'''
wait 是true表示阻塞运行
否则使用popen表示非阻塞运行。
'''
def taskkill(exe_name,wait=True):
    if wait:
        cmd2('taskkill /f /im %s'%exe_name)
    else:
        os.popen('taskkill /f /im %s'%exe_name)

'''
做func1：做func2的比例= freq1：freq2
例如：random_do(lambda :print('1'),lambda :print(2),90,10)
'''
def random_do(func1,func2,frequency1:int,frequency2:int):
    a=random.randint(0,frequency1+frequency2)
    if a>=0 and a<=frequency1:
        return func1()
    else:
        return func2()



#转换成qt的path
def to_qt_path(path):
    return path.replace('\\', '/')

def to_pickle_bytes(obj,protocol=3):
    f = BytesIO()
    pickle.dump(obj,f,protocol=protocol)
    return f.getvalue()
def from_pickle_bytes(bytes,protocal=3):
    f = BytesIO(bytes)
    return pickle.load(f)

