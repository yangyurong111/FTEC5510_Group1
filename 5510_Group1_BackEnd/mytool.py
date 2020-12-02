# -*- coding: utf-8 -*-
"""
Created on Fri Sep 14 09:12:03 2018

@author: NI YOU DU
"""
import time
import shutil
import random
import codecs
import decimal
import re
import subprocess
import chardet
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import base64
import requests
import rsa
import psutil
import signal
import copy
import json
import qrcode
import datetime
import pytz
import threading
from io import BytesIO
from sys import version_info
from PIL import Image
#import pypinyin
import traceback
import gzip
import v
import zipfile
import string

'''
该方法timeout之后子线程实际还在运行，并没有被kill
'''
def xiancheng(fun,timeout=0):
    t = threading.Thread(target=fun)
    t.setDaemon(True)
    t.start()
    t.join(timeout)

def cmd(cmd_string,encoding='gbk',ignore=True):
#cmd 命令调用
    ignore_str='ignore'if ignore else 'strict'
    proc = subprocess.Popen(cmd_string, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=True)
    out, err = proc.communicate()
    if encoding=='auto_detect':
        if len(err)>len(out):
            encoding=chardet.detect(err)['encoding']
        else:
            encoding=chardet.detect(out)['encoding']
    out_msg=out
    err_msg=err
    if out==b'':
        out_msg=None
        err_msg=str(err,encoding,ignore_str)
    if err==b'':
        err_msg=None
        out_msg=str(out, encoding, ignore_str)
    return [err_msg,out_msg]
def install(package,mirror=None,path='D:\ProgramData\Scripts',encoding='gbk'):
#安装扩展包，调用清华镜像
    path_disk=path[0:1]
    if mirror==None:
        msg=cmd('%s %s &pip install %s'%(path_disk,path,package),encoding)
        print(msg)
    else:
        msg=cmd('%s %s &pip install -i https://pypi.tuna.tsinghua.edu.cn/simple %s'%(path_disk,path,package),encoding)
        print(msg)
def uninstall(package,mirror=None,path='D:\ProgramData\Scripts',encoding='gbk'):
    path_disk=path[0:1]
    if mirror==None:
        msg=cmd('%s %s &pip uninstall %s'%(path_disk,path,package),encoding)
        print(msg)


'''
这种方法不能解决双层嵌套的list
'''
def str_to_list(s):
    s_list1=[]
    s_list = s.strip(',').strip('[').strip(']').split(',')
    for i in s_list:
        i1=i.strip(' ').strip('\'').strip('\"')
        s_list1.append(i1)
    return s_list1
def str_to_list_dict(s):
    s_list1=[]
    s_list = s.strip(',').strip('[').strip(']').split('},')
    for i in s_list:
        if i[-1:]!="}":
            i=i+"}"
        i1=i.strip(' ').strip('\'').strip('\"')
        i2=eval(i1)
        s_list1.append(i2)
    return s_list1
'''
s="[{'domain': 'passport.baidu.com', 'httpOnly': False, 'name': 'Hm_lpvt_90056b3f84f90da57dc0f40150f005d5', 'path': '/', 'secure': False, 'value': '1565956772'}, {'domain': 'passport.baidu.com', 'httpOnly': True, 'name': 'UBI', 'path': '/', 'secure': True, 'value': 'fi_PncwhpxZ%7ETaKAcO3QtS8etGmXxrnvelG5ebyYYehDOxDlf2RZuB58MI7NJnE-OKnPtkbHvihnemMXXdsHdlqGWs1Ardzkt3jkgTI6u-7bq43DyEo8V5Cm54eAoZ-ASHjOKcIysDOQXhZxqiO88b%7E5zskUw__'}]"
print(str_to_list_dict(s))
'''

def list_to_str(l):
    s=str(l) 
    return s
'''
10个10个的分，或者等分成10部分
'''
def split_list(l,count=0,part=0):
    l_new=[]
    if count!=0 and part!=0:
        raise Exception("参数错误，请指定以何种方式分割列表！")
    if count!=0:
        p=len(l)//count
        for i in range(0,p):
            l_new.append(l[count*i:count*i+count])
            if i==p-1 and len(l)!=count*p:
                l_new.append(l[count*(i+1):])
        return(l_new)
    if part!=0:
        p=part
        count=len(l)//p
        for i in range(0,p):
            if i==p-1 and len(l)>count*p:
                l_new.append(l[count*i:])
            else:
                l_new.append(l[count*i:count*i+count])

        return(l_new)
    

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
def writefile(string,file,encoding='gbk'):
    path2=file
    if os.path.exists(shangji_mulu(path2))==False:
        k=1
        path_list=[]
        while shangji_mulu(path2)!=path2:
            path_list.append(path2)
            path2=shangji_mulu(path2)
        for i in range(1,len(path_list)):
            if os.path.exists(path_list[len(path_list)-i])!= True:
                os.mkdir(path_list[len(path_list)-i])
    f=codecs.open(file, 'w',encoding=encoding)
    f.write(str(string.encode(encoding, 'ignore'), encoding=encoding))
    f.close()
def writefilea(string,file,encoding='gbk'):
    path2=file
    if os.path.exists(shangji_mulu(path2))==False:
        k=1
        path_list=[]
        while shangji_mulu(path2)!=path2:
            path_list.append(path2)
            path2=shangji_mulu(path2)
        for i in range(1,len(path_list)):
            if os.path.exists(path_list[len(path_list)-i])!= True:
                os.mkdir(path_list[len(path_list)-i])
    f=codecs.open(file, 'a',encoding=encoding)
    f.write(str(string.encode(encoding, 'ignore'), encoding=encoding))
    f.close()
#arr必须是二维的。此方法将arr变为csv存储下来。
def arr_to_csv(arr_table,csvfile,delimiter=',',line_spliter='\n'):
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

def shengcheng_aes(key_size=256):
    '''
    get random key for symmetric encryption
    with key_size bits
    :param key_size: bit length of the key
    :return: bytes key
    '''
    # length for urandom
    ulen = int(key_size/8/4*3)
    key = os.urandom(ulen)
    key1=base64.b64encode(key)
    return key1.decode('utf-8')
def aes_jiami(message, key):
    '''
    use AES CBC to encrypt message, using key and init vector
    :param message: the message to encrypt
    :param key: the secret
    :return: bytes init_vector + encrypted_content
    '''
    iv_len = 16
    assert type(message) in (str,bytes)
    assert type(key) in (str,bytes)
    if type(message) == str:
        message = bytes(message, 'utf-8')
    if type(key) == str:
        key = bytes(key, 'utf-8')
    backend = default_backend()
    iv = os.urandom(iv_len)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(message) + padder.finalize()
    enc_content = encryptor.update(padded_data) + encryptor.finalize()
    k=iv + enc_content
    k1=base64.b64encode(k).decode('utf-8')
    return k1
