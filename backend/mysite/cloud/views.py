from django.shortcuts import render
from .models import File, StarFile, ShareUser, ShareFile, ShareFolder
from django.contrib.auth.models import User
from django.http import HttpResponse
import boto3
import os
import json
from django.http import JsonResponse
from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
import json
from .serializers import (
    FileSerializer,
    FileViewSerializer,
    StarFileSerializer,
    ShareFolderSerializer,
    ShareUserSerializer,
    ShareFileSerializer
)
from accounts.serializers import (
    UserSerializer
)
from rest_framework.parsers import MultiPartParser, FormParser

#from cloud.aws import aws_key
import configparser
from .s3_function import *
config = configparser.ConfigParser()
config.read('config.ini')


# 현재 폴더 로딩
class loadFolder(generics.GenericAPIView):
    serializer_class = FileViewSerializer

    def get(self, request, *args, **kwargs):
        folder = {}
        id = request.GET.get('id')
        owner = settings.AWS_STORAGE_BUCKET_NAME
        print(id)
        query = File.objects.get(owner=owner, id=id)
        folder['id'] = query.id
        folder['name'] = query.name
        folder['isFolder'] = query.isFolder
        folder['path'] = query.path
        folder['modifiedDate'] = query.modifiedDate
        folder['share'] = query.share
        folder['cid'] = query.cid
        folder['filesize'] = query.filesize
        folder['owner'] = query.owner
        return Response({'folder': folder})


# 파일 로딩
class loadFiles(generics.GenericAPIView):
    serializer_class = FileSerializer

    def get(self, request, *args, **kwargs):
        files = []
        cid = request.GET.get('cid')
        print(cid)
        owner = request.GET.get('owner')
        queryset = File.objects.filter(cid=cid).filter(
            owner=settings.AWS_STORAGE_BUCKET_NAME)
        for query in queryset:
            file = {}
            file['id'] = query.id
            file['name'] = query.name
            file['isFolder'] = query.isFolder
            file['path'] = query.path
            file['modifiedDate'] = query.modifiedDate
            file['share'] = query.share
            file['cid'] = query.cid
            file['filesize'] = query.filesize
            file['owner'] = query.owner
            files.append(file)
        return Response({'files': files})


# 폴더 업로드
class uploadFolder(generics.GenericAPIView):
    serializer_class = FileSerializer

    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        folder = serializer.save()
        return Response({
            'file': FileViewSerializer(folder).data
        })


# 다중 파일 업로드
class uploadFiles(generics.GenericAPIView):
    permissions_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = FileSerializer

    def post(self, request, *args, **kwargs):
        files = []
        user = UserSerializer(self.request.user).data
        print("User: ", user)
        for key, file in enumerate(request.FILES.getlist('file')):
            uploadFile = {}
            s3_upload_file(request.data.getlist('path')[
                           key], request.FILES.getlist('file')[key])
            uploadFile['name'] = request.data.getlist('name')[key]
            uploadFile['isFolder'] = request.data.getlist('isFolder')[key]
            uploadFile['path'] = request.data.getlist('path')[key]
            uploadFile['owner'] = settings.AWS_STORAGE_BUCKET_NAME
            uploadFile['filesize'] = request.data.getlist('filesize')[key]
            uploadFile['share'] = request.data.getlist('share')[key]
            uploadFile['modifiedDate'] = request.data.getlist('modifiedDate')[
                key]
            uploadFile['cid'] = int(request.data.getlist('cid')[key])

            serializer = self.get_serializer(data=uploadFile)
            serializer.is_valid(raise_exception=True)
            file = serializer.save()
            file = FileViewSerializer(file).data
            print(file)
            files.append(file)
        return Response({'files': files})


'''
## 파일 삭제
class deleteTrash(generics.GenericAPIView):
    permissions_classes = [
            permissions.IsAuthenticated,
        ]
    def delete(self, request, id):
        print(id)
        queryset = File.objects.filter(id=id)
        print(queryset)
        file = FileSerializer(queryset, many=True).data
        location = file[0]['path']
        delete_file = s3_delete_file(location)
        print(delete_file)
        if queryset.delete():
            print("DATABASE DELETE!")
        else:
            print("DATABASE NOT DELETE!")
        return JsonResponse(delete_file)

'''


# 휴지통에서 파일 복원
class restoreFile(generics.GenericAPIView):
    def get(self, request, id):
        print('restore file',id)
        File.objects.get_or_restore(id=id)
        return Response({'message': 'Success to restore!'})


# 파일 삭제 soft -> 휴지통으로 이동
class deleteTrash(generics.GenericAPIView):
    def delete(self, request, id):
        files = []
        files.append(id)
        cnt = 0
        for fid in files:
            queryset = File.objects.filter(id=fid)  # id로 DB에서 객체 찾음
            queryset.delete()
            cnt += 1
        if cnt == len(files):
            return Response({'message': 'Success to soft delete!'})


