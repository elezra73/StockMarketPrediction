import pandas as pd
import numpy as np
import os
import keras
import matplotlib.pyplot as plt
from keras.layers import Dense,GlobalAveragePooling2D
from keras.applications import MobileNet
from keras.preprocessing import image
from keras.applications.vgg16 import VGG16
from keras.applications.mobilenet import preprocess_input
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing import image
from keras.models import Model
from keras.optimizers import Adam

#base_model=MobileNet(weights='imagenet',include_top=False) #imports the mobilenet model and discards the last 1000 neuron layer.
base_model = VGG16(weigth='imagenet', include_top=False)
x=base_model.output
x=GlobalAveragePooling2D()(x)
x=Dense(1024,activation='relu')(x) #we add dense layers so that the model can learn more complex functions and classify for better results.
x=Dense(1024,activation='relu')(x) #dense layer 2
x=Dense(512,activation='relu')(x) #dense layer 3
preds=Dense(120,activation='softmax')(x) #final layer with softmax activation

model=Model(inputs=base_model.input,outputs=preds)
print(model)
#specify the inputs
#specify the outputs
#now a model has been created based on our architecture

for i,layer in enumerate(model.layers):
  print(i,layer.name)

  for layer in model.layers:
      layer.trainable = False
  # or if we want to set the first 20 layers of the network to be non-trainable
  for layer in model.layers[:20]:
      layer.trainable = False
  for layer in model.layers[20:]:
      layer.trainable = True

  train_datagen = ImageDataGenerator(preprocessing_function=preprocess_input)  # included in our dependencies

  train_generator = train_datagen.flow_from_directory('C:\\Users\Daniel\Desktop\Linear_Interpolation',
                                                      target_size=(224, 224),
                                                      color_mode='rgb',
                                                      batch_size=32,
                                                      class_mode='categorical',
                                                      shuffle=True)

