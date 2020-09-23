
# task_worker.py


 

import random,time,queue
import time, sys, queue
from multiprocessing.managers import BaseManager
from pkg.cmdcolor import *


# 创建类似的QueueManager:
class QueueManager(BaseManager):
    pass

# 由于这个QueueManager只从网络上获取Queue，所以注册时只提供名字:
QueueManager.register('get_task_queue')
QueueManager.register('get_result_queue')

# 连接到服务器，也就是运行task_master.py的机器:
server_addr = '172.16.yourIP'
printDarkGreen('Connect to server %s...' % server_addr)
# 端口和验证码注意保持与task_master.py设置的完全一致:
m = QueueManager(address=(server_addr, 5000), authkey=b'yourpass')




# 从网络连接:
m.connect()
# 获取Queue的对象:
task = m.get_task_queue()
result = m.get_result_queue()
# 从task队列取任务,并把结果写入result队列:

def build_list():
    cmd = []
    command_1 = 'python C:\PythonProjects\PythonProjects\main.py killTJ'
    cmd.append(command_1)
    command_2 = 'python C:\PythonProjects\PythonProjects\main.py beginTJ -inout discharged --department ortho4'
    cmd.append(command_2)
    command_3 = 'python C:\PythonProjects\PythonProjects\main.py paninfo_discharged  -r --startpage 0 --wholepage 8'
    cmd.append(command_3)
    #print(cmd)
    return cmd
 
 
def build_list2(n_,partment_):
    cmd = []
    command_1 = 'python C:\PythonProjects\PythonProjects\main.py killTJ'
    cmd.append(command_1)
    command_2 = f'python C:\PythonProjects\PythonProjects\main.py beginTJ -inout discharged --department ortho{partment_}'
    cmd.append(command_2)
    command_3 = f'python C:\PythonProjects\PythonProjects\main.py paninfo_discharged --startpage {n_*40} --wholepage {40} -db Y:\dic\ '
    cmd.append(command_3)
    #print(cmd)
    return cmd
 
#"endterminal" 结束终端

def update_files():
    cmd = ["copy y:\dic\client.py C:\PythonProjects\PythonProjects /y ","exit"]
    return cmd

def kill_cmd():
    cmd = ["python C:\PythonProjects\PythonProjects\main.py killTJ","exit"]
    return cmd
 

#print(cmd)
'''
print(type(cmd))
for i in cmd:
    print(i)
    print(type(i))
exit()
'''


def upload_kill():

    for i in range(20):
        cmd = kill_cmd()
                
        task.put(cmd)
        print(cmd)
    time.sleep(1)

def upload2():

    for i in range(20):
        cmd = update_files()
                
        task.put(cmd)
        print(cmd)
    time.sleep(1)


def upload():
    for i in range(1):
        #try:

        #n = random.randint(0, 10000)
        printDarkGreen('Put task ')
        #task.put(n)
        #step = 20
        #for z in range(1,5):
        for x in range(0,3):
            for y in range(2,3):


                cmd = build_list2(x,y)
            
                task.put(cmd)
                print(cmd)
                printDarkYellow('uploaded')
                time.sleep(1)
        
        #except queue.Empty:
        #    print('task queue is empty.')
        #except:
        #    printRed('pass')
        #    print(cmd)
        #    pass

upload()
upload_kill()
printGreen('worker exit.')
# 处理结束:


exit()
for i in range(1,21):
    a = f'.\\vmrun.exe -T ws clone "C:\Virtual Machines\VCclient_template\VCclient_template.vmx" "C:\Virtual Machines\slaves\{i}\slave{i}.vmx" linked -snapshot=shot1 -cloneName=slave{i} '
    with open("C:\\out.txt", "a") as sob:
        sob.write(a+'\r\n')

for i in range(1,21):
    a = f'.\\vmrun.exe -T ws register "C:\Virtual Machines\slaves\{i}\slave{i}.vmx"'
    with open("C:\\out.txt", "a") as sob:
        sob.write(a+'\r\n')
exit()

for i in range(0,20):
    for j in range(1,5):
        print(f"i*8 = {i * 8 }  i = {i}    j = {j}")
 

exit()