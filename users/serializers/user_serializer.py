from users.models import UserModel
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for returning user details securely."""

    phoneNumber = serializers.CharField(source="phone_number")

    lastName = serializers.CharField(source="last_name")
    firstName = serializers.CharField(source="first_name")
    fullName = serializers.SerializerMethodField(source="get_full_name")

    isStaff = serializers.BooleanField(source="is_staff")
    isActive = serializers.BooleanField(source="is_active")

    updatedAt = serializers.DateTimeField(source="updated_at")
    createdAt = serializers.DateTimeField(source="created_at")

    class Meta:
        model = UserModel
        fields = [
            "id",
            "email",
            "username",
            "phoneNumber",
            "firstName",
            "lastName",
            "fullName",
            "isStaff",
            "isActive",
            "createdAt",
            "updatedAt",
        ]

        read_only_fields = fields  # Make all fields read-only

    def get_full_name(self, obj):
        """Return the full name, joining first and last name."""
        return obj.get_full_name()
