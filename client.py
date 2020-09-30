
# task_worker.py
import os
import time, sys, queue
from multiprocessing.managers import BaseManager

import subprocess
import sys
import threading

from pkg.cmdcolor import *

client_name = 'S_'
name = os.environ.get("COMPUTERNAME")

client_name = client_name + name


printDarkGreen(f'        客户端启动中.. {client_name}')

class MyException(Exception):
    def __init__(self,message):
        Exception.__init__(self)
        self.message=message    

class MyException2(Exception):
    def __init__(self,message):
        Exception.__init__(self)
        self.message=message        
        
def build_return_list(str_1,str_2,color_):
    list_ = []
    list_.append(str_1)
    list_.append(str_2)
    list_.append(color_)
    return list_


def run_cmd_code(str_):
    
    # 执行命令
    #print(f'str ==={str_}')
    #sp = subprocess.Popen(str_, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE,bufsize=1) #universal_newlines=True,
    sp = subprocess.Popen(str_, shell=True, stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=1) #错误重定向至标准输出，获取返回值再处理
    while 1:
        run_result = sp.stdout.readline()
        #print(f'str ==={sp.poll()}')
        #print(f'str ==={run_result}')
        if sp.poll() is (not None) :
            break
        if run_result == b'':
            break
        #print(sp.poll())
        run_result_ = run_result.decode('gbk')


        #打印标准输出
        print(run_result_)
        #sys.stdout.flush()
        

        #标准输出至控制台
        
        return_list = build_return_list(run_result_,client_name,0)
        result.put(return_list)
        
        sys.stdout.flush()
        #sys.stdout.flush()
        
        #result.put(f'                        ----FROM {client_name}')
        #sys.stdout.flush()
        
        #time.sleep(1)
    returncode = sp.wait()
    if returncode:
        raise subprocess.CalledProcessError(returncode,sp)
    return sp.poll()
def stdoutprocess(o):
   while 1:
      stdoutdata = o.stdout.readline()
      if stdoutdata:
         sys.stdout.write(stdoutdata)
      else:
         break

# 创建类似的QueueManager:
class QueueManager(BaseManager):
    pass

# 由于这个QueueManager只从网络上获取Queue，所以注册时只提供名字:
QueueManager.register('get_task_queue')
QueueManager.register('get_result_queue')

# 连接到服务器，也就是运行task_master.py的机器:
server_addr = '192.168.IP'
print('Connect to server %s...' % server_addr)
# 端口和验证码注意保持与task_master.py设置的完全一致:
m = QueueManager(address=(server_addr, 5000), authkey=b'yourpass')
# 从网络连接:
m.connect()
# 获取Queue的对象:
task = m.get_task_queue()
result = m.get_result_queue()
# 从task队列取任务,并把结果写入result队列:
while 1:
    try:
        n = task.get(timeout=1)
        printYellow(f'        running task... ')
        #print(n)
        sys.stdout.flush()
        r = n
        #print(r)
        time.sleep(0.5)
        for i in r:
            #print(i)
            #time.sleep(10.5)
            back_massage_ = build_return_list(i,client_name,1)
            result.put(back_massage_)
            if i =="exit":
                raise MyException("Exit...")
            if i =="endterminal":
                raise MyException2("End terminal...")
            sys.stdout.flush()
            run_cmd_code(i)
            sys.stdout.flush()
            time.sleep(5)
    except queue.Empty:
        printDarkGreen('task queue is empty. try again after 200s')
        time.sleep(200)
    except MyException:
        printDarkGreen('exit,try again agter 410s')
        time.sleep(410)
    except MyException2:
        printYellow('terminal end, close after 20s')
        time.sleep(20)
    except KeyboardInterrupt :
        print("KEY INTERRUPT")
        task.put(n)
        printRed(str(n))
        return_list = build_return_list("Key_Interrupt",client_name,2)
        result.put(return_list)
        printRed("队列执行错误，已返回队列Queue")
        time.sleep(5)
        break
    except Exception as e :
        print(e)
        task.put(n)
        printRed(str(n))
        return_list = build_return_list(str(e),client_name,2)
        result.put(return_list)
        printRed("队列执行错误，已返回队列Queue")
        break
# 处理结束:
print('worker exit.')
