#!/root/anaconda3/bin/python3
import sys
import os
import json
import pandas as pd
import numpy as np
import optparse
import time
import datetime
import pytz
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from mpl_toolkits.mplot3d import Axes3D
from keras.models import Sequential, load_model
from keras.preprocessing import sequence
from keras.preprocessing.text import Tokenizer
from collections import OrderedDict
def read_log(path):
        #'predict_data.txt'为用于预测的实际数据，在当前路径下
       # if path.split('/')[-1] == 'access.log':
        dataframe = pd.read_table(path, sep=' ', header=None,
                                          names=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13'],
                                          dtype = {'1': str, '2': str, '3': str, '4': str, '5':str, '6': int, '7': float,
                                                   '8': int})
        dataset = dataframe.sample(frac=1).values
        info = np.array(dataset)
        b = []
        for x in info:
                b.append(list(x))
        b = np.array(b)
        return b

def utc2timestamp(utc_matrix):
        timeStamp = []
        for x in utc_matrix:
                x = x[0] + ' ' + x[-1]
                timeArray = datetime.datetime.strptime(x, "%d/%b/%Y:%H:%M:%S %z")
                timeStamp.append([int(time.mktime(timeArray.astimezone(pytz.utc).timetuple()))])
        timestamp_matrix = np.array(timeStamp)
        return timestamp_matrix

def ip2bina(ip_matrix):
        matrix = np.zeros((1, 32))
        for ip in ip_matrix:
                temp = []
                for i in ip.split('.'):
                        binary = bin(int(i))[2:].zfill(8)
                        for b in binary:
                                temp.append(int(b))
                matrix = np.row_stack((matrix, np.array(temp)))
        matrix = np.delete(matrix, 0, 0)

        return matrix

def bool2bina(axis, bool_matrix):
        tmp = np.zeros((1, axis))
        #遍历矩阵
        for x in bool_matrix:
                if str(x)[0] == '2':
                        tmp = np.row_stack((tmp, [1, 0, 0, 0]))
                elif str(x)[0] == '3':
                        tmp = np.row_stack((tmp, [0, 1, 0, 0]))
                elif str(x)[0] == '4':
                        tmp = np.row_stack((tmp, [0, 0, 1, 0]))
                elif str(x)[0] == '5':
                        tmp = np.row_stack((tmp, [0, 0, 0, 1]))
        tmp = np.delete(tmp, 0, 0)
        return tmp

def cookie2bina(axis, cookie_matrix):
        tmp = np.zeros((1, axis))
        for x in cookie_matrix:
                if x == "":
                        tmp = np.row_stack((tmp, [1, 0]))
                else:
                        tmp = np.row_stack((tmp, [0, 1]))
        tmp = np.delete(tmp, 0, 0)
        return tmp

def completion2bina(axis, compt_matrix):
        tmp = np.zeros((1, axis))
        for x in compt_matrix:
                if x == "":
                        tmp = np.row_stack((tmp, [1, 0]))
                else:
                        tmp = np.row_stack((tmp, [0, 1]))
        tmp = np.delete(tmp, 0, 0)
        return tmp

#输入数据归一化
#求出matrix矩阵在axis=0即列方向的最大值和最小值
def normalize(num_matrix):
        amax = np.apply_along_axis(np.max, 0, num_matrix)
        amin = np.apply_along_axis(np.min, 0, num_matrix)
        #遍历元素，求出归一化数值
        for j in range(num_matrix.shape[1]):
                for i in range(num_matrix.shape[0]):
                        num_matrix[i, j] = (num_matrix[i, j] - amin[j]) / (amax[j] - amin[j])
        return num_matrix
#
def conn_matx(num_matrix, bool_matrix, ip_matrix, timestamp_matrix, compt_matrix, cookie_matrix):
        matrix = np.hstack((num_matrix, bool_matrix, ip_matrix,
                            timestamp_matrix, compt_matrix, cookie_matrix))
        return matrix

#合成矩阵维度	
def add_dimension(matrix):
        ti = []
        for i in matrix:
                temp_list = []
                for j in i:
                        temp_list.append([j])
                ti.append(np.array(temp_list))
        return ti

