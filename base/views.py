from django.shortcuts import render,redirect
from django.http import JsonResponse
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from .models import Advocate,Company
from rest_framework.permissions import IsAuthenticated
from .serializers import AdvocateSerializer,CompanySerializer
from django.db.models import Q
from rest_framework.views import APIView

# Create your views here.

@api_view(['GET','POST'])
def endpoints(request):
    data = ['/advocates','advocates/:username']
    return Response(data)

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def advocate_list(request):
    #data = ['ephraim','njogu','gethi']
    if request.method == 'GET':
       query = request.GET.get('query')

       if query==None:
          query = ''

       advocates = Advocate.objects.filter(Q(username__icontains=query) | Q(bio__icontains=query))
       serializer = AdvocateSerializer(advocates,many = True)
       return Response(serializer.data)
    if request.method == 'POST':
        advocate = Advocate.objects.create(username = request.data['username'],
                                bio = request.data['bio'])
        serializer = AdvocateSerializer(advocate,many = False)
        return Response(serializer.data)

@api_view(['GET'])
def companies_list(request):
    companies = Company.objects.all()
    serializer = CompanySerializer(companies,many=True)
    return Response(serializer.data) 
        


class AdvocateDetail(APIView):
    
    def get_object(self,username):
        try:
            return Advocate.objects.get(username=username)
        except Advocate.DoesNotExist:
            raise Advocate

    def get(self,request,username):
      #   advocates = Advocate.objects.get(username=username)
        advocates = self.get_object(username)
        serializer = AdvocateSerializer(advocates,many = False)
        return Response(serializer.data)
    
    def put(self,request,username):
        advocates = Advocate.objects.get(username=username)
        advocates.username = request.data['username']
        advocates.bio = request.data['bio']
        advocates.save()
        serializer = AdvocateSerializer(advocates,many = False)
        return Response(serializer.data)

    def delete(self,request,username):
        advocates = Advocate.objects.get(username=username)
        advocates.delete()
        return Response('deleted successfuly')

# @api_view(['GET','PUT','DELETE'])
# def advocate_detail(request,username):
#     advocates = Advocate.objects.get(username=username)
#     if request.method == 'GET':
#        serializer = AdvocateSerializer(advocates,many = False)
#        return Response(serializer.data)
    
#     if request.method == 'PUT':
#        advocates.username = request.data['username']
#        advocates.bio = request.data['bio']
#        advocates.save()
#        serializer = AdvocateSerializer(advocates,many = False)
#        return Response(serializer.data)
    
#     if request.method == 'DELETE':
#         advocates.delete()
#         return Response('deleted successfuly')