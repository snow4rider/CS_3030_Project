from rest_framework import serializers
from users.models import Profile


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ('username', 'logged_on', 'id', 'friends')


class ProfileListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ('username', 'id', 'logged_on')