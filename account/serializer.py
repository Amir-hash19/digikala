from rest_framework import serializers
from django.contrib.auth.models import Group
from .models import CustomUser
from phonenumber_field.serializerfields import PhoneNumberField




class SendOTPRegisterSerializer(serializers.ModelSerializer):
    phone = PhoneNumberField(region="IR")

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'phone', 'gender')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['user_type'] = 'normal' 

    
        user = CustomUser(**validated_data)
        user.set_unusable_password()
        user.save()

        if user.user_type:
            group, _ = Group.objects.get_or_create(name=user.user_type.capitalize())
            user.groups.add(group)

        return user


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['phone'] = str(instance.phone)
        return representation
          