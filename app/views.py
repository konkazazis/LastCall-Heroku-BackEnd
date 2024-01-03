from rest_framework import generics, permissions, status
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import render
from django.contrib.auth import  login, logout

from .models import  Expense

from .serializers import UserRegisterSerializer, UserLoginSerializer, UserSerializer, ExpenseSerializer, UserUpdateSerializer
from .validation import custom_validation, validate_email, validate_password

######### Home View #########
def home(request):
    return render(request, 'home.html')

######### User Views #########
class UserRegister(APIView):
	permission_classes = (permissions.AllowAny,)
	def post(self, request):
		#clean_data = custom_validation(request.data)
		serializer = UserRegisterSerializer(data=request.data)
		if serializer.is_valid(raise_exception=True):
			user = serializer.create(request.data)
			if user:
				return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(status=status.HTTP_400_BAD_REQUEST)
	
class UserLogin(APIView):
	permission_classes = (permissions.AllowAny,)
	authentication_classes = (SessionAuthentication,)
	##
	def post(self, request):
		data = request.data
		# assert validate_email(data)
		# assert validate_password(data)
		serializer = UserLoginSerializer(data=data)
		if serializer.is_valid(raise_exception=True):
			user = serializer.check_user(data)
			login(request, user)
			return Response(serializer.data, status=status.HTTP_200_OK)

class UserLogout(APIView):
	permission_classes = (permissions.AllowAny,)
	authentication_classes = ()
	def post(self, request):
		logout(request)
		return Response(status=status.HTTP_200_OK)

class UserView(APIView):
	permission_classes = (permissions.IsAuthenticated,)
	authentication_classes = (SessionAuthentication,)
	##
	def get(self, request):
		serializer = UserSerializer(request.user)
		return Response({'user': serializer.data}, status=status.HTTP_200_OK)
################                 


######### Expenses Views #########
class ExpenseListView(generics.ListAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Get the authenticated user
        user = self.request.user
        # Filter expenses based on the authenticated user
        queryset = Expense.objects.filter(user=user)
        
        return queryset

class ExpenseDeleteView(generics.DestroyAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]  # Include Session Authentication 

class ExpenseCreateView(generics.CreateAPIView):
	queryset = Expense.objects.all()
	serializer_class = ExpenseSerializer
	permission_classes = [permissions.IsAuthenticated]
	authentication_classes = (SessionAuthentication,)

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)
################

class UserProfileUpdate(UpdateAPIView):
    serializer_class = UserUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)
