from djongo import models
from django.utils import timezone
from paranoid_model.models import Paranoid
from django.contrib.auth.models import User

class File(Paranoid):
    name = models.CharField(null=True, default='', max_length=50)
    isFolder = models.BooleanField()
    path = models.TextField()
    owner = models.CharField(null=True, default='', max_length=30)
    filesize = models.CharField(max_length=10)
    createdDate = models.DateTimeField(default=timezone.now)
    modifiedDate = models.CharField(blank=True, null=True, max_length=10)
    share = models.BooleanField(default=False)
    cid = models.IntegerField(default=0)
    class Meta:
        ordering = ['createdDate']

class StarFile(models.Model):
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class ShareFolder(models.Model):
    name = models.CharField(null=True, default='', max_length=50)
    owner = models.CharField(null=True, default='', max_length=30)
    createdDate = models.DateTimeField(default=timezone.now)

class ShareUser(models.Model):
    shareFolder = models.ForeignKey(ShareFolder, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class ShareFile(models.Model):
    shareFolder = models.ForeignKey(ShareFolder, on_delete=models.CASCADE)
    file = models.ForeignKey(File, on_delete=models.CASCADE)