#print(get_aes_key(key_size=256))
def aes_jiemi(content, key):
    '''
    use AES CBC to decrypt message, using key
    :param content: the encrypted content using the above protocol
    :param key: the secret
    :return: decrypted bytes
    '''
    content=content.encode('utf-8')
    content=base64.b64decode(content)
    assert type(content) == bytes
    assert type(key) in (bytes, str)
    if type(key) == str:
        key = bytes(key, 'utf-8')
    iv_len = 16
    assert len(content) >= (iv_len + 16)
    iv = content[:iv_len]
    enc_content = content[iv_len:]
    backend = default_backend()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    unpadder = padding.PKCS7(128).unpadder()
    decryptor = cipher.decryptor()
    dec_content = decryptor.update(enc_content) + decryptor.finalize()
    real_content = unpadder.update(dec_content) + unpadder.finalize()
    return real_content. decode('utf-8')

def aes_jiemi_lun(content, key,file):
    '''
    use AES CBC to decrypt message, using key
    :param content: the encrypted content using the above protocol
    :param key: the secret
    :return: decrypted bytes
    '''
    r=readfile(file)
    '''
    if iskong(r):
        k3=""
        for i in range(1,101):
            k3=k3+key+'@'
        writefile(aes_jiami(k3,'37OI3yrc9/wf2tvJqY38GxZX4YZoaKwT'),file)
        '''
    if iskong(r):
        raise Exception( "error")
    r_jiemi=aes_jiemi(r,'37OI3yrc9/wf2tvJqY38GxZX4YZoaKwT')
    r_list=r_jiemi.split('@')
    if len(r_list)!=101:
        raise Exception( "error")
    for i in range(0,100):
        if r_list[i]==key:
            raise Exception( "error")
        else:
            pass
    r_list.pop(0)
    r_list.pop(99)
    r_list.append(key)
    k1=''
    for i in range(0,100):
        k1=k1+r_list[i]+'@'
    writefile(aes_jiami(k1,'37OI3yrc9/wf2tvJqY38GxZX4YZoaKwT'),file)
    return aes_jiemi(content,key)
'''
print(shengcheng_aes())
l=aes_jiami('123456','3OXjEOC5VQhw00TX4qJQvyGTay6xe36i')
k=aes_jiemi_lun(l,'3OXjEOC5VQhw00TX4qJQvyGTay6xe36i','./resources/index.png')
print(k)
'''

def print1(s):
    print(s)
    writefilea(str(s)+'\n','log_print.txt')
#print1("dfefedf")
def isshuzi(string):
    for s in string:
        inside_code=ord(s)
        if inside_code > 47 and inside_code <= 57:
            pass
        else:
            return False
    return True
#print(isshuzi('122d'))
def iszimu(s):
    inside_code=ord(s)
    if inside_code > 64 and inside_code <= 122:
        if inside_code <=90 or inside_code >=97:
            return True
        else:
            return False
    else:
        return False
def ishanzi(s):
    uchar=s
    if uchar >= u'\u4e00' and uchar<=u'\u9fa5':
        return True
    else:
        return False
    
def round2(f,i=0):
    a=round((f + 0.00000001), i)
    return a
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
'''
判断是否是纯ASCII码字符
数字、大小写、英文符号都返回True，中文返回False
'''
def is_ASCII(keyword):
    return all(ord(c) < 128 for c in keyword)
def is_zimu(s):
    return s.isalpha()
def is_shuzi(s):
    return s.isdigit()


def bianli_mulu(path,child=False):
    if child==False:
        l=[]
        for i in os.listdir(path):
            l.append(path+'\\'+i)
        return l
    else:
        l=[]
        for root, dirs, files in os.walk(path):
            for file in files:
                k=os.path.join(root,file)
                l.append(k)
        return l


#path_=r'C:\Users\Administrator\Desktop\python_document\python_document\新 发票查验\js'
#l_bianli=bianli_mulu(path_,child=False)
#print(l_bianli)

def xiuzheng_mulu(path):
    path=path.replace('\\','/')
    return path


def suiji_chouqu(l):
    k=random.randint(0,len(l)-1)
    return(l[k])

def delete(path):
    try:
        os.remove(path)
    except:
        try:
            shutil.rmtree(path)
        except:
            #print('删除文件失败')
            return('删除文件失败')
def shengcheng_rsa():
    # 生成密钥
    (pubkey, privkey) = rsa.newkeys(1024)
    # 保存密钥
    with open('public.pem','w+') as f:
        f.write(pubkey.save_pkcs1().decode())
    with open('private.pem','w+') as f:
        f.write(privkey.save_pkcs1().decode())


def rsa_jiami(message):
    with open('public.pem','r') as f:
        pubkey = rsa.PublicKey.load_pkcs1(f.read().encode())
        # 公钥加密
        crypto = rsa.encrypt(message.encode(), pubkey)
        k1=base64.b64encode(crypto).decode('utf-8')
        return k1


def rsa_jiemi(message):
    content=message.encode('utf-8')
    crypto=base64.b64decode(content)
    with open('private.pem','r') as f:
        privkey = rsa.PrivateKey.load_pkcs1(f.read().encode())
        # 私钥解密
        message = rsa.decrypt(crypto, privkey).decode()
        return message
def suoyou_jincheng():
    l=[]
    def getAllPid():
        pid_dict={}
        pids = psutil.pids()
        try:
            for pid in pids:
                p = psutil.Process(pid)
                pid_dict[pid]=p.name()
                l.append(p.name())
        except:
            pass
            #print("pid-%d,pname-%s" %(pid,p.name()))
        return pid_dict
    dic = getAllPid()
    return l
def shasi_jincheng(jincheng):
#print os.getpid()
    def getAllPid():
        pid_dict={}
        pids = psutil.pids()
        try:
            for pid in pids:
                p = psutil.Process(pid)
                pid_dict[pid]=p.name()
        except:
            pass
            #print("pid-%d,pname-%s" %(pid,p.name()))
        return pid_dict
    
    def kill(pid):
        try:
            kill_pid = os.kill(pid, signal.SIGABRT)
            print ('已杀死pid为%s的进程,　返回值是:%s' % (pid, kill_pid))
        except Exception as e:
            pass
            #print ('没有如此进程!!!')
    dic=getAllPid()
    for t in dic.keys():
        if dic[t]==jincheng:
            kill(t)

