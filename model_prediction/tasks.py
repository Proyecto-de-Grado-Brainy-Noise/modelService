import base64
import json
import os
import celery
import nibabel as nib
import os
from model_prediction.CNN import cnn_model
from django.utils import timezone
from .models import ResonanceResult
from modelService.celery import app
import skimage.transform as skTrans


@app.task
def process_nifti(niftiFile_base64,niftiFile_name,metadata_base64, email):
    try:   
        BASE_VOLUME_PATH='/usr/src/app'
        
        print(f"Worker-Task started at: {timezone.localtime(timezone.now())}")
                
        nifti_file_contents = base64.b64decode(niftiFile_base64.encode('utf-8'))
                
        nifiti_file_temp_path=f"{BASE_VOLUME_PATH}/temp/{niftiFile_name[:8]}.nii.gz"
        
        
        with open(nifiti_file_temp_path, "wb") as f:
            f.write(nifti_file_contents)
        
                                    
        nifti = nib.load(nifiti_file_temp_path)
        data = nifti.get_fdata()
        
        if(data.shape[0]!=256 or data.shape[1]!=256 or data.shape[2]!=336):
            resul_tranform = skTrans.resize(data, (336,256,256), order=1, preserve_range=True)
            data=resul_tranform.T
        
        print("Nifti file shape: ",data.shape)
                
                
        cnn_model.model.summary()
        print("Generating CNN prediction")
        predicted_label,label_confidence=cnn_model.getPrediction(data)
        print("Label: ",predicted_label)
            
        splitFileName=niftiFile_name.split(".")
        
        
        if(metadata_base64!=None):
            metadata_file_contents = base64.b64decode(metadata_base64.encode('utf-8'))    
            file_contents= json.loads(metadata_file_contents)    
        else:
            file_contents={"Value":"None"}
                        
        print("Uploading result to database...")
        
        ResonanceResult.objects.create(task_id=f"{celery.current_task.request.id}",
                                       predicton=predicted_label,confidence=label_confidence,metadata=file_contents, 
                                       fileName=splitFileName[0],email=email,
                                       fileExtension=".nii.gz",completeFileName=niftiFile_name,
                                       predicton_date=f"{timezone.localtime(timezone.now())}")
        
        
        print("Deleting data...")
        os.remove(nifiti_file_temp_path)
        
        return "Ok"
    except Exception as e:
        return f"Error processing file: {e}"
    
    

# @app.task
# def process_nifti(niftiFile_base64,niftiFile_name,metadata_base64, email):
#     try:   
#         BASE_VOLUME_PATH='/usr/src/app'
        
#         print(f"Worker-Task started at: {timezone.localtime(timezone.now())}")
                
#         nifti_file_contents = base64.b64decode(niftiFile_base64.encode('utf-8'))
        
#         metadata_file_contents = base64.b64decode(metadata_base64.encode('utf-8'))
                
#         nifiti_file_temp_path=f"{BASE_VOLUME_PATH}/temp/{niftiFile_name[:8]}.nii.gz"
        
        
#         with open(nifiti_file_temp_path, "wb") as f:
#             f.write(nifti_file_contents)
            
#         file_contents= json.loads(metadata_file_contents)
        
                            
#         nifti = nib.load(nifiti_file_temp_path)
#         data = nifti.get_fdata()
        
#         if(data.shape[0]!=256 or data.shape[1]!=256 or data.shape[2]!=336):
#             resul_tranform = skTrans.resize(data, (336,256,256), order=1, preserve_range=True)
#             data=resul_tranform.T
        
#         print("Nifti file shape: ",data.shape)
                
                
#         cnn_model.model.summary()
#         print("Generating CNN prediction")
#         predicted_label=cnn_model.getPrediction(data)
#         print("Label: ",predicted_label)
            
#         splitFileName=niftiFile_name.split(".")
                        
#         print("Uploading result to database...")
#         ResonanceResult.objects.create(task_id=f"{celery.current_task.request.id}",predicton=predicted_label, 
#                                        metadata=file_contents, 
#                                        fileName=splitFileName[0],email=email,
#                                        fileExtension=".nii.gz",completeFileName=niftiFile_name,
#                                        predicton_date=f"{timezone.localtime(timezone.now())}")
        
        
#         print("Deleting data...")
#         os.remove(nifiti_file_temp_path)
        
#         return "Ok"
#     except Exception as e:
#         return f"Error processing file: {e}"    