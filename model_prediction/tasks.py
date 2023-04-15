import base64
import json
import os
from celery import Celery
import nibabel as nib
import os
from model_prediction.CNN import cnn_model
from django.utils import timezone
from .models import ResonanceResult
from modelService.celery import app



@app.task
def process_nifti(niftiFile_base64,niftiFile_name,metadata_base64, email):
    try:   
        
        print(f"WORKER CONNECTED TO VIEW!!!!!:{timezone.localtime(timezone.now())}")
        nifti_file_contents = base64.b64decode(niftiFile_base64.encode('utf-8'))
        
        metadata_file_contents = base64.b64decode(metadata_base64.encode('utf-8'))
        
        nifiti_file_temp_path=f"model_prediction/temp/{niftiFile_name[:8]}.nii.gz"
        
        metadata_file_temp_path=f"model_prediction/temp/{niftiFile_name[:8]}_metadata.json"
        
        print("Nifti route: ",nifiti_file_temp_path)
        
        print("Metadata route: ",metadata_file_temp_path)
        
        print("OKKKKKK")
  
        print("OKKKKKK 2.0")
        
        with open(nifiti_file_temp_path, "wb") as f:
            f.write(nifti_file_contents)
            
            
        with open(metadata_file_temp_path, "wb") as f:
            f.write(metadata_file_contents)
            
                
        nifti = nib.load(nifiti_file_temp_path)
        data = nifti.get_fdata()
        print("Nifti file shape: ",data.shape)
                
        print("DATA REMOVED!")
        
        cnn_model.model.summary()
        print("NOW ITS TIME TO PREDICT THE DATA!")
        predicted_label=cnn_model.getPrediction(data)
        print("Label: ",predicted_label)
        
                
        with open(metadata_file_temp_path, 'r') as f:
            file_contents = json.load(f)
            
        splitFileName=niftiFile_name.split(".")
        
                
        print("Uploading result to database...")
        ResonanceResult.objects.create(predicton=predicted_label, metadata=file_contents, 
                                       fileName=splitFileName[0],email=email,
                                       fileExtension=".nii.gz",completeFileName=niftiFile_name,
                                       predicton_date=f"{timezone.localtime(timezone.now())}")
        
        # print("Deleting data...")
        
        # os.remove(nifiti_file_temp_path)
        # os.remove(metadata_file_contents)
        
        
        return "Ok"
    except Exception as e:
        return f"Error processing file: {e}"