def xiazai(url, filePath,show_state=True,status_obj=None):
    # https://video-subtitle.tedcdn.com/talk/podcast/2015Z/None/JasondeCairesTaylor_2015Z-480p-en.mp4
    #默认覆盖！
    if status_obj is not None:
        status_obj.speed = 0
        status_obj.percent = 1
        status_obj.need_time = 0
    #首先可能要新建文件夹
    try:
        os.mkdir(filePath)
    except:
        pass
    res = requests.get(url, stream=True)
    res.raise_for_status()
    contentLength = int(res.headers.get('Content-Length'))
    if show_state:
        print('总大小：' + str(round(contentLength / 1024 / 1024, 2)) + " mb")
    if status_obj is not None:
        status_obj.length_mb=str(round(contentLength / 1024 / 1024, 2))

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
            if show_state:
                print('速度：' + str(v) + ' kb/s  百分比：' + str(percent) + "%  预计剩余：" + str(yuji) + '分钟')
            if status_obj is not None:
                status_obj.speed=v
                status_obj.percent=percent
                status_obj.need_time= yuji
            display = 0
    playFile.close()
    try:
        os.rename(filePath+'.tmp',filePath)
    except FileExistsError as e:
        delete(filePath)
        os.rename(filePath + '.tmp', filePath)

    if show_state:
        print('下载完成！')
    if status_obj is not None:
        status_obj.speed = 0
        status_obj.percent = 100
        status_obj.need_time = 0
        
path=r'C:\Users\Administrator\Desktop\python_document\ifind\自己的主界面'
def shangji_mulu(path):
    path=xiuzheng_mulu(path)
    return os.path.dirname(path)
def round2(f,i=0):
    a=round((f + 0.00000001), i)
    return a
def fuzhi_list(l):
    l2=copy.deepcopy(l)
    return l2
def zhengze_inner(s1,reg_str):
    def return_raw(reg_str):
        k5=True
        while k5:
            for i2 in range(0,len(reg_str)):
                if reg_str[i2]=='(' or reg_str[i2]==')':
                    if i2==0:
                        reg_str=reg_str[1:]
                        break
                    if i2>=0:
                        if reg_str[i2-1]=='\\':
                            pass
                        else:
                            reg_str=reg_str[:i2]+reg_str[i2+1:]
                            break
                        
                if i2==len(reg_str)-1:
                    return reg_str
    reg_str_raw=return_raw(reg_str)             
    l=[]
    for i in range(0,len(reg_str)):
        if reg_str[i]=='(':
            if i==0:
                l.append(0)
            if i>0:
                if reg_str[i-1]!='\\':
                    reg_str_new='('+return_raw(reg_str[:i])+')'+return_raw(reg_str[i+1:])
                    k6=re.match(reg_str_new,s1)
                    l.append(len(k6.groups()[0]))
    return l
'''  
print(zhengze_inner('0123456789500, 500)','(0)123(456)789[0-9]*, ([0-9]*)\)'))
'''
def zhengze(string,reg_str,return_type='span',clean=False,need_print=False):
    #return_type='span' 返回很多个[1,2] 前面是一个匹配的start，后面是end
    #return_type='start'返回[2,5,7,23] 所有匹配的start
    # return_type='end'返回[2,5,7,23] 所有匹配的end
    if clean==True:
        for k in range(0,33):
            o=chr(k)
            string=string.replace(o,'')
            reg_str=reg_str.replace(o,'')
            string=string.replace(o,' ')
            reg_str=reg_str.replace(o,' ')
        writefile(string,'原string.txt')
        writefile(reg_str,'原reg.txt')
    s=string
    arr=[]
    cut_index=0
    if need_print==True:
        print("使用清除模式需要将.*变为.*?，并且关键reg要一个一个加上去/n用后面的表达式更好([\u4e00-\u9fa5_a-zA-Z0-9_]{1,20})")
    while True:
        arr0=[]
        m=re.search(reg_str,string)
        if m==None:
            break
        s1=m.group()
        l=zhengze_inner(s1,reg_str)
        start=m.span()[0]
        end=m.span()[1]
        #arr.append([start+cut_index,end+cut_index,s[start+cut_index:end+cut_index]])
        k_leiji=start
        k1=0
        for i in m.groups():
            '''
            k2=re.search(i,s1)
            start_inner=k2.span()[0]
            end_inner=k2.span()[1]
            '''
            start_inner=l[k1]
            end_inner=start_inner+len(i)
            k1=k1+1
            '''
            print('开始位置'+str(cut_index+start_inner+k_leiji)+'结束位置'+str(cut_index+end_inner+k_leiji-1))
            '''
            arr0.append([cut_index+start_inner+k_leiji,cut_index+end_inner-1+k_leiji,i])
            #14,16,19,21

            
        arr.append(arr0)   
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
def ui_zhuan_py(path):
    xiuzhengmulu=xiuzheng_mulu(path)
    shangjimulu=shangji_mulu(path)
    cmd_string='d:&cd D:\ProgramData\Anaconda3\Scripts&pyuic5 -o %s %s &'%(xiuzhengmulu[:-3]+'.py',xiuzhengmulu)
    cmd_string=xiuzheng_mulu(cmd_string)
    print(cmd_string)
    cmd(cmd_string)
    path_py=xiuzhengmulu[:-3]+'.py'
    r=readfile(path_py)
    '''
    resize
    '''
    while True:
        k1=zhengze(r,'.resize\(([0-9]*), [0-9]*\)')
        if k1==[]:
            break
        j = k1[0]
        r=r[:j[0][0]]+j[0][2]+'*v.factory_x'+r[j[0][1]+1:]

    while True:
        k1=zhengze(r,'.resize\(.*, ([0-9]*)\)')
        if k1==[]:
            break
        j = k1[0]
        r=r[:j[0][0]]+j[0][2]+'*v.factory_y'+r[j[0][1]+1:]
    '''
    QtCore.QRect
    '''
    while True:
        k1=zhengze(r,'QtCore.QRect\(([0-9]*), [0-9]*, [0-9]*, [0-9]*\)')
        if k1==[]:
            break
        j = k1[0]
        r=r[:j[0][0]]+j[0][2]+'*v.factory_x'+r[j[0][1]+1:]
    while True:
        k1=zhengze(r,'QtCore.QRect\([^,]*, ([0-9]*), [0-9]*, [0-9]*\)')
        if k1==[]:
            break
        j = k1[0]
        r=r[:j[0][0]]+j[0][2]+'*v.factory_y'+r[j[0][1]+1:]

    while True:
        k1=zhengze(r,'QtCore.QRect\([^,]*, [^,]*, ([0-9]*), [0-9]*\)')
        if k1==[]:
            break
        j = k1[0]
        r=r[:j[0][0]]+j[0][2]+'*v.factory_x'+r[j[0][1]+1:]

    while True:
        k1=zhengze(r,'QtCore.QRect\([^,]+, [^,]+, [^,]+, ([0-9]*)\)')
        if k1==[]:
            break
        j = k1[0]
        r=r[:j[0][0]]+j[0][2]+'*v.factory_y'+r[j[0][1]+1:]
        
    while True:
        k1=zhengze(r,'(font\.setPointSize\()[0-9]*(\))')
        if k1==[]:
            break
        j = k1[0]
        r=r[:j[0][0]]+'font.setPixelSize(round2('+r[j[0][1]+1:j[1][0]]+'*17/10*v.factory_x,0))'+r[j[1][1]+1:]

    '''
    font.setPointSize(10)
    font.setPixelSize(round2(10*17/10*v.factory_x,0))
    '''
    try:
        k1=zhengze(r,'(def setupUi\(self, [a-zA-Z]*\):)')
        j = k1[0]
        r=r[:j[0][0]]+j[0][2]+'\n        self.shadow_margin=int(10*v.factory_x)'+r[j[0][1]+1:]
    except:
        pass
    writefile(r,path_py,encoding='utf-8')