# 파일 삭제 hard -> 휴지통에서 삭제시 S3에서 삭제
class hardDelete(generics.GenericAPIView):
    def delete(self, request, id):
        File.objects.get_or_restore(id=id)
        print("id: ", id)
        queryset = File.objects.filter(id=id)
        location = queryset.values('path')
        for i in location:
            path = i['path']
        print("path: ", path)
        delete_file = s3_delete_file(path)
        if queryset.delete(hard_delete=True):
            print("DATABASE DELETE!")
        else:
            print("DATABASE NOT DELETE!")
        return JsonResponse({'message': delete_file})


# soft 파일들 로드
class loadTrash(generics.GenericAPIView):
    serializer_class = FileSerializer

    def get(self, request):
#         queryset = File.objects.all(with_delete=True)
        queryset = File.objects.exclude(deleted_at = None)
        print(queryset)
        files = []
        for query in queryset:
            file = {}
            file['id'] = query.id
            file['name'] = query.name
            file['isFolder'] = query.isFolder
            file['path'] = query.path
            file['modifiedDate'] = query.modifiedDate
            file['share'] = query.share
            file['cid'] = query.cid
            file['filesize'] = query.filesize
            file['owner'] = query.owner
            file['deleted_at'] = query.deleted_at
            files.append(file)
        return Response({'files': files})


# 파일 다운로드
class downloadFile(generics.GenericAPIView):
    def get(self, request, id):
        print(id)
        queryset = File.objects.filter(id=id)
        print(queryset.values())
        file_name = FileSerializer(queryset, many=True).data
        owner = file_name[0]['owner']
        file_name = file_name[0]['path']
        print(file_name)
        download_file = s3_download_file(file_name, owner)
        return Response({'file_url': download_file})


# 파일 이름 변경
class renameFile(generics.GenericAPIView):
    def post(self, request, id):
        queryset = File.objects.filter(id=id)
        owner = queryset.values('owner')[0]['owner']
        path = queryset.values('path')[0]['path']
        oldname = queryset.values('name')[0]['name']
        newname = request.data.get('newname')
        extension=oldname.split(".")[-1]
        newname = newname + '.' + extension
        print(owner, path)
        print(path[:path.index(oldname)]+newname)
        response = s3_rename_file(newname, owner, path)
        queryset.update(name=newname, path=path[:path.index(oldname)]+newname)
        file = FileViewSerializer(queryset, many=True).data
        print(file[0])
        return Response({'updatedFile': file[0]})


