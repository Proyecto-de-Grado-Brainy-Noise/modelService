from keras.models import load_model
from scipy import stats
import numpy as np
import tensorflow as tf
import skimage.transform as skTrans

class CNN_Model():
    
    def __init__(self):
        # physical_devices = tf.config.list_physical_devices('GPU')
        # tf.config.experimental.set_memory_growth(physical_devices[0], True)
        self.model= load_model("model_prediction/model_weights")
        
    def getPrediction(self,img_data):
        split_data=self.getSplitNifti(img_data)
        print(split_data.shape)
        pr= self.model.predict(split_data)
        predictions=np.argmax(pr, axis=1)
        predicted_label=int(stats.mode(predictions, keepdims=False)[0])
        return predicted_label 
    
    
    def getSplitNifti(self,img_data):
        result = skTrans.resize(img_data, (336,256,256), order=1, preserve_range=True)
        img_data=result.T
        X=[]
        for i in range(56):
            start = i*6
            end = (i+1)*6
            data_slice=img_data[:,:,start:end]
            X.append(data_slice)
        return np.array(X) 
    
    
    
cnn_model= CNN_Model()