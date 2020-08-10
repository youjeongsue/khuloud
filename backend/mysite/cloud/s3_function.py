from django.conf import settings
import boto3
import sys
from django.conf import settings
from django.http import JsonResponse
s3 = boto3.resource('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
s3client = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
bucket = s3.Bucket(settings.AWS_STORAGE_BUCKET_NAME)


# 회원생성시 버킷 생성
def create_bucket(username):
    bucket = s3client.create_bucket(
        ACL='public-read-write',
        Bucket=username,
        CreateBucketConfiguration={
            'LocationConstraint': 'ap-northeast-2'},
    )


# 파일 업로드
def s3_upload_file(location, file):
    try:
        print(location, file)
        s3client.put_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=location, Body=file,
                            ACL="public-read")
    except Exception as e:
        print('Error on line {}'.format(
            sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        raise Exception('Upload Failed! ', e)


# 파일 다운로드
def s3_download_file(location, owner):
    try:
        print(location)
        object_url = "https://s3-{0}.amazonaws.com/{1}/{2}".format(
            'ap-northeast-2', owner, location)
        return object_url
    except Exception as e:
        print('Error on line {}'.format(
            sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        raise Exception('Download Failed! ', e)


def list_path(bucket, path):
    filelist = []
    for my_bucket_object in bucket.objects.all():
        filelist.append(my_bucket_object)
    print(filelist)

    return filelist


# hard Delete
def s3_delete_file(path):
    try:
        #location = location
        response = s3client.delete_object(Bucket='khuloud6', Key=path)
        print(response)
        message = {'message': 'Success to delete!'}
        return message
    except:
        message = {'message': 'Delete Failed'}
        return message


# 파일 이름 변경
def s3_rename_file(newname, owner, path):
    try:
        # print(">>>>>>>>>",owner, path, newname)
        response = s3client.copy_object(
            Bucket=owner,
            CopySource="/"+owner+"/"+path,
            Key="/"+newname
        )
        response = s3client.delete_object(Bucket=owner, Key=path)

        return response
    except Exception as e:
        print('Error on line {}'.format(
            sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        raise Exception('Rename Failed! ', e)