class FileList(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        owner = request.GET.get('owner', None)
        queryset = File.objects.filter(owner=owner)
        serializer = FileSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

## 중요문서함 로딩
class loadStarFiles(generics.GenericAPIView):
    permissions_classes=[
            permissions.IsAuthenticated,
    ]
    def get(self, request, *args, **kwargs):
        queryset = StarFile.objects.filter(user = self.request.user.id)
        print(queryset)
        user = User.objects.get(id = self.request.user.id)
        print(user)
        starFiles = []
        for query in queryset:
            starFile = {}
            file = File.objects.get(id = query.file.id)
            file = FileViewSerializer(file).data
            print(file)
            starFiles.append(file)
        print(starFiles)
        return Response({'files': starFiles})

## 중요문서함 생성
class createStarFile(generics.GenericAPIView):
    permissions_classes=[
        permissions.IsAuthenticated,
    ]
    def post(self, request, id, *args, **kwargs):
        print(self.request.user)
        user = User.objects.get(id=self.request.user.id)
        file = File.objects.get(id=id)
        starFile = StarFile.objects.create(
                    file=file, user=user
        )
        starFile = StarFileSerializer(starFile).data
        print(starFile, user)
        return Response({'files': starFile})

## 중요문서함 삭제
class deleteStarFile(generics.GenericAPIView):
    permissions_classes=[
        permissions.IsAuthenticated,
    ]
    def delete(self, request, id, *args, **kwargs):
        starFile = StarFile.objects.filter(file=id, user=self.request.user.id)
        starFile.delete()
        return Response({'info': 'Database deleted'})


## 최신문서함 로딩
class loadRecentFiles(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        queryset = File.objects.filter(isFolder = False, owner= self.request.user.username).order_by('updated_at')
        print(queryset)
        files = FileViewSerializer(queryset, many=True).data
        print(queryset, files)
        return Response({'files': files})

## 공유문서함 로딩
class loadSingleShareFolder(generics.GenericAPIView):
    permissions_classes=[
            permissions.IsAuthenticated,
    ]

    def get(self, request, id, *args, **kwargs):
        shareFolder = ShareFolder.objects.get(id = id)
        shareFolder = ShareFolderSerializer(shareFolder).data
        print(shareFolder)
        return Response({'shareFolder': shareFolder})

## 공유문서함 로딩
class loadShareFolder(generics.GenericAPIView):
    permissions_classes=[
            permissions.IsAuthenticated,
    ]

    def get(self, request, *args, **kwargs):
        queryset = ShareUser.objects.filter(user = self.request.user.id)
        shareFolders = []
        for query in queryset:
            shareFolder = {}
            shareFolder = ShareFolder.objects.get(id = query.shareFolder.id)
            shareFolder = ShareFolderSerializer(shareFolder).data
            print(shareFolder)
            shareFolders.append(shareFolder)
        print(shareFolders)
        return Response({'shareFolders': shareFolders})


## 공유문서함 클릭 이후 파일 로딩
class loadShareFile(generics.GenericAPIView):
    permissions_classes=[
            permissions.IsAuthenticated,
    ]
    def get(self, request, id, *args, **kwargs):
        queryset = ShareFile.objects.filter(shareFolder=id)
        print(queryset)
        shareFiles = []
        for query in queryset:
            shareFile = {}
            shareFile = File.objects.get(id = query.file.id)
            shareFile = FileViewSerializer(shareFile).data
            shareFiles.append(shareFile)
        print(shareFiles)
        return Response({'shareFiles': shareFiles})



## 공유문서함에서 유저 로딩
class loadShareUser(generics.GenericAPIView):
    def get(self, request, id, *args, **kwargs):
        queryset = ShareUser.objects.filter(shareFolder=id)
        shareUsers = []
        for query in queryset:
            shareUser = {}
            shareUser = User.objects.get(id = query.user.id)
            print(shareUser)
            shareUser = UserSerializer(shareUser).data
            shareUsers.append(shareUser)
        return Response({'shareUsers': shareUsers})

## 공유문서함 추가
class createShareFolder(generics.GenericAPIView):
    permissions_classes=[
        permissions.IsAuthenticated
    ]
    serializer_class = ShareFolderSerializer

    def post(self, request, *args, **kwargs):
        print(request.data) # name, owner(user.username)
        user = User.objects.get(id = self.request.user.id)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()
        shareFolder = serializer.save()
        ShareUser.objects.create(user = user, shareFolder = shareFolder)
        return Response({
            'shareFolder': ShareFolderSerializer(shareFolder).data
        })

## 공유문서함 삭제
class deleteShareFolder(generics.GenericAPIView):
    permissions_classes=[
        permissions.IsAuthenticated
    ]
    def delete(self, request, id, *args, **kwargs):
        shareFolder = ShareFolder.objects.filter(id=id, owner=self.request.user.username)
        shareFolder.delete()
        return Response({'info': 'Database deleted'})

## 공유문서함에 유저 추가
class createShareUser(generics.GenericAPIView):
    permissions_classes=[
        permissions.IsAuthenticated,
    ]
    def post(self, request, id, *args, **kwargs):
        print(request.data) # name, owner(user.username)
        username = request.data.get('username')
        shareFolder = ShareFolder.objects.get(id=id, owner=self.request.user.username)
        user = User.objects.get(username = username)
        shareUser = ShareUser.objects.create(
                    shareFolder=shareFolder, user=user
        )
        user = UserSerializer(user).data
        print('addShareUser', user)
        return Response({'shareUser': user})

## 공유문서함에 유저 삭제
class deleteShareUser(generics.GenericAPIView):
    permissions_classes=[
        permissions.IsAuthenticated
    ]
    def delete(self, request, id, *args, **kwargs):
        userId = request.GET.get('userId')
        shareUser = ShareUser.objects.filter(shareFolder=id, user=userId)
        shareUser.delete()
        return Response({'info': 'Database deleted'})

# 공유문서함에 파일 추가
class createShareFile(generics.GenericAPIView):
    def post(self, request, id, *args, **kwargs):
        fileId = request.data.get('fileId')
        shareFolder = ShareFolder.objects.get(id=id)
        print(shareFolder)
        file = File.objects.get(id = fileId)
        file.share = True
        file.save()
        print(file)
        print('update share file', file)
        shareFile = ShareFile.objects.create(
            shareFolder=shareFolder, file=file
        )
        shareFile = ShareFileSerializer(shareFile).data
        print('addShareFile', shareFile)
        return Response({'shareFile': shareFile})

# 공유문서함에 파일 삭제
class deleteShareFile(generics.GenericAPIView):
    def delete(self, request, id, *args, **kwargs):
        fileId = request.GET.get('fileId')
        print(fileId)
        shareFile = ShareFile.objects.get(shareFolder=id, file = fileId)
        file = File.objects.get(id = fileId)
        file.share = False
        file.save()
        shareFile.delete()
        print('deleteShareFile!')
        return Response({'message': 'Datebase deleted'})