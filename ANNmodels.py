import numpy as np
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM
from keras.layers.wrappers import TimeDistributed, Bidirectional
from keras.models import Sequential
import ANNTool as md

SAMPLE_LEN = 100 #Size of the sequences (size of each csv file)
N_SAMPLE = 5000 #Number of sequences (the number of csv files)


'''Function that fetches the data
Args : the folder where the csv files containing the traces are
Outputs : (list of rtt, list of labels (cp) 
'''
def fetch_data(folder):
    file_csv = os.listdir(folder)
    x = []
    y = []
    for f in file_csv:
        f = folder + '/' + f
        temp = csvio.csv2list(f, 'trace', sep=',', decimal='.')
        x.append(temp)
        y.append(csvio.csv2list(f, 'cpt', sep=',', decimal='.'))
    inputs=[[x[i][j]-min(x[i]) for j in range(len(x[i]))] for i in range(len(x))]
    outputs=[1 if sum(y[i])>0 else 0 for i in range(len(y))]
    inputs=inputs.reshape(N_SAMPLE,SAMPLE_LEN,1)
    outputs=outputs.reshape(N_SAMPLE,1)
    return (inputs,outputs)

    
'''
Function to be called to train the model on the data_x, data_y.
Args : (data_x, data_y, number of epochs
'''
def train_model(data_x,data_y,N_EPOCH):
    model=sequential()
    model.add(LSTM(15, return_sequences = False, input_shape = (None, 100,1)))
    model.add(Dense(1, activation = 'sigmoid'))
    model.compile(loss = 'binary_crossentropy', optimizer = 'adam', metrics = MTX)
    history = model.fit(data_x, data_y, validation_split = 0.2,
                    epochs = N_EPOCH, batch_size = SAMPLE_LEN, verbose=1)
    print(model.summary())
    md.save_trained_model(model, fn='detectChange')
    return
