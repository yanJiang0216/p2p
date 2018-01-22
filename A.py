from socket import *
from threading import *
from time import sleep,ctime
import atexit
import tkinter as tk
class MyThread(Thread):
    def __init__(self,func,name=''):
        Thread.__init__(self)
        self.name=name
        self.func = func
    def run(self):
        self.func()
ss = socket(AF_INET,SOCK_STREAM,0)
ss.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
ss.bind(('192.168.2.112',8002))
ss.listen(5)

###########################UI
root = tk.Tk()
root.geometry('950x500')
root.title("dialog")
frame =tk.Frame(root)
frame.pack()
text1 = tk.Text(root,width=100,height = 15)
text1.pack(fill=tk.X) 
text2 = tk.Text(root,width=40,height = 2)
text2.pack(fill=tk.Y,side=tk.LEFT)
def send():
    cs = socket(AF_INET,SOCK_STREAM,0)
    cs.connect(('192.168.2.121',8001))
    data = text2.get('0.0','end')
    print(data)
    cs.send('m'.encode('utf-8'))
    cs.send(data.encode('utf-8'))
    cs.close()
sendButton1 = tk.Button(root,text='Send Message',command=send,width=20).pack(\
                        fill=tk.Y,side=tk.LEFT)
text3= tk.Text(root,width=40,height = 2)
def sendFile():
    cs = socket(AF_INET,SOCK_STREAM,0)
    cs.connect(('192.168.2.121',8001))
    path = text3.get('0.0','end')
    i=path.rfind('\\')
    i+=1
    fileName=path[i::]
    print('KK'+fileName)
    cs.send('f'.encode('utf-8'))
    cs.send(fileName.encode('utf-8'))
    sleep(0.5)
    with open(path[:-1:],'rb') as f:
        for data in f:
            cs.send(data)
    cs.close()
    # text3.delete('0.0',tk.END)
    # text3.insert(tk.END,'finished!')
sendButton2 = tk.Button(root,text='Send file',width=20,command=sendFile).pack(\
              fill=tk.Y,side=tk.RIGHT)
text3.pack(fill=tk.Y,side=tk.RIGHT) 
text3.pack()
def receive():
    while True:
        cs,addr = ss.accept()
        ip,port=addr
        text1.insert(tk.END,"\nconnect from: "+ip)
        recv = cs.recv(1)
        print(recv)
        c = recv.decode('utf-8')
        print(c)
        if c== 'm':
            text1.insert(tk.END,'\nreceived message: ')
            while True:
                data = cs.recv(1024)
                if not data:
                    break
                else:
                    text1.insert(tk.END,data.decode('utf-8'))           
        elif c == 'f':
            text1.insert(tk.END,'\nreceived file: ')
            name = cs.recv(1024)
            while True:
                data = cs.recv(255)
                if not data:
                    break
                else:
                    with open('.\\'+name.decode('utf-8')[:-1:],'ab') as f:
                        f.write(data)
                text1.insert(tk.END,'\n'+name.decode('utf-8')[:-1:]+'\nafter receiving and saving!')
        else:
            break
# @atexit.register
# def clearResource():
#     ss.close()
#     cs.close()
#     print("done!")

def main():
    text1.insert(tk.END,ctime())
    receiveThread = MyThread(receive,receive.__name__)
    receiveThread.start()
    root.mainloop()
    #receiveThread.join()    
if __name__ == '__main__':
    main()

    


