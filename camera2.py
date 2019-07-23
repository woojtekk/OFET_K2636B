import cv2
import time
import threading
import numpy as np

class cammera2():
    
    lum=0
    xxx=0
    w=0
    h=0
    z=0
    stop_threads=False
    
    def __init__(self):
        print("------ cam init ------")
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Could not open video device")
            self.stop_threads=True
            
        self.cap.set(cv2.CAP_PROP_EXPOSURE, -1)
        # cv2.namedWindow('frame', cv2.WINDOW_NORMAL)

    def run(self):
        t1 = threading.Thread(target=self.f1)
        t1.start()
        
        
    def f1(self):
        ret, fr = self.cap.read()
        w,h,z  = fr.shape
        self.w=int(w/2)
        self.h=int(h/2)
        self.z=z
        dd=50
        
        while( True ):
            ret, fr = self.cap.read()

            if self.stop_threads: break
            if not ret: break
            
            fr2=fr[(self.w-dd):(self.w+dd),(self.h-dd):(self.h+dd)]

            cv2.rectangle(fr,(self.h-dd,self.w-dd),(self.h+dd,self.w+dd),(0,255,0),1)

            
            
            gray = cv2.cvtColor(fr2, cv2.COLOR_BGR2GRAY)
            gray2 = cv2.GaussianBlur(gray, (11, 11), 0)


            fr[0:dd*2,0:dd*2]=fr2
            
   
            self.lum=cv2.minMaxLoc(gray2)[1]
            
            cv2.imshow("frame", fr)
            cv2.imshow("frame2", gray2)


            cv2.waitKey(1)

        self.cap.release()
        cv2.destroyAllWindows()
        
    def stop(self):
        print("----cam stop-----")
        self.stop_threads=True
        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    d = cammera2()
    d.run()
    x = 0
    while (x <= 200):
        print("::",x, d.lum,d.xxx)
        d.xxx = d.xxx+2
        x += 1
        time.sleep(0.5)
    d.stop()

    