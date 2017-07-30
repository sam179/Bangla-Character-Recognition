import keras
import numpy as np 
from keras.datasets import cifar100,cifar10
from keras.models import Sequential,Model
from keras.layers import Dense,Dropout,Activation,Convolution2D,MaxPooling2D,Flatten
from keras.optimizers import SGD,RMSprop
from keras.preprocessing.image import ImageDataGenerator
from keras.utils import np_utils
import keras.layers.containers
from keras.callbacks import EarlyStopping

import numpy as np
from sklearn.cross_validation import train_test_split



train = np.load("train.npy")
test = np.load("labels.npy")

#print train.shape
#print test.shape

nb_classes = 222

labels = np_utils.to_categorical(test, nb_classes)
#print labels.shape


X_train, X_test, Y_train, Y_test = train_test_split(train,labels,test_size = 0.2)

X_train = X_train.reshape(X_train.shape[0], 1, 32, 32)
X_test = X_test.reshape(X_test.shape[0], 1, 32, 32)

print X_train.shape
print X_test.shape
print Y_train.shape
print Y_test.shape


###################################################################################################################################

nn = Sequential()
nn.add(Convolution2D(32,3,3,border_mode='same',init="glorot_normal",input_shape=(1,32,32)))
nn.add(Activation('relu'))
nn.add(Convolution2D(32,3,3))
nn.add(Activation('relu'))
nn.add(MaxPooling2D(pool_size=(2,2)))
nn.add(Dropout(0.5))

nn.add(Convolution2D(64,3,3,border_mode='same'))
nn.add(Activation('relu'))
nn.add(Convolution2D(64,3,3))
nn.add(Activation('relu'))
nn.add(MaxPooling2D(pool_size=(2,2)))
nn.add(Dropout(0.5))


nn.add(Flatten())
nn.add(Dense(512))
nn.add(Activation('relu'))
nn.add(Dropout(0.5))
nn.add(Dense(nb_classes))
nn.add(Activation('softmax'))
sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
rms = RMSprop(lr=0.001)
nn.compile(loss='categorical_crossentropy',optimizer=sgd)
nn.load_weights('my_model_weights.h5')

#nn.fit(X_train,Y_train,nb_epoch=200,batch_size=10,show_accuracy=True,verbose=1)
X_train = X_train.astype('float32')
X_test = X_test.astype('float32')
X_train /= 255
X_test /= 255

#datagen = ImageDataGenarator()

#checkpointer = keras.callbacks.ModelCheckpoint(filepath="epoch_weights.hdf5", verbose=1, save_best_only=True)
datagen = ImageDataGenerator(
        featurewise_center=False,  # set input mean to 0 over the dataset
        samplewise_center=False,  # set each sample mean to 0
        featurewise_std_normalization=False,  # divide inputs by std of the dataset
        samplewise_std_normalization=False,  # divide each input by its std
        zca_whitening=False,  # apply ZCA whitening
        rotation_range=0,  # randomly rotate images in the range (degrees, 0 to 180)
        width_shift_range=0.1,  # randomly shift images horizontally (fraction of total width)
        height_shift_range=0.1,  # randomly shift images vertically (fraction of total height)
        horizontal_flip=True,  # randomly flip images
        vertical_flip=False)  # randomly flip images

    # compute quantities required for featurewise normalization
    # (std, mean, and principal components if ZCA whitening is applied)
datagen.fit(X_train)

    # fit the model on the batches generated by datagen.flow()
nn.fit_generator(datagen.flow(X_train, Y_train, batch_size=128),
                        samples_per_epoch=0.1*X_train.shape[0],
                        nb_epoch=2, show_accuracy=True,
                        validation_data=(X_test, Y_test),
                        nb_worker=1)#,callbacks=[checkpointer])

#score = model.evaluate(X_test, Y_test, batch_size=16)
print nn.predict_classes(X_test, batch_size=128, verbose=0)
#json_string = nn.to_json()
#open('my_model_architecture.json', 'w').write(json_string)
nn.save_weights('my_model_weights.h5',overwrite=True)

score = nn.evaluate(X_test, Y_test, verbose=1,show_accuracy=True)
print score