def py_zhuan_py(path):
    xiuzhengmulu = xiuzheng_mulu(path)
    shangjimulu = shangji_mulu(path)
    path_py = xiuzhengmulu[:-3] + '.py'
    path_py_correct=xiuzhengmulu[:-3] +'_correct'+ '.py'
    r = readfile(path_py)
    '''
    resize
    '''
    while True:
        k1 = zhengze(r, '.resize\(([0-9]*), [0-9]*\)')
        if k1 == []:
            break
        j = k1[0]
        r = r[:j[0][0]] + j[0][2] + '*v.factory_x' + r[j[0][1] + 1:]

    while True:
        k1 = zhengze(r, '.resize\(.*, ([0-9]*)\)')
        if k1 == []:
            break
        j = k1[0]
        r = r[:j[0][0]] + j[0][2] + '*v.factory_y' + r[j[0][1] + 1:]
    '''
    QtCore.QRect
    '''
    while True:
        k1 = zhengze(r, 'QtCore.QRect\(([0-9]*), [0-9]*, [0-9]*, [0-9]*\)')
        if k1 == []:
            break
        j = k1[0]
        r = r[:j[0][0]] + j[0][2] + '*v.factory_x' + r[j[0][1] + 1:]
    while True:
        k1 = zhengze(r, 'QtCore.QRect\([^,]*, ([0-9]*), [0-9]*, [0-9]*\)')
        if k1 == []:
            break
        j = k1[0]
        r = r[:j[0][0]] + j[0][2] + '*v.factory_y' + r[j[0][1] + 1:]

    while True:
        k1 = zhengze(r, 'QtCore.QRect\([^,]*, [^,]*, ([0-9]*), [0-9]*\)')
        if k1 == []:
            break
        j = k1[0]
        r = r[:j[0][0]] + j[0][2] + '*v.factory_x' + r[j[0][1] + 1:]

    while True:
        k1 = zhengze(r, 'QtCore.QRect\([^,]+, [^,]+, [^,]+, ([0-9]*)\)')
        if k1 == []:
            break
        j = k1[0]
        r = r[:j[0][0]] + j[0][2] + '*v.factory_y' + r[j[0][1] + 1:]

    while True:
        k1 = zhengze(r, '(font\.setPointSize\()[0-9]*(\))')
        if k1 == []:
            break
        j = k1[0]
        r = r[:j[0][0]] + 'font.setPixelSize(round2(' + r[j[0][1] + 1:j[1][0]] + '*17/10*v.factory_x,0))' + r[j[1][1] + 1:]
    try:
        k1 = zhengze(r, '(def setupUi\(self, [a-zA-Z]*\):)')
        j = k1[0]
        r = r[:j[0][0]] + j[0][2] + '\n        self.shadow_margin=int(10*v.factory_x)' + r[j[0][1] + 1:]
    except:
        pass
    writefile(r, path_py_correct, encoding='utf-8')


'''
def bendi_jiami(s):
    s1=aes_jiami(s,"riPXbnF+o+5a0dTBYNIufM76jlxxQmyY")
    s2=aes_jiami(s1,"5LJW0rjCsz7POKsKJmT6lhK0fXS/kbfk")
    return s2
'''
def bendi_jiami(s):
    k=shengcheng_aes()
    s1=aes_jiami(s,k)
    s2=s1+shengcheng_aes()+k+shengcheng_aes()
    s3=aes_jiami(s2,"5LJW0rjCsz7POKsKJmT6lhK0fXS/kbfk")
    return s3
'''
def yunduan_jiemi(s):
    s1=aes_jiemi(s,"5LJW0rjCsz7POKsKJmT6lhK0fXS/kbfk")
    s2=aes_jiemi(s1,"riPXbnF+o+5a0dTBYNIufM76jlxxQmyY")
    return s2
'''
def yunduan_jiemi(s):
    s1=aes_jiemi(s,"5LJW0rjCsz7POKsKJmT6lhK0fXS/kbfk")
    s2=s1[:-96]
    key=s1[-64:-32]
    s3=aes_jiemi_lun(s2,key,"./resources/index.png")
    return s3
def bendi_jiemi(s):
    s1=aes_jiemi(s,"/r9VgKOuUxGhsB65og3PHo85dmIMpXY+")
    s2=s1[:-96]
    key=s1[-64:-32]
    s3=aes_jiemi_lun(s2,key,"./resources/index.png")
    return s3

def yunduan_jiami(s):
    k=shengcheng_aes()
    s1=aes_jiami(s,k)
    s2=s1+shengcheng_aes()+k+shengcheng_aes()
    s3=aes_jiami(s2,"/r9VgKOuUxGhsB65og3PHo85dmIMpXY+")
    return s3

'''
k_server = suiji_chouqu(v.server_info)
SERVER = k_server[0] + '/check_pa'
print(SERVER)
ID = k_server[1]
KEY = k_server[2]

data={}
data['code']='2156'
data_json = json.dumps(data)
r = requests.post(SERVER, data=data_json, verify=False)
print(r.text)
'''
def run_cloud(fun,s):
    SERVER = v.outside_ifind_server+'/%s'%fun
    params_jiami = {}
    params_jiami['code'] = bendi_jiami(s)
    data_json = json.dumps(params_jiami)
    try:
        r = requests.post(SERVER, data=data_json,verify=False,timeout=10)
    except:
        print('在run_cloud与服务器post请求时发生异常，但未卡住！')
    r_eval=eval(r.text)
    r_jiemi=bendi_jiemi(r_eval["result"])
    return r_jiemi
def run_cloud2(fun,s):
    SERVER = 'http://47.103.196.168/py_x2'+'/%s'%fun
    #SERVER = 'http://127.0.0.1:8000/py_x2' + '/%s' % fun
    params_jiami = {}
    params_jiami['code'] = bendi_jiami(s)
    data_json = json.dumps(params_jiami)
    try:
        r = requests.post(SERVER, data=data_json,verify=False,timeout=10)
    except:
        print('在run_cloud与服务器post请求时发生异常，但未卡住！')
    r_eval=eval(r.text)
    r_jiemi=bendi_jiemi(r_eval["result"])
    return r_jiemi


'''
查询所有文件的方法如下：
k=run_cloud('print_csv','please print_csv@log_zhifujilu.txt')
print(k)
'''


