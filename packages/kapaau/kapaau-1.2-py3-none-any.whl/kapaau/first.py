import cv2
import baiduasr
import keyboard
import socket
import threading
import time
from speak import speak
from FaceRecognition import Face
from prediction import showResult,remove_result,modelpre

socket_c1=''
socket_c2=''
data=''
def TCP_V():
    global data
    global socket_c1
    global socket_c2
    socket_c1=socket.socket()
    socket_c2=socket.socket()
    socket_c1.connect(('127.0.0.1',2001))
    socket_c2.connect(('127.0.0.1',2002))
    while 1:
        data=socket_c2.recv(1024).decode()
        print(data)
        time.sleep(0.1)
if __name__=='__main__':
    th1=threading.Thread(target=TCP_V)
    th1.setDaemon(1)
    th1.start()
    time.sleep(0.1)
    remove_result()
    speak('开始人脸识别')
    name,confidence=Face()
    confidence="{0}".format(round(250-confidence))
    print('你的名字：',name)
    print('匹配指数：',confidence)
    faceimg=cv2.imread('./image.jpg')
    cv2.imshow('image',faceimg)
    cv2.waitKey(3000)
    cv2.destroyAllWindows()
    speak('按下S键后开始语音识别')
    while 1:
        msg=''
        if keyboard.is_pressed('s'):
            print('下指令')
            baiduasr.record()
            h=baiduasr.asr_updata().split(',')
            print(h)
            for i in range(len(h)):
                if '第一' in h[i]:
                    msg='A'
                    print(msg)
                    socket_c1.send(msg.encode())
                elif '第二' in h[i]:
                    msg='B'
                    print(msg)
                    socket_c1.send(msg.encode())
                elif '第三' in h[i]:
                    msg='C'
                    print(msg)
                    socket_c1.send(msg.encode())
                elif '第四' in h[i]:
                    msg='D'
                    print(msg)
                    socket_c1.send(msg.encode())
                elif '管控' in h[i]:
                    msg='start'
                    print(msg)
                    socket_c1.send(msg.encode())
            speak('按下s键后再次语音识别')
        elif data=='ok':
            speak("推理中")
            src_roi=cv2.imread('D:/VisionMaster/image.jpg')
            label,pred_class=modelpre(src_roi)
            print(label,pred_class)
            showResult(src_roi,pred_class)
            if label==0:
                msg='fangbianmian'
            elif  label == 1:
                msg = 'fenda'
            elif  label == 2:
                msg = 'guantou'
            socket_c2.send(msg.encode())
            speak('识别结果是'+pred_class)
            data=''



                    



