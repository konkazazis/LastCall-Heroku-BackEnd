from rest_framework import serializers
from .models import Expense
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import make_password

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'

UserModel = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserModel
		fields = '__all__'
	def create(self, clean_data):
		user_obj = UserModel.objects.create_user(email=clean_data['email'], password=clean_data['password'])
		user_obj.username = clean_data['username']
		user_obj.save()
		return user_obj

class UserLoginSerializer(serializers.Serializer):
	email = serializers.EmailField()
	password = serializers.CharField()
	def check_user(self, clean_data):
		user = authenticate(username=clean_data['email'], password=clean_data['password'])
		# if not user:
		# 	raise ValidationError('user not found')
		return user

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserModel
		fields = ('email', 'username','user_id')

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
            'username': {'required': False},
            'email': {'required': False},
        }
    def create(self, validated_data):
        password = validated_data.get('password')
        hashed_password = make_password(password, hasher='pbkdf2_sha256')
        validated_data['password'] = hashed_password
        user = self.Meta.model.objects.create(**validated_data)
        return user
    def update(self, instance, validated_data):
        password = validated_data.get('password')
        if password:
            hashed_password = make_password(password, hasher='pbkdf2_sha256')
            validated_data['password'] = hashed_password
        else:
            validated_data['password'] = instance.password
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
