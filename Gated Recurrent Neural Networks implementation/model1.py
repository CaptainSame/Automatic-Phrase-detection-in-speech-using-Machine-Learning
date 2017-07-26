import os
import numpy as np
from features import logfbank
from scipy.io.wavfile import read

base_dir = 'dataset'
subdirs = [os.path.join(base_dir, f) for f in os.listdir(base_dir)]
n_classes = len(subdirs)
X = []
y = []
for index, subdir in enumerate(subdirs):
    files = [os.path.join(subdir, f) for f in os.listdir(subdir)]
    for filepath in files:
        sr, audio = read(filepath)
        feats = logfbank(audio, sr, nfilt=40)
        X.append(feats)
        y.append(index)

X = np.array(X)
y = np.eye(n_classes)[np.array(y)]

print 'Data generated'

from sklearn.cross_validation import train_test_split

Xtrain, Xtest, ytrain, ytest = train_test_split(X, y, test_size=0.3)

from keras.optimizers import SGD
from keras.models import Sequential
from keras.layers.core import Dense
from keras.layers.recurrent import GRU

model = Sequential()
model.add(GRU(32, input_shape=(None, 40)))
#model.add(GRU(32))
model.add(Dense(n_classes, activation='softmax'))
sgd = SGD(lr=0.0001, momentum=0.9, decay=0.0)
model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
print model.summary()

n_epochs = 10000
training_losses = []
training_accs = []
testing_losses = []
testing_accs = []
for epoch_no in range(n_epochs):
    for i in range(Xtrain.shape[0]):
        train_loss, train_acc = model.train_on_batch( np.array([Xtrain[i]]), np.array([ytrain[i]]) )
        training_losses.append(train_loss)
        training_accs.append(train_acc)
    print 'Epoch:', epoch_no, '\ttraining_loss:', round(np.mean(training_losses), 3), '\ttraining acc:', round(np.mean(training_accs), 3), 
    for i in range(Xtest.shape[0]):
        test_loss, test_acc = model.test_on_batch( np.array([Xtest[i]]), np.array([ytest[i]]) )
        testing_losses.append(test_loss)
        testing_accs.append(test_acc)
    print '\tvalidation_loss:', round(np.mean(testing_losses), 3), '\ttestingacc:', round(np.mean(testing_accs), 3)