def try_once(func,needPrint=False,return_when_error=None,ignore_conflict=False):
    try:
        a=func()
        if a ==return_when_error :
            pass
        else:
            return a
    except BaseException as e:
        if needPrint:
            print('错误代码：' + str(e) )
        return return_when_error
    #处理a是None或者a和设定的错误返回值一样的情况
    if ignore_conflict==False:
        raise Exception('函数未出错情况下返回值和错误返回值相同，请注意！返回值为：'+str(return_when_error))
    else:
        return a
def get_random_string(size, type=0):
    def find_from_list(item, list):
        a = try_once(lambda: list.index(item), needPrint=False, return_when_error=-1)
        return a
    def get_random_lowercase_char():
        exclude=[105,108,111]#i l o
        l = []
        for i in range(97,122+1):
            if find_from_list(i,exclude)==-1:
                l.append(i)
        return chr(l[random.randint(0,len(l)-1)])
    def get_random_number():
        return str(random.randint(0,9))

    if type==0:#生成小写字母+数字的混合,一人一半
        size2=int(size/2)
        string=''
        for i in range(0,size2):
            string=string+get_random_lowercase_char()
        for i in range(0, size2):
            string = string + get_random_number()
        return string
def shengcheng_erweima(qr_url,path):
    img=qrcode.make(qr_url)
    img.save(path)
'''
这个获取网络时间的方法就是有点慢，要几秒钟，其他都还好。返回的是一个datetime
'''
def beijing_shijian():
    r = requests.get('http://time.tianqi.com/')
    r_shijian = zhengze(r.text, '北京现在时间：([^。]*)。')
    k=r_shijian[0][0][2]
    da=datetime.datetime.strptime(k,'%Y-%m-%d %H:%M:%S')
    return da

def get_cpu_info():
    s = wmi.WMI()
    cpu = []
    cp = s.Win32_Processor()
    for u in cp:
        cpu.append(
            {
                "Name": u.Name,
                "Serial Number": u.ProcessorId,
                "CoreNum": u.NumberOfCores
            }
        )
 #   print(":::CPU info:", json.dumps(cpu))
    return cpu


def get_disk_info():
    s = wmi.WMI()
    disk = []
    for pd in s.Win32_DiskDrive():
        disk.append(
            {
                "Serial": s.Win32_PhysicalMedia()[0].SerialNumber.lstrip().rstrip(), # 获取硬盘序列号，调用另外一个win32 API
                "ID": pd.deviceid,
                "Caption": pd.Caption,
                "size": str(int(float(pd.Size)/1024/1024/1024))+"G"
            }
        )
 #   print(":::Disk info:", json.dumps(disk))
    return disk
#mac 地址（包括虚拟机的）
def get_network_info():
    s = wmi.WMI()
    network = []
    for nw in s.Win32_NetworkAdapterConfiguration ():  # IPEnabled=0
        if nw.MACAddress != None:
            network.append(
                {
                    "MAC": nw.MACAddress,  # 无线局域网适配器 WLAN 物理地址
                    "ip": nw.IPAddress
                }
            )
#    print(":::Network info:", json.dumps(network))
    return network
#主板序列号
def get_mainboard_info():
    s = wmi.WMI()
    mainboard=[]
    for board_id in s.Win32_BaseBoard ():
        mainboard.append(board_id.SerialNumber.strip().strip('.'))
    return mainboard
def shengcheng_xuliehao():
    return get_cpu_info()[0]['Serial Number']+get_disk_info()[0]['Serial']
def xianzai_shijian(string=True,beijing=True):
    if beijing:
        d=datetime.datetime.now(pytz.timezone('Asia/Shanghai'))
    else:d=datetime.datetime.now()
    d1=str(d)[:19]
    d2=datetime.datetime.strptime(d1,'%Y-%m-%d %H:%M:%S')
    if string==False:
        return d2
    else:
        s=d2.strftime("%Y-%m-%d %H:%M:%S")
        return s
#print(xianzai_shijian())
def list_find_string(l,s):
    for i in range(0,len(l)):
        if l[i]==s:
            return i
    return -1
def string_find_list(s,l):
    for i in range(0,len(l)):
        k=s.find(l[i])
        if k!=-1:
            return [k,i]
    return [-1,-1]

def list_tihuan(s,a,b):
    for i in range(0,len(a)):
        s1=s.replace(a[i],b[i])
        s=s1
    return s
#print(replace_list("1df5e1f6efd6f1f",["1d","1f"],["我","你"]))
#ui_zhuan_py(r"C:\Users\Administrator\Desktop\python_document\my_main_window-发票\ui\W02G1D1_确认订单.ui")
'''
这个copy如果没有路径会自己新建文件夹
'''
def copy(path,path2):
    path3=path2
    if os.path.exists(shangji_mulu(path2))==False:
        k=1
        path_list=[]
        while shangji_mulu(path2)!=path2:
            path_list.append(path2)
            path2=shangji_mulu(path2)
        for i in range(1,len(path_list)):
            if os.path.exists(path_list[len(path_list)-i])!= True:
                os.mkdir(path_list[len(path_list)-i])
    if os.path.isdir(path):
        shutil.copytree(path,path3)
    else:
        shutil.copy(path,path3)
#copy("ui/resources/a.bat","fapiao_pkg/ui/resources/a.bat")
'''
put_in_mainthread2(me,main,main2,main3)
但是经过测试，一般函数都可以，就是有窗口的就是不行。
'''
def put_in_mainthread2(*args):
    class myThread (threading.Thread):
        def __init__(self,args,i):
            threading.Thread.__init__(self)
            self.fun=args[i]
        def run(self):
            self.fun()
    li=[]
    for i in range(0,len(args)):
        t=myThread(args,i)
        li.append(t)
        t.start()
    for t in li:
        t.join()
def gelin_weizhi():
    a=int(1000 * time.time())
    return a
def tujian_origin(img_path):
    def base64_api(uname, pwd, softid, img):
        img = img.convert('RGB')
        buffered = BytesIO()
        img.save(buffered, format="JPEG")
        if version_info.major >= 3:
            b64 = str(base64.b64encode(buffered.getvalue()), encoding='utf-8')
        else:
            b64 = str(base64.b64encode(buffered.getvalue()))
        data = {"username": uname, "password": pwd, "softid": softid, "image": b64,'typeid':'3'}
        result = json.loads(requests.post("http://api.ttshitu.com/base64", json=data).text)
        if result['success']:
            return result["data"]["result"]
        else:
            return result["message"]
        return ""
    img = Image.open(img_path)
    result = base64_api(uname='503105037qq', pwd='luoyu807', softid='4545454', img=img)
    return result
# for i in range(100):
#     print(i)
#     print(tujian_origin(r'C:\Users\50310\Desktop\untitled.png'))
#print(tujian(r'C:\Users\Administrator\Desktop\python_document\my_main_window-发票\fapiao 不采用诺诺\resources\index\1574156677660.png'))

def tupian_to_b64(path):
    with open(path, 'rb') as f:
        base64_data = base64.b64encode(f.read())
        s = base64_data.decode()
        return s
