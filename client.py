
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


server_addr = '172.16.YOURIP'
server_port = 5000
server_authkey = b'yourpass'


printDarkGreen(f'        客户端启动中.. {client_name}')




def build_return_list(str_1,str_2,color_):
    list_ = []
    list_.append(str_1)
    list_.append(str_2)
    list_.append(color_)
    return list_


def run_cmd_code(str_):
    
    # 执行命令
    sp = subprocess.Popen(str_, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE,bufsize=1) #universal_newlines=True,

    while 1:
        run_result = sp.stdout.readline()
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

print('Connect to server %s...' % server_addr)



# 端口和验证码注意保持与task_master.py设置的完全一致:
while 1:
    try:
        m = QueueManager(address=(server_addr, server_port), authkey=server_authkey)
        # 从网络连接:
        m.connect()
        # 获取Queue的对象:
        task = m.get_task_queue()
        result = m.get_result_queue()
        break
    except:
        printDarkRed(f'        连接服务器{server_addr}:{server_port}失败...120s后重试')
        time.sleep(120)
        
# 从task队列取任务,并把结果写入result队列:
while 1:
    try:
        n = task.get(timeout=1)
        printDarkYellow(f'        running task... ')
        print(n)
        sys.stdout.flush()
        r = n
        
        time.sleep(0.5)
        for i in r:
            back_massage_ = build_return_list(i,client_name,1)
            result.put(back_massage_)
            sys.stdout.flush()
            run_cmd_code(i)
            sys.stdout.flush()
            time.sleep(5)
    except queue.Empty:
        printDarkGreen('task queue is empty. try again after 20s')
        time.sleep(20)
# 处理结束:
print('worker exit.')