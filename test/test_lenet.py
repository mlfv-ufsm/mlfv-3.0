import sys
import rpyc
import timeit
import multiprocessing
import numpy as np
import pandas as pd
import keras.backend as K
import keras
from keras.models import Sequential
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import AveragePooling2D, MaxPooling2D
from keras.layers.core import Activation
from keras.layers.core import Flatten
from keras.layers.core import Dense
from keras.optimizers import SGD
from keras.utils.np_utils import to_categorical
from SpatialPyramidPooling import SpatialPyramidPooling

MLFV_SERVER_HOST="127.0.0.1"
MLFV_SERVER_PORT=15088


def read_images(img_path='./dataset/',apps=['cg','dt','mg','bifu','cyl2d'],train_dim=128,test_dim=256):
  import os
  import cv2

  X_train = []
  X_test  = []
  y_train = []
  y_test  = []

  max = 999
  for app in apps:
    path = img_path + app + '_' + str(train_dim) + '/'
    f = os.listdir(path)
    if (len(f) < max): max = len(f)
  max = 200

  for app in apps:
    path = img_path + app + '_' + str(train_dim) + '/'
    for d, r, f in os.walk(path):
      for file in f[:max]:
        if (not file.endswith('.png')): continue
        img = cv2.imread(path+file,cv2.IMREAD_GRAYSCALE)
        if (not img is None):
          X_train.append(img)
          y_train.append(apps.index(app))

    path = img_path + app + '_' + str(test_dim) + '/'
    for d, r, f in os.walk(path):
      for file in f[:100]:
        if (not file.endswith('.png')): continue
        img = cv2.imread(path+file,cv2.IMREAD_GRAYSCALE)
        if (not img is None):
          X_test.append(img)
          y_test.append(apps.index(app))

  X_train = np.asarray(X_train)
  X_test  = np.asarray(X_test)

  y_train = to_categorical(np.asarray(y_train))
  y_test  = to_categorical(np.asarray(y_test))

  X_train = X_train.reshape(X_train.shape[0],X_train.shape[1],X_train.shape[2],1)
  X_test = X_test.reshape(X_test.shape[0],X_test.shape[1],X_test.shape[2],1)

  return (X_train, y_train), (X_test, y_test)

def get_chain():
  p = {}

  dataset = read_images()

  apps=['cg','dt','mg','bifu','cyl2d']
  input_shape = (None, None, 1) if K.image_data_format() == 'channels_last' else (1, None, None)

  model = Sequential([
    Conv2D(6, kernel_size=(5, 5), strides=(1, 1), activation='tanh', input_shape=input_shape, padding='same'),
    AveragePooling2D(pool_size=(2,2), strides=(1,1), padding='valid'),
    Conv2D(16, kernel_size=(5, 5), strides=(1, 1), activation='tanh', padding='valid'),
    AveragePooling2D(pool_size=(2, 2), strides=(2, 2), padding='valid'),
    Conv2D(120, kernel_size=(5, 5), strides=(1, 1), activation='tanh', padding='valid'),
    SpatialPyramidPooling([1, 2, 4]),
    Dense(84, activation='tanh'),
    Dense(len(apps), activation='softmax'),
    Activation('softmax')
  ])

  p['model_json'] = model.to_json()
  p['dataset'] = dataset

  p['batch_size'] = 28
  p['epochs'] = 2

  p['optimizer'] = { 'type': 'SGD', 'lr': 0.001 } # SGD(lr=0.001)
  p['loss'] = 'categorical_crossentropy'
  p['metrics'] = ['accuracy']

  #generating the functions 
  s0 = "prep_data = preprocessing.Preprocessing(dataset)"
  s1 = "cla = training.Training(model_json, optimizer, loss, metrics, batch_size, epochs, prep_data)"
  s2 = "pred = testing.Testing(cla, model_json, optimizer, loss, metrics, batch_size, prep_data)"

  #composing and returning the chain
  return (s0, s1, s2), p


#connects to the MLFV Module and sends the chain (c) with their parameters (p)
def send_chain(c,p):
  start = timeit.default_timer()

  rpyc.core.protocol.DEFAULT_CONFIG['allow_pickle'] = True
  rpyc.core.protocol.DEFAULT_CONFIG['sync_request_timeout'] = 30000
  
  con = rpyc.connect(MLFV_SERVER_HOST, MLFV_SERVER_PORT, config = rpyc.core.protocol.DEFAULT_CONFIG)

  ret = con.root.exec_chain(c,p)
  end = timeit.default_timer()
  time = end - start
  print("Total execution time: "+str(time))
  return ret


#executes a single chain
def single():
  c,p = get_chain()
  x = send_chain(c,p)


#perfoms multiple executions in parallel
def multiple(num_par):
  jobs = []
  c,p = get_chain()
  for i in range(num_par):
    print("Sending "+str(i))
    proc = multiprocessing.Process(target=send_chain, args=(c, p))
    jobs.append(proc)
    proc.start()
  for j in jobs:
    print("Waiting for jobs")
    j.join()
    print(j.name+'exitcode = ' +str(j.exitcode))


if __name__ == "__main__":
  if len(sys.argv) == 1:
    single()
  else:
    multiple(int(sys.argv[1]))

