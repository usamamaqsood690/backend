from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import UserProfile, Transaction, Category, Account


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value

    def create(self, validated_data):
        import secrets
        
        user = User.objects.create_user(
            username=validated_data['email'],  # 👈 username becomes email
            email=validated_data['email'],
            password=validated_data['password']
        )
        UserProfile.objects.get_or_create(
            user=user,
            defaults={'mongo_id': secrets.token_hex(12)}
        )
        return user


class RegisterResponseSerializer(serializers.ModelSerializer):
    access = serializers.SerializerMethodField()
    refresh = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'access', 'refresh']

    def get_access(self, obj):
        return str(RefreshToken.for_user(obj).access_token)

    def get_refresh(self, obj):
        return str(RefreshToken.for_user(obj))


class TransactionSerializer(serializers.ModelSerializer):
    transid = serializers.IntegerField(source='id', read_only=True)
    fee = serializers.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    datetime = serializers.DateField(source='date')
    typeoftrans = serializers.CharField(source='type')
    logo = serializers.CharField(allow_blank=True, default='')

    class Meta:
        model = Transaction
        fields = ['transid', 'name', 'amount', 'fee', 'datetime', 'typeoftrans', 'logo']
        read_only_fields = ['transid', 'datetime', 'typeoftrans']



class TransactionCreateSerializer(serializers.ModelSerializer):
    account = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all())
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), allow_null=True)

    class Meta:
        model = Transaction
        fields = ['account', 'category', 'name', 'amount', 'fee', 'type', 'date', 'logo', 'note']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            self.fields['account'].queryset = Account.objects.filter(user=request.user)
            self.fields['category'].queryset = Category.objects.filter(user=request.user)

    def validate_type(self, value):
        valid_types = {choice[0] for choice in Category.TYPE_CHOICES}
        if value not in valid_types:
            raise serializers.ValidationError("Type must be either 'income' or 'expense'.")
        return value

    def validate(self, attrs):
        category = attrs.get("category")
        transaction_type = attrs.get("type")

        if category and transaction_type and category.type != transaction_type:
            raise serializers.ValidationError({
                "category": "Category type must match the transaction type."
            })
        return attrs

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