def matp(data, prediction):
        C = []
        fig = plt.figure(figsize=(15,7.5))
        ax = fig.add_subplot(111, projection='3d')
        type0_x = []
        type0_y = []
        type0_z = []
        type1_x = []
        type1_y = []
        type1_z = []
        type2_x = []
        type2_y = []
        type2_z = []
        type3_x = []
        type3_y = []
        type3_z = []
        type4_x = []
        type4_y = []
        type4_z = []

        for x in range(len(prediction)):
                if(prediction[x][-1] > 0.45):
                        sub = 4
                else:
                        sub = np.argmax(prediction[x])
                if(sub == 0):
                        type0_x.append(data[x][0])
                        type0_y.append(data[x][1])
                        type0_z.append(data[x][2])
                elif(sub == 1):
                        type1_x.append(data[x][0])
                        type1_y.append(data[x][1])
                        type1_z.append(data[x][2])
                elif(sub == 2):
                        type2_x.append(data[x][0])
                        type2_y.append(data[x][1])
                        type2_z.append(data[x][2])
                elif(sub == 3):
                        type3_x.append(data[x][0])
                        type3_y.append(data[x][1])
                        type3_z.append(data[x][2])
                elif(sub == 4):
                        type4_x.append(data[x][0])
                        type4_y.append(data[x][1])
                        type4_z.append(data[x][2])

        type0 = ax.scatter(type0_x, type0_y, type0_z, s = 10, c = 'red')
        type1 = ax.scatter(type1_x, type1_y, type1_z, s = 10, c = 'black')
        type2 = ax.scatter(type2_x, type2_y, type2_z, s = 10, c = 'blue')
        type3 = ax.scatter(type3_x, type3_y, type3_z, s = 10, c = 'orange')
        type4 = ax.scatter(type4_x, type4_y, type4_z, s = 10, c = 'green')
        plt.legend((type0, type1, type2, type3, type4 ), ("DDos", "General", "Slow Links", "Blasting", "Hit the library"))
        local_time = time.strftime('%Y-%m-%d-%H-%M',time.localtime(time.time()))
        path = "/home/ELK/ELK/nginxlog/predictdata/pre-result/picture"
        if(os.path.exists(path) == False):
              os.makedirs(path)
        plt.savefig(path + '/' + str(local_time) + '.png')
        print("result")

def pca(prediction, n):
        pca = PCA(n_components=n)
        newdata = pca.fit_transform(prediction)
        matp(newdata, prediction)

def predict(csv_file):
    input_infos = read_log(csv_file)
    input_info = input_infos[:, 0:8]
    bool_matrix = input_info[:, 5].astype(int)
    ip_matrix = input_info[:, 2]
    timestamp_matrix = input_info[:, 0:2]
    compt_matrix = input_info[:, 4]
    cookie_matrix = input_info[:, 3]
    num_matrix = input_info[:, 6:8].astype(float)

    bool_matrix = bool2bina(4, bool_matrix)
    ip_matrix = ip2bina(ip_matrix)
    timestamp_matrix = normalize(utc2timestamp(timestamp_matrix))
    compt_matrix = completion2bina(2, compt_matrix)
    cookie_matrix = cookie2bina(2, cookie_matrix)
    #num_matrix = normalize(num_matrix)
	
    input_matrix = conn_matx(num_matrix, bool_matrix,
                                           ip_matrix, timestamp_matrix, compt_matrix, cookie_matrix)
    
    model = load_model('/home/ELK/ELK/nginxlog/traindata/securitai-lstm-model.h5')
    model.compile(loss = 'binary_crossentropy', optimizer = 'adam', metrics = ['accuracy'])
    input_matrix = np.reshape(input_matrix, (input_matrix.shape[0], 1, input_matrix.shape[1]))
    print("cwlx")
    prediction = model.predict(input_matrix)
    pca(prediction, 3)
    local_time = time.strftime('%Y-%m-%d-%H-%M',time.localtime(time.time()))
    path = "/home/ELK/ELK/nginxlog/predictdata/pre-result/resultlog"
    if(os.path.exists(path) == False):
          os.makedirs(path)
    for x in range(len(prediction)):
            np.set_printoptions(precision=3)
            sub = np.argmax(prediction[x])
            f = open(path + '/' + 'result.log','a')
            # f = open("/home/ELK/ELK/nginxlog/predictdata/result/" + str(local_time) + '_'+ str(sub), 'a')
            #"result/"为预测结果的输出、保存路径，在当前路径下
            for i in(input_info[x]):
                    f.write(str(i) + ' ')
            f.write('[' + str('{:.5f}'.format(prediction[x][0])) + ' ')
            for j in range(1, len(prediction[x])-1):
                    f.write(str('{:.5f}'.format(prediction[x][j])) + ' ')
            f.write(str('{:.5f}'.format(prediction[x][-1])) + ']' +'\n')

if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('-f', '--file', action="store", dest="file", help="data file")
    options, args = parser.parse_args()
    print("jit") 
    if options.file is not None:
        csv_file = options.file
    else:
       # csv_file = 'access.log'
        csv_file = '/home/ELK/ELK/nginxlog/predictdata/heartbeat.log'
        #'predict_data.txt'为用于预测的实际数据，在当前路径下
   # np.set_printoptions(suppress=True)
    predict(csv_file)