def b64_to_tupian(s,path):
    img_data = base64.b64decode(s)
    with open(path, 'wb') as f:
        f.write(img_data)
#b64_to_tupian(s,"c://1.png")
#k=tupian_to_b64(r'C:\Users\Administrator\Desktop\python_document\my_main_window-发票\fapiao 不采用诺诺\resources\index_1.png')
#k2=run_cloud('shibie',k)
#print(k2)
def tujian(path,key2):
    #key2其实就是01,02,03,04 代表四种颜色
    def dijiwei(path):
        #####检测黑白图片中的字符属于图鉴api答案中的第几位
        im = Image.open(path)
        width = im.size[0]  # 长度
        height = im.size[1]  # 宽度
        l = []
        for k in range(1, 7):  # 遍历所有长度的点
            count = 0
            for i in range(4 + 13 * (k - 1), 4 + 13 * (k)):
                for j in range(0, height):  # 遍历所有宽度的点
                    data = im.getpixel((i, j))  # i,j表示像素点
                    if data == (0, 0, 0):
                        count = count + 1
            if count > 25:
                l.append(k)
        return l

    def shibie_yellow(path):
        im = Image.open(path)
        width = im.size[0]  # 长度
        height = im.size[1]  # 宽度
        for i in range(0, width):  # 遍历所有长度的点
            for j in range(0, height):  # 遍历所有宽度的点
                data = im.getpixel((i, j))  # i,j表示像素点
                # if (data[0] > 120 and data[1] > 140 and data[2] < 180):
                if (data[0] > 120 and data[1] > 140 and data[2] < 120):
                    im.putpixel((i, j), (0, 0, 0))
                    pass
                else:
                    im.putpixel((i, j), (255, 255, 255))
        '''
        去除噪点
        '''
        for i in range(0, width):  # 遍历所有长度的点
            for j in range(0, height):  # 遍历所有宽度的点
                try:
                    data = im.getpixel((i, j))  # i,j表示像素点
                    if data == (0, 0, 0):
                        if im.getpixel((i - 1, j)) == (255, 255, 255) and im.getpixel((i + 1, j)) == (
                        255, 255, 255) and im.getpixel((i, j + 1)) == (255, 255, 255) and im.getpixel(
                                (i + 1, j + 1)) == (255, 255, 255) and im.getpixel((i - 1, j + 1)) == (
                        255, 255, 255) and im.getpixel((i, j - 1)) == (255, 255, 255) and im.getpixel(
                                (i - 1, j - 1)) == (255, 255, 255) and im.getpixel((i + 1, j - 1)) == (255, 255, 255):
                            im.putpixel((i, j), (255, 255, 255))
                except:
                    im.putpixel((i, j), (255, 255, 255))
        t=gelin_weizhi()
        im.save('./resources/index_%s.png'%t)
        k=tupian_to_b64(path)
        result_full=run_cloud('shibie',k)
        l_weishu = dijiwei('./resources/index_%s.png'%t)
        delete('./resources/index_%s.png' % t)
        result = ''
        for c in l_weishu:
            result = result + result_full[c - 1]
        return result


    # shibie_yellow(r'C:\Users\Administrator\Desktop\python_document\my_main_window-发票\fapiao 不采用诺诺\resources\index333.png')
    # print(shibie_yellow(r'C:\Users\Administrator\Desktop\python_document\my_main_window-发票\fapiao 不采用诺诺\screen4.jpg'))

    def shibie_blue(path):
        im = Image.open(path)
        width = im.size[0]  # 长度
        height = im.size[1]  # 宽度
        for i in range(0, width):  # 遍历所有长度的点
            for j in range(0, height):  # 遍历所有宽度的点
                data = im.getpixel((i, j))  # i,j表示像素点
                if (data[0] < 140 and data[1] < 120 and data[2] > 140):
                    # if (data[0] > 150 and data[1] > 150 and data[2] < 100):
                    im.putpixel((i, j), (0, 0, 0))
                    pass
                else:
                    im.putpixel((i, j), (255, 255, 255))
        '''
        去除噪点
        '''
        for i in range(0, width):  # 遍历所有长度的点
            for j in range(0, height):  # 遍历所有宽度的点
                try:
                    data = im.getpixel((i, j))  # i,j表示像素点
                    if data == (0, 0, 0):
                        if im.getpixel((i - 1, j)) == (255, 255, 255) and im.getpixel((i + 1, j)) == (
                        255, 255, 255) and im.getpixel((i, j + 1)) == (255, 255, 255) and im.getpixel(
                                (i + 1, j + 1)) == (255, 255, 255) and im.getpixel((i - 1, j + 1)) == (
                        255, 255, 255) and im.getpixel((i, j - 1)) == (255, 255, 255) and im.getpixel(
                                (i - 1, j - 1)) == (255, 255, 255) and im.getpixel((i + 1, j - 1)) == (255, 255, 255):
                            im.putpixel((i, j), (255, 255, 255))
                except:
                    im.putpixel((i, j), (255, 255, 255))
        t=gelin_weizhi()
        im.save('./resources/index_%s.png'%t)
        k=tupian_to_b64(path)
        result_full=run_cloud('shibie',k)
        l_weishu = dijiwei('./resources/index_%s.png'%t)
        delete('./resources/index_%s.png' % t)
        result = ''
        for c in l_weishu:
            result = result + result_full[c - 1]
        return result

    def shibie_red(path):
        im = Image.open(path)
        width = im.size[0]  # 长度
        height = im.size[1]  # 宽度
        for i in range(0, width):  # 遍历所有长度的点
            for j in range(0, height):  # 遍历所有宽度的点
                data = im.getpixel((i, j))  # i,j表示像素点
                if (data[0] > 150 and data[1] < 120 and data[2] < 160):
                    # if (data[0] > 150 and data[1] > 150 and data[2] < 100):
                    im.putpixel((i, j), (0, 0, 0))
                    pass
                else:
                    im.putpixel((i, j), (255, 255, 255))
        '''
        去除噪点
        '''
        for i in range(0, width):  # 遍历所有长度的点
            for j in range(0, height):  # 遍历所有宽度的点
                try:
                    data = im.getpixel((i, j))  # i,j表示像素点
                    if data == (0, 0, 0):
                        if im.getpixel((i - 1, j)) == (255, 255, 255) and im.getpixel((i + 1, j)) == (
                        255, 255, 255) and im.getpixel((i, j + 1)) == (255, 255, 255) and im.getpixel(
                                (i + 1, j + 1)) == (255, 255, 255) and im.getpixel((i - 1, j + 1)) == (
                        255, 255, 255) and im.getpixel((i, j - 1)) == (255, 255, 255) and im.getpixel(
                                (i - 1, j - 1)) == (255, 255, 255) and im.getpixel((i + 1, j - 1)) == (255, 255, 255):
                            im.putpixel((i, j), (255, 255, 255))
                except:
                    im.putpixel((i, j), (255, 255, 255))
        t=gelin_weizhi()
        im.save('./resources/index_%s.png'%t)
        k=tupian_to_b64(path)
        result_full=run_cloud('shibie',k)
        l_weishu = dijiwei('./resources/index_%s.png'%t)
        delete('./resources/index_%s.png'%t)
        result = ''
        for c in l_weishu:
            result = result + result_full[c - 1]
        return result

    def shibie_black(path):
        im = Image.open(path)
        width = im.size[0]  # 长度
        height = im.size[1]  # 宽度
        for i in range(0, width):  # 遍历所有长度的点
            for j in range(0, height):  # 遍历所有宽度的点
                data = im.getpixel((i, j))  # i,j表示像素点
                if (data[0] < 180 and data[1] < 120 and data[2] < 200):
                    # if (data[0] > 150 and data[1] > 150 and data[2] < 100):
                    im.putpixel((i, j), (0, 0, 0))
                    pass
                else:
                    im.putpixel((i, j), (255, 255, 255))
        '''
        去除噪点
        '''
        for i in range(0, width):  # 遍历所有长度的点
            for j in range(0, height):  # 遍历所有宽度的点
                try:
                    data = im.getpixel((i, j))  # i,j表示像素点
                    if data == (0, 0, 0):
                        if im.getpixel((i - 1, j)) == (255, 255, 255) and im.getpixel((i + 1, j)) == (
                        255, 255, 255) and im.getpixel((i, j + 1)) == (255, 255, 255) and im.getpixel(
                                (i + 1, j + 1)) == (255, 255, 255) and im.getpixel((i - 1, j + 1)) == (
                        255, 255, 255) and im.getpixel((i, j - 1)) == (255, 255, 255) and im.getpixel(
                                (i - 1, j - 1)) == (255, 255, 255) and im.getpixel((i + 1, j - 1)) == (255, 255, 255):
                            im.putpixel((i, j), (255, 255, 255))
                except:
                    im.putpixel((i, j), (255, 255, 255))
        t=gelin_weizhi()
        im.save('./resources/index_%s.png'%t)
        k=tupian_to_b64(path)
        result_full=run_cloud('shibie',k)

        '''验证码收集part1，不要请注释掉
        dangqian_xiancheng=dangqian_xiancheng()
        v.result_full[int(dangqian_xiancheng[-1:])]=result_full
        im.save('./resources/pic/%s.png' % dangqian_xiancheng)
        '''
        l_weishu = dijiwei('./resources/index_%s.png'%t)
        delete('./resources/index_%s.png' % t)
        result = ''
        try:
            for c in l_weishu:
                result = result + result_full[c - 1]
        except:
            pass
        return result
    try:
        if key2=="":
            print('key2不能为空！')
            return ""
        if key2=='02':
            result=shibie_yellow(path)
        if key2=='03':
            result=shibie_blue(path)
        if key2=='01':
            result=shibie_red(path)
        if key2=='00':
            result=shibie_black(path)
        return result
    except Exception as e:
        print(str(e)+"验证码识别交互出错！")
        return ""
