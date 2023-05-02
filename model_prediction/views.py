import json
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from rest_framework import status
from .tasks import process_nifti
import base64
from  django.core.files.uploadedfile import TemporaryUploadedFile


# Create your views here.

def showIntro():
    print("+++++------------------------------------------------------------------------------------------------+++++")
    print("+++++-------------------------------BRAINY NOISE CNN MODEL SERVICE-----------------------------------+++++")
    print("+++++------------------------------------------------------------------------------------------------+++++")
    print("+++++--------------------------Jessica N. , Estefanía B. , Sebastián V. -----------------------------+++++")
    print("+++++------------------------------------------------------------------------------------------------+++++") 


@csrf_exempt
@api_view(['POST'])
def makePrediction(request):
    
    try:       
        
        showIntro()
        print(f"Getting file info at: {timezone.localtime(timezone.now())}")
   
   
        if 'resonance_file' not in request.data or 'email' not in request.data:
            return Response({'error': 'No data uploaded, some of the data is missing.'}, status=status.HTTP_400_BAD_REQUEST)
        
        nifiti_file_obj = request.data['resonance_file']
        email =  request.data['email']
        
        
        if('metadata' in request.data) and  type(request.data['metadata'])==TemporaryUploadedFile:
            metadata_file_obj = request.data['metadata']
            metadata_file_contents = metadata_file_obj.read()
            metadata_file_contents_b64 = base64.b64encode(metadata_file_contents).decode('utf-8')
        else:
            metadata_file_obj=None
            metadata_file_contents_b64=None
        
    
        if not nifiti_file_obj.name.endswith('.nii.gz') or (metadata_file_obj!=None and not metadata_file_obj.name.endswith('.json') ):
                return Response({'error': 'Files must be a NIFTI and a JSON.'}, status=status.HTTP_400_BAD_REQUEST)
    
        nifiti_file_contents = nifiti_file_obj.read()
        nifiti_file_contents_b64 = base64.b64encode(nifiti_file_contents).decode('utf-8')
        
        
        
        print("Processing and adding to queue Nifti File...")
            
        result=process_nifti.delay(nifiti_file_contents_b64,
                                   nifiti_file_obj.name,
                                   metadata_file_contents_b64,
                                   email,
                                   )
            
        return Response({'message': 'NIFTI file uploaded successfully', "task_id":result.id},status=status.HTTP_200_OK)
        
    except TypeError as e:
       return Response({'error':"Server error","description":e}, status=status.HTTP_400_BAD_REQUEST)
    
    
        