# _*_ coding: utf-8 _*_
from MSP430 import MSPComm
import socket
import time
import threading
import serial.tools.list_ports
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from objs import OBJ
import math
import icp
import numpy as np
from  matplotlib import pyplot as plt
import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import NearestNeighbors

def serialRead():
    serialDict = []
    serialNum = 0
    ports = list(serial.tools.list_ports.comports())
    for a, b, c in ports:
        # print(a,b,c)
        d = a.split('.')
        if d[-1] != 'Bluetooth-Incoming-Port':
            # print (d[-1])
            serialDict.append(a)
            serialNum += 1
    return serialNum, serialDict


class FetchData:
    def __init__(self, msp):
        self.msp = msp
        # second
        self.send_time = 0.1
        self.mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.mysocket.connect(("localhost", 8002))
        # need to renew everytime
        self.r = 4
        self.c = 6
        self.data = []
        self.datanumers = 0
        self.sumcoils = 24
        self.channel = 32
        self.mapping = [] # used for match the id and coils
        for i in range(self.channel):
            self.mapping.append(i)


        # these parameters use for process coils data
        self.t = 10  # parameter (array resize factor)
        self.rows = (self.r - 1) * self.t  # height of the heat map
        self.cols = (self.c - 1) * self.t  # width of the heat map

        self.coil_array = np.zeros((self.r, self.c))
        self.interp_array = np.zeros((self.rows, self.cols))
        self.binary_array = self.interp_array
        self.edge_array = self.interp_array
        self.only_edge_array = [[], []]
        self.icp_medal=[[],[]]
        self.icp_data=[[],[]]
        self.peak = [0]*40
        self.high = 1
        self.low = 0
        self.tempthreshold=1




    def sender(self):

        while 1:
            data, base = self.fetch_ch_data()
            ch = []
            for i in range(self.channel):
                if((i+1)%4!=0):
                    ch.append(data[i]-base[i])
            # print ch
            self.mysocket.send(' '.join(str(e) for e in ch) + "\n")
            #self.data.append(ch)
            #self.datanumers = self.datanumers + 1
            # self.mysocket.send('100' + '\n')

            time.sleep(self.send_time)

    def print_on_console(self):
        while 1:
            data, base = self.fetch_ch_data()
            ch = []
            for i in range(len(data)):
                ee = data[i]-base[i]
                if ee > self.peak[i]:
                    self.peak[i] = ee
                ch.append(ee)
            self.data.append(ch)
            print self.data[self.datanumers]
            for y in range(self.r):
                for x in range(self.c):
                    self.coil_array[y][x]=ch[self.mapping[y*self.c+x]]
            self.bilinear_interpolation()
            self.binary_image()

            self.edge_detection()
            time.sleep(0.1)
            status = raw_input('m or d or s')
            if status == 'm':
                self.icp_medal = self.only_edge_array
            elif status == 'd':
                self.icp_data=self.only_edge_array
            elif status == 's':
                self.icp_show()
            elif status == 'r':
                for submsp in mymsp:
                    submsp.reset_base() 
    def icp_show(self):
        b=np.array(self.icp_medal)
        a=np.array(self.icp_data)
        M2 = icp.icp(a, b, [0.1, 0.33, np.pi / 2.2], 30)
        # Plot the result
        src = np.array([a.T]).astype(np.float32)
        res = cv2.transform(src, M2)
        plt.figure()
        # plt.plot(b[0], b[1], 'g')
        # plt.plot(res[0].T[0], res[0].T[1], 'r.')
        # plt.plot(a[0], a[1], 'b')
        plt.scatter(b[0],b[1])
        plt.scatter(res[0].T[0], res[0].T[1])
        plt.scatter(a[0], a[1])
        plt.show()

    def drawimage(self):# not to be used right now
        # plt.figure(figsize=(8,8))
        plt.figure()
        plt.ion()
        while 1:
            singlecoildata = np.array(self.data)
            for r in range(self.r):
                for c in range(self.c):
                    axi = plt.subplot2grid((self.r, self.c), (r, c), colspan=1, rowspan=1)
                    axi.plot([0, self.datanumers], singlecoildata[:self.datanumers, self.c * r + c],
                             'r')  # can be replaced by my function
            plt.pause(0.1)

    def fetch_ch_data(self):
        data = [0] * self.channel
        base = [0] * self.channel
        for j in range(self.channel):
            for i in range(10):  # extract 10 samples and then calculate the average each time.
                data[j] += self.msp[j/4].data_ch[j % 4]/10
                base[j] += self.msp[j/4].base_ch[j % 4]/10
            time.sleep(0.001)
        return data, base

    # transform the grayimage into binary image through a threshold
    def binary_image(self) :
        print ('hello word')
        self.binary_array=self.interp_array
        for y in range(self.rows):
            for  x in range(self.cols):
                if self.binary_array[y][x]< self.tempthreshold:
                    self.binary_array[y][x]=self.low
                else:
                    self.binary_array[y][x]=self.high

    # detect the edge of a binary image
    def edge_detection(self):
        self.only_edge_array=[[], []]
        for y in range(1,self.rows-1):
            for x in range(1,self.cols-1):
                if self.binary_array[y][x] == self.high and self.mask(y, x) == self.high:
                    self.edge_array[y][x] == self.high
                    self.only_edge_array[0].append(y)
                    self.only_edge_array[1].append(x)
                else:
                    self.edge_array[y][x] == self.low

    def mask(self,y,x):
        maskvalue = self.binary_array[y - 1][x] + self.binary_array[y - 1][x + 1] + self.binary_array[y - 1][x - 1] +self.binary_array[y][x + 1] + self.binary_array[y][x - 1] +self.binary_array[y + 1][x] + self.binary_array[y + 1][x + 1] + self.binary_array[y + 1][x - 1];
        if maskvalue < 8*self.high and maskvalue >= 1*self.high:
            return self.high
        else:
            return self.low

    def bilinear_interpolation(self):
        # add the original coils data into new array
        for i in range(self.r):
            for j in range(self.c):
                x = j * self.t - 1
                y = i * self.t - 1
                if x<0:
                    x=0
                if y<0:
                    y=0
                self.interp_array[y][x] = self.coil_array[i][j]

        # calcaulate the interpolation value and add
        for y in range(self.rows):
            dy1 = int(math.floor(y/(self.t*1.0)))
            dy2 =int( math.ceil(y / (self.t * 1.0)))
            y1 = dy1*self.t-1
            y2 = dy2 * self.t - 1
            if y1 < 0:
                y1 = 0
            if y2 < 0:
                y2 = 0
            for x in range(self.cols):
                dx1 = int(math.floor(x / (self.t * 1.0)))
                dx2 = int(math.ceil(x / (self.t * 1.0)))
                x1 = dx1 * self.t - 1
                x2 = dx2 * self.t - 1
                if x1 <0:
                    x1=0
                if x2 <0:
                    x2=0
                q11 = self.coil_array[dy1][dx1]
                q12 = self.coil_array[dy2][dx1]
                q21 = self.coil_array[dy1][dx2]
                q22 = self.coil_array[dy1][dx1]

                count =0
                if q11 >0:
                    count=count+1
                if q12 >0:
                    count = count + 1
                if q21>0:
                    count = count + 1
                if q22 >0:
                    count = count + 1

                if count > 2:
                    if not (y1==y2 and x1 == x2):
                        t1 = (x - x1)
                        t2 = (x2 - x)
                        t3 = (y - y1)
                        t4 = (y2 - y)
                        t5 = (x2 - x1)
                        t6 = (y2 - y1)
                        if y1 == y2:
                            self.interp_array[y][x] = q11 * t2 / t5 + q21 * t1 / t5
                        elif x1 == x2:
                            self.interp_array[y][x] = q11 * t4 / t6 + q12 * t3 / t6
                        else:
                            diff = t5*t6
                            self.interp_array[y][x] = (q11 * t2 * t4 + q21 * t1 * t4 + q12 * t2 * t3 + q22 * t1 * t3) / diff
                    else:
                        self.interp_array[y][x] = q11
                else:
                    self.interp_array[y][x]=0


    def data_collection(self, participant):
        """
        data format:
        #participant, raw_code[0..4], base[0..4], correct_obj
        """

        objs = OBJ()
        data_list = list()
        for obj in objs.names:
            print("target data: " + obj)
            for i in range(5):
                raw_input("press ENTER to begin trial {} >>".format(i))
                data, base = self.fetch_ch_data()

                line = str(participant) + ","
                for d in data:
                    line += str(d) + ","
                for b in base:
                    line += str(b) + ","
                line += str(OBJ().id[obj]) + "\n"
                print str(i)+': '+line
                data_list.append(line)

        filename = "data/" + str(participant) + ".csv"
        f = open(filename, "w")
        for line in data_list:
            f.write(line)
        f.close()
        print("writen to file " + filename)

    def start(self):
        t = threading.Thread(target=self.sender, args=())
        t.start()

        # it's too slow
        #realimage = threading.Thread(target=self.drawimage, args=())
        #realimage.start()

        #reset_bases = threading.Thread(target=self.resetbase, args=())
        #reset_bases.start()
        print 'reset start'

        print_inductance=threading.Thread(target=self.print_on_console, args=())
        print_inductance.start()


    def resetbase(self) :
        while 1:

            base_flat=raw_input("reset?")
            if base_flat == 'r':
                for submsp in mymsp:
                    submsp.reset_base()
                print 'reset succeed'
            elif base_flat == 'q':
                break
            else:
                print "type again"
            time.sleep(0.1)

if __name__ == "__main__":
    mymsp = list()
    serialNums, serialDicts = serialRead()
    serialDicts.sort()    
    print serialNums, serialDicts
    serialID = 0
    for COM in serialDicts:
        serialID += 1
        mymsp.append(MSPComm(COM,  str(serialID)))


    fetchdata = FetchData(mymsp)
    fetchdata.start()
    #fetchdata.data_collection(2)  # args=(list of msp, # of participant)

