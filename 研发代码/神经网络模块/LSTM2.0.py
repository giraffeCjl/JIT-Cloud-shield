import sys
import os
import json
import pandas as pd
import numpy as np
import optparse
import time
import datetime
import pytz
from keras.callbacks import TensorBoard
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout
from keras.layers.embeddings import Embedding
from keras.preprocessing import sequence
from keras.preprocessing.text import Tokenizer
from collections import OrderedDict

def read_log(path):
        dataframe = pd.read_table(path, sep=' ', header=None,
                                        names=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13'],
                                        dtype = {'1': str, '2': str, '3': str, '4': str, '5':str, '6': int, '7': float,
                                                '8': int, '9':int , '10': int, '11': int, '12': int, '13': int})
        dataframe = dataframe.sample(frac=1).values
        info = np.array(dataframe)
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
        print(num_matrix)
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

def train(csv_file):
    input_infos = read_log(csv_file)
    input_info = input_infos[:, 0:8]
    output_info = input_infos[:, 8:]
    
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

    train_size = 4500
    
    X_train, X_test = input_matrix[0:train_size], input_matrix[train_size:len(input_matrix)]
    Y_train, Y_test = output_info[0:train_size], output_info[train_size:len(output_info)]
    X_train = np.reshape(X_train, (X_train.shape[0], 1, X_train.shape[1]))
    X_test = np.reshape(X_test, (X_test.shape[0], 1, X_test.shape[1]))

    tb_callback = TensorBoard(log_dir='./logs')

    model = Sequential()

    model.add(LSTM(64, recurrent_dropout=0.5, input_shape=(1, 43)))
    model.add(Dropout(0.5))
    model.add(Dense(5, activation='sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    print(model.summary())
    model.fit(X_train, Y_train, validation_split=0.25, epochs=300, batch_size=128, callbacks=[tb_callback])

    # Evaluate model
    score, acc = model.evaluate(X_test, Y_test, verbose=1, batch_size=128)

    print("Model Accuracy: {:0.2f}%".format(acc * 100))

    # Save model
    model.save_weights('securitai-lstm-weights.h5')
    model.save('securitai-lstm-model.h5')
    with open('securitai-lstm-model.json', 'w') as outfile:
        outfile.write(model.to_json())

if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('-f', '--file', action="store", dest="file", help="data file")
    options, args = parser.parse_args()

    if options.file is not None:
        csv_file = options.file
    else:
        csv_file = '/home/ELK/ELK/nginxlog/traindata/train_data.txt'
    train(csv_file)
