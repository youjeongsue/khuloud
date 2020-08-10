from rest_framework import serializers
from .models import File, StarFile, ShareFolder, ShareUser, ShareFile


class FileViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['name', 'isFolder', 'path', 'owner',
                  'filesize', 'modifiedDate', 'share', 'cid']

class StarFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StarFile
        fields = '__all__'

class ShareFolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShareFolder
        fields = '__all__'

class ShareUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShareUser
        fields = '__all__'

class ShareFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShareFile
        fields = '__all__'