#print(tujian(r'C:\Users\Administrator\Desktop\python_document\my_main_window-发票\fapiao 不采用诺诺\resources\index_1.png','00'))
'''
run_in_another_thread2(me,main,main2,main3)
但是经过测试，一般函数都可以，就是有窗口的就是不行。
'''
def run_in_another_thread2(*args):
    class myThread (threading.Thread):
        def __init__(self,args,i):
            threading.Thread.__init__(self)
            self.fun=args[i]
        def run(self):
            self.fun()
    '''
    注意，用了li的池子之后反而走不动！
    '''
    for i in range(0, len(args)):
        t = myThread(args, i)
        t.start()
    '''
    li=[]
    for i in range(0,len(args)):
        t=myThread(args,i)
        li.append(t)
        t.start()
    for t in li:
        t.join()
    '''
def shasi_jincheng2(s):
    try:
        command = 'taskkill /F /IM '+s
        os.popen(command)
    except:
        pass
def zuihou_lujing(s):
    s=s.replace('\\','/').replace('//','/')
    return s.split('/')[-1]
#s='C:/Users/50310/Desktop/暂存/新建文件夹 (2)/2019年12月宝丰发票(1).pdf'
def bendi_cunchu(path,s):
    if not os.path.exists(path):
        writefilea('',path)
    #注意不能带有@符号。
    r=readfile(path)
    mima = 'ANfjjg7hyfvJa5ZfkViRXP46kwhzRfYp'
    if r:
        r = aes_jiemi(r, mima)
    l=r.split('#@#')
    l2=s.split('@')
    zhaodao=0
    mima = 'ANfjjg7hyfvJa5ZfkViRXP46kwhzRfYp'
    for i in range(0,len(l)):
        i1=l[i].split('@')
        if l2[0]==i1[0]:
            zhaodao=1
            l[i]=s
            k = '#@#'.join(l)
            print(k)
            k=aes_jiami(k,mima)
            writefile(k, path)
            continue
    if zhaodao==0:
        l.append(s)
        k = '#@#'.join(l)
        print(k)
        k = aes_jiami(k, mima)
        writefile(k, path)

#bendi_cunchu('resources/super.dat','niyou5@567')
#bendi_cunchu('resources/super_config.dat','niyou2:247')
def bendi_quchu(path,s):
    #注意不能带有@和:符号。
    r=readfile(path)
    mima = 'ANfjjg7hyfvJa5ZfkViRXP46kwhzRfYp'
    if r:
        r = aes_jiemi(r, mima)
    l=r.split('#@#')
    zhaodao=0
    for i in range(0,len(l)):
        i1=l[i].split('@')
        if s==i1[0]:
            zhaodao=1
            return i1[1]
            continue
    if zhaodao==0:
        return '没有找到key值！'
#k=bendi_quchu('resources/super.dat','niyou3')
#print(k)
'''
def pinyin(word,num=-1):
    s = ''
    for i in pypinyin.pinyin(word, style=pypinyin.NORMAL):
        s += ''.join(i)
    if num==-1:
        return s
    else:return s[num]
'''

def duan(s='999999'):
    if s!='999999':
        time.sleep(int(s))
    else:
        time.sleep(999999)

def jiexi_gzip(file_path):
    s=readfile(file_path).replace("\n","").replace("\r","")
    '''
    1f8b开头，直接解析gzip
    '''
    if s[:5]=="1f8b":
        b = b"".fromhex(s)
        data = gzip.decompress(b)
        try:
            data = str(data, encoding="gbk")
        except:
            data = str(data, encoding="utf-8")
        return data
        '''
        FTP协议的开头，分段
        '''
    else:
        k=0
        while k> -1:
            k = s.find("402343")
            if k==-1:
                break
            s=s[:k]+s[k+108:]
        b = b"".fromhex(s)
        data = gzip.decompress(b)
        try:
            data = str(data, encoding="gbk")
        except:
            data = str(data, encoding="utf-8")
        return data
