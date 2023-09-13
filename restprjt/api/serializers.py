from rest_framework import serializers
from .models import User, Doctor
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import ValidationError

class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'},write_only=True)
    is_doctor = serializers.BooleanField(default=False,required=False)
    email = serializers.EmailField()
    
    class Meta:
        model =User
        fields = ['username','email','password','password2','is_doctor']

    def validate(self,data):
        password = data.get('password') 
        password2 = data.get('password2')   
        if password != password2:
            raise serializers.ValidationError('Passwords are incorrect!')
        return data
            
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['is_doctor'] = user.is_doctor
        if hasattr(user,'is_admin'):
            token['is_admin'] = user.is_admin
        return token   

class DoctorSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    hospital = serializers.CharField(required=False)
    department = serializers.CharField(required=False)
    class Meta:
        model = Doctor
        fields = ['id','hospital','department','user']
        read_only_fields = ('user',)

class UserProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    username = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    class Meta:
        model = User
        fields = ('id','first_name', 'last_name','username', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        users = args[0]
        if  users.is_doctor:
            self.fields['doctor'] = DoctorSerializer()
            
  

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)

        if instance.is_doctor:
            doctor_data = validated_data.get('doctor')
            print(doctor_data)
            if doctor_data:
                doctors = Doctor.objects.filter(user=instance)
                if doctors.exists():
                    doctor = doctors.first()  
                    doctor.hospital = doctor_data.get('hospital', doctor.hospital)
                    doctor.department = doctor_data.get('department', doctor.department)
                    if doctor.hospital is not None and doctor.department is not None:
                        doctor.is_verified=True
                    doctor.save()
                else:
                    raise ValidationError("No doctor record found for this user.")

        instance.save() 
        return instance
            

class UserProfileAdminSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer(read_only=True)   
    class Meta:
        model = User
        fields = ('id','first_name', 'last_name','username', 'email','is_doctor','is_active','doctor')

    def update(self,instance,validated_data):
        instance.is_active = validated_data.get('is_active',instance.is_active)
        instance.save()
        return instance