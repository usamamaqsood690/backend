from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, TransactionSerializer, TransactionCreateSerializer
from .models import Transaction


# ==========================
# REGISTER VIEW
# ==========================
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)

        return Response({
            "success": True,
            "message": "User registered successfully",
            "data": {
                "id": user.id,
                "email": user.email,
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            }
        }, status=status.HTTP_201_CREATED)


# ==========================
# EMAIL LOGIN VIEW
# ==========================
class EmailLoginView(APIView):

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response({
                "success": False,
                "message": "Email and password are required"
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({
                "success": False,
                "message": "Invalid credentials"
            }, status=status.HTTP_401_UNAUTHORIZED)

        user = authenticate(username=user_obj.username, password=password)

        if user is None:
            return Response({
                "success": False,
                "message": "Invalid credentials"
            }, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)

        return Response({
            "success": True,
            "message": "Login successful",
            "data": {
                "id": user.id,
                "email": user.email,
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            }
        }, status=status.HTTP_200_OK)


# ==========================
# TRANSACTION LIST VIEW
# ==========================
class TransactionListView(generics.ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Transaction.objects.filter(user=self.request.user).select_related("account", "category")

        transaction_type = self.request.query_params.get("type")
        start_date = self.request.query_params.get("start_date")
        end_date = self.request.query_params.get("end_date")

        if transaction_type:
            if transaction_type not in {choice[0] for choice in Transaction._meta.get_field("type").choices}:
                raise ValidationError({"type": "Type must be either 'income' or 'expense'."})
            queryset = queryset.filter(type=transaction_type)
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)

        return queryset


# ==========================
# TRANSACTION CREATE VIEW
# ==========================
class TransactionCreateView(generics.CreateAPIView):
    serializer_class = TransactionCreateSerializer
    permission_classes = [IsAuthenticated]