def printl(s):

    pass
    '''
    a = str(threading.current_thread().getName())
    print(s)
    writefilea(str(s)+'\n',"第%s条线程.txt"%a)
    '''
def dangqian_xiancheng():
    a = str(threading.current_thread().getName())
    return a
print(dangqian_xiancheng())
    


'''
注意，下面这个方法把1234的string转为b'1234'，但是\u4eba会变成\\u4eba,并且要注意传入的字符最好前面加一个r'1234'
'''
def tianjia_b(s):
    hex1 = ''.join([hex(ord(c)).replace('0x', '') for c in s])
    b = b''.fromhex(hex1)
    return b
def qudiao_b(b):
    s=b.decode()
    return s
def b64_jiami(s):
    k=s.encode('utf-8')
    k1 = base64.b64encode(k)
    k2=qudiao_b(k1)
    return k2
def b64_jiemi(s):
    k=s.encode('utf-8')
    k1 = base64.b64decode(k)
    k2=qudiao_b(k1)
    return k2
def trytrytry(fun,times=3,*args):
    if args:
        fun2=args[0]
    for i in range(1,times+1):
        try:
            a=fun()
            break
        except Exception as e:
            if args:
                fun2()
            print('第%s次函数运行失败'%str(i)+str(e))
            pass
    return a

def jiexi_headers(f):
    k=readfile(f)
    l=k.split('\n')
    dict={}
    for i in l:
        dict[i.split(':')[0].strip()]=i.split(':')[1].strip()
    print(dict)
    return dict
def duibi(path1,path2):
    r1=readfile(path1)
    l1=r1.split('\n')
    r2=readfile(path2)
    l2 = r2.split('\n')
    length=min(len(l1),len(l2))
    l_butong = []
    for i in range(1,length+1):
        if l1[i-1]!=l2[i-1]:
            l_butong.append(i)
    print(l_butong)
#duibi(r'C:\Users\50310\Desktop\python_document2\ifind主程序测试\mytool_tcp.py',r'C:\Users\50310\Desktop\python_document2\ifind程序\tcp_ifind.py')
#bendi_cunchu('fapiao_pkg/resources/super_config.dat','haomamingming@1')

# r = open(r'D:\iFinD1' + r'/users/UsersData.dat','rb')
# print(r.read())
# writefile('123','123/123.txt')

#js_list=['base64.js','jquery-1.10.2.min.js','jquery.PrintArea.js','jquery.alerts.js','jquery.md5.js','showModalDialog.js','aes.js','pbkdf2.js','AesUtil.js','common.js','validate.js','result.js','bootstrap-datepicker.js','bootstrap-datepicker.zh-CN.min.js','emwrs.js','urmqn.js','wlop.js','92da1b9c13d7432c8eae5aa66e641262.js','eab23.js','indexfunc.js','90a1c.js','gunScanner.js']
def js_xiazai(zhuzhan,js_list,path):
    s = requests.Session()
    headers = {'Accept': 'application/javascript, */*;q=0.8', 'Referer': 'https',
             'Accept-Language': 'zh-Hans-CN,zh-Hans;q=0.5', 'Accept-Encoding': 'gzip, deflate',
             'Connection': 'close', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv'}
    for i in js_list:
        res = s.get(zhuzhan+i, headers=headers,verify=False)
        writefile(res.text,path+i)

def zhengze_tidai(s,reg,s1,need_print=False):
    while True:
        k=zhengze(s,reg)
        for i in range(1,len(k)+1):
            j=len(k)-i
            if need_print:
                print(s[k[j][0][0]:k[j][0][1] + 1])
            s = s[:k[j][0][0]] + s1 + s[k[j][0][1] + 1:]
        return s

def zuihou_mulu(path):
    k1=xiuzheng_mulu(path)
    k2=shangji_mulu(path)
    return k1[len(k2)+1:]

def zhuan_daoxu(K):
    panding = b64_encode(b'{"key1":"iVBORw0KGgoAAAANSUhEUgAAAFoAAAAjCAIAAA')
    '''生成间隔'''
    for j in range(0,len(panding)):
        if panding[j]!=K[j] and j!=0:
            jiange=j
            break
    '''开始倒序替换'''
    k = ''
    for i in range(0,len(K)):
        c=K[i]
        if is_zimu(c) and i%jiange==0:
            if c.upper()==c:
                c=chr(90-(ord(c)-65))
            else:c=chr(122-(ord(c)-97))
        if is_shuzi(c) and i%jiange==0:
            c=str(9-int(c))
        k=k+c
    k = b64_decode(k)
    k = qudiao_b(k)
    return k


def suiji_shuzizimu(num):
    passwd = []
    letters = string.ascii_letters + string.digits
    length = len(letters)
    for i in range(num):
        letter = letters[random.randint(0,length - 1)]
        passwd.append(letter)
    return "".join(passwd)

def jieya(path):
    f = zipfile.ZipFile(path, 'r')
    for file in f.namelist():  # f.namelist()返回列表，列表中的元素为压缩文件中的每个文件
        f.extract(file, shangji_mulu(path))


def string_zhuan_shijian(s):
    try:
        s=s.strip()
        time=datetime.datetime.strptime(s, '%Y-%m-%d %H:%M:%S')
    except:
        time = datetime.datetime.strptime(s, '%Y-%m-%d')
    return time
def shijian_zhuan_string(d):
    #s = datetime.datetime.strftime(d)
    s=str(d)
    return s
# t1=string_zhuan_shijian('2020-09-19')
# t2=string_zhuan_shijian('2020-09-09')

def jizhang(i,j,txt):
    jine=0
    date_i=string_zhuan_shijian(i)
    date_j = string_zhuan_shijian(j)
    a = run_cloud("print_csv", "please print_csv@%s"%txt)
    b=a.strip().split('\n')
    for k in b:
        amount=zhengze(k,r"'buyer_pay_amount': '(.*?)'")[0][0][2]
        date=zhengze(k,r"'send_pay_date': '(.*?)'")[0][0][2]
        date_jiaoyi=string_zhuan_shijian(date)
        if date_i<date_jiaoyi and date_j>date_jiaoyi:
            print(shijian_zhuan_string(date_jiaoyi)+'  支付金额：'+amount)
            jine=jine+float(amount)
    print('总计支付金额：'+str(jine))
    return jine
def wenjian_daxiao(path,moshi):
    if moshi=='kb':
        return os.path.getsize(path)/1024
    if moshi=='mb':
        return os.path.getsize(path) / 1024/1024
    return os.path.getsize(path)

#
# im_path=r"C:\Users\50310\Desktop\untitled.png"
# k=tupian_to_b64(im_path)
#
# start = time.clock()
# for i in range(10):
#     print(i)
#     run_cloud2('shibie3', k + '@黑')
#     #tujian_origin(im_path)
# elapsed = (time.clock() - start)
# print(elapsed)






