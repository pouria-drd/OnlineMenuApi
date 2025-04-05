from rest_framework import serializers
from django.contrib.auth import authenticate


class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True,
        min_length=1,
        max_length=30,
        error_messages={
            "required": "نام کاربری الزامی است.",
            "blank": "نام کاربری نمی‌تواند خالی باشد.",
            "min_length": "نام کاربری باید حداقل 1 کاراکتر باشد.",
            "max_length": "نام کاربری باید حداکثر 30 کاراکتر باشد.",
        },
    )
    password = serializers.CharField(
        required=True,
        min_length=1,
        write_only=True,
        error_messages={
            "required": "رمز عبور الزامی است.",
            "blank": "رمز عبور نمی‌تواند خالی باشد.",
            "min_length": "رمز عبور باید حداقل 1 کاراکتر باشد.",
        },
    )

    def validate(self, data):
        request = self.context.get("request")  # get request from serializer context
        user = authenticate(request=request, **data)  # pass request explicitly

        if not user:
            raise serializers.ValidationError(
                {"message": "نام کاربری یا رمز عبور اشتباه است."}
            )

        if not user.is_active:
            raise serializers.ValidationError({"message": "حساب کاربری فعال نیست."})

        data["user"] = user
        return data
