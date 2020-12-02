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
import signal
import copy
import datetime
import pytz
import base64

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
    f=codecs.open(file, 'w',encoding=encoding)
    f.write(str(string.encode(encoding, 'ignore'), encoding=encoding))
    f.close()
def writefilea(string,file,encoding='gbk'):
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


def isshuzi(s):
    inside_code=ord(s)
    if inside_code > 47 and inside_code <= 57:
        return True
    else:
        return False
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
            print('删除文件失败')
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
    if show_state:print('总大小：' + str(round(contentLength / 1024 / 1024, 2)) + " mb")
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
        delete(filePath)
        os.rename(filePath + '.tmp', filePath)

    if show_state:print('下载完成！')
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
def zhengze(string,reg_str,return_type='span'):
    #return_type='span' 返回很多个[1,2] 前面是一个匹配的start，后面是end
    #return_type='start'返回[2,5,7,23] 所有匹配的start
    # return_type='end'返回[2,5,7,23] 所有匹配的end
    
    s=string
    arr=[]
    cut_index=0
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
def beijing_shijian():
    r = requests.get('http://time.tianqi.com/')
    r_shijian = zhengze(r.text, '北京现在时间：([^。]*)。')
    k=r_shijian[0][0][2]
    da=datetime.datetime.strptime(k,'%Y-%m-%d %H:%M:%S')
    return da
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