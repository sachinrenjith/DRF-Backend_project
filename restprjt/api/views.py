from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import UserRegistrationSerializer, MyTokenObtainPairSerializer, UserProfileSerializer,UserProfileAdminSerializer
from .models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAdminUser




class UserRegistration(APIView):
    def post(self,request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            User.objects.create_user(
                username = serializer.validated_data['username'],
                email = serializer.validated_data['email'],
                password = serializer.validated_data['password'],
                is_doctor = serializer.validated_data['is_doctor']
            )
            return Response({'msg':'Registration Successfull..'},status=status.HTTP_201_CREATED)
        return Response({'msg':serializer.errors},status=status.HTTP_400_BAD_REQUEST)

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UserProfile(APIView):
    def get(self,request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def patch(self,request):
        serializer = UserProfileSerializer(request.user,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Profile Updated ...','Profile':serializer.data},status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request):
        user = User.objects.get(id=request.user.id)
        user.delete()
        return Response({"msg":"Deleted"},status=status.HTTP_200_OK)

@permission_classes([IsAdminUser])
class UserProfileView(APIView):
    def get(self,request,pk=None):
        if pk is None:
            user=User.objects.exclude(is_admin=True)
            serializer=UserProfileAdminSerializer(user,many=True)
            return Response(serializer.data)
        user=User.objects.get(pk=pk)
        serializer=UserProfileAdminSerializer(user)
        return Response(serializer.data)
    
    def patch(self,request,pk=None):
        if pk is not None:
            user=User.objects.get(pk=pk)
            serializer=UserProfileAdminSerializer(user,data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                if serializer.validated_data['is_active']:
                    return Response({'msg':'User Unblocked'},status=status.HTTP_200_OK)
                return Response({'msg':'User is Blocked'},status=status.HTTP_200_OK)
            return Response(serializer.errors)



