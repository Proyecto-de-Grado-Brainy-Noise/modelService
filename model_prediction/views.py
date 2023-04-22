import os
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from rest_framework import status
from .tasks import process_nifti
import base64

#from bson.objectid import ObjectId


# Create your views here.


#from model_prediction.models import ResonanceResult


@csrf_exempt
@api_view(['POST'])
def makePrediction(request):
    
    try:       
        dag_path=os.getcwd()
        print("++------------------------------------------------------------------------+++++")
        print(f"Getting file info: {timezone.localtime(timezone.now())}")
        print("MAIN PATH: ",dag_path)
        print(request.data)
        
        if 'resonance_file' not in request.data or 'metadata' not in request.data or 'email' not in request.data:
            return Response({'error': 'No data uploaded, some of the data is missing.'}, status=status.HTTP_400_BAD_REQUEST)
        
        nifiti_file_obj = request.data['resonance_file']
        metadata_file_obj = request.data['metadata']
        email =  request.data['email']
        
        if not nifiti_file_obj.name.endswith('.nii.gz') or not metadata_file_obj.name.endswith('.json'):
            print("Incorrect File 2")
            return Response({'error': 'Files must be a NIFTI and a JSON.'}, status=status.HTTP_400_BAD_REQUEST)
    
    
        nifiti_file_contents = nifiti_file_obj.read()
        metadata_file_contents = metadata_file_obj.read()
        
        
        nifiti_file_contents_b64 = base64.b64encode(nifiti_file_contents).decode('utf-8')
        
        metadata_file_contents_b64 = base64.b64encode(metadata_file_contents).decode('utf-8')
        
        print("Processing a queueing Nifti File...")
            
        result=process_nifti.delay(nifiti_file_contents_b64,
                                   nifiti_file_obj.name,
                                   metadata_file_contents_b64,
                                   email
                                   )
            
        return Response({'message': 'NIFTI file uploaded successfully', "task_id":result.id},status=status.HTTP_200_OK)
        
    except Exception as e:
       return Response({'error':"Server error","description":e}, status=status.HTTP_400_BAD_REQUEST)
    
    
        
    

    

    # results = ResonanceResult.objects.all()
    # data = [{'name': r.name, 'age': r.age, 'id': r._id} for r in results]
    # print(data)







#   result = ResonanceResult.objects.get(_id=ObjectId("6431dfb5b439ae1687706b1e"))
#         print(result._id)



 # result=ResonanceResult.objects.all()
        
        # print("The length of the result is: ", len(result))
        
        
        
         
        # result=ResonanceResult.objects.all()
        
        # print("The length of the result is: ", len(result))
        
        
        # result = ResonanceResult.objects.get(_id=ObjectId("6433020fe5f52412a0a53625"))
        # print(result._id)
        
        # ResonanceResult.objects.create(predicton=1, metadata={"hola":"no"}, 
        #                            fileName="hola",
        #                            fileExtension=".nii.gz",completeFileName="hola.nii.gz",
        #                            predicton_date=f"{timezone.localtime(timezone.now())}")
           