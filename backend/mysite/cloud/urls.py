from django.urls import path, include
from cloud import views

urlpatterns = [
    # 폴더 업로드
    # query parameter <files/fileList?cid=<int>>
    path('files/loadFolder', views.loadFolder.as_view()),
    path('files/loadFiles', views.loadFiles.as_view()),
    path('files/uploadFiles', views.uploadFiles.as_view()),
    path('files/uploadFolder', views.uploadFolder.as_view()),
    path('files/deleteTrash/<int:id>', views.deleteTrash.as_view()),
    path('files/hardDelete/<int:id>', views.hardDelete.as_view()),
    path('files/restoreFile/<int:id>', views.restoreFile.as_view()),
    path('files/downloadFile/<int:id>', views.downloadFile.as_view()),
    path('files/renameFile/<int:id>', views.renameFile.as_view()),
    path('files/loadTrash', views.loadTrash.as_view()),
    path('files/fileList', views.FileList.as_view()),
    path('files/loadStarFiles', views.loadStarFiles.as_view()),
    path('files/loadRecentFiles', views.loadRecentFiles.as_view()),
    path('files/createStarFile/<int:id>', views.createStarFile.as_view()),
    path('files/deleteStarFile/<int:id>', views.deleteStarFile.as_view()),
    # 현재 공윺폴더함 로딩
    path('files/loadSingleShareFolder/<int:id>', views.loadSingleShareFolder.as_view()),
    # 공유문서함 폴더 로딩
    path('files/loadShareFolder', views.loadShareFolder.as_view()),
    # 공유문서함 파일 로딩
    path('files/loadShareFile/<int:id>', views.loadShareFile.as_view()),
    # 공유문서함 폴더 추가 data: name, owner(user.username)
    path('files/createShareFolder', views.createShareFolder.as_view()),
    # 공유문서함 아이디
    path('files/deleteShareFolder/<int:id>', views.deleteShareFolder.as_view()),
    # 공유문서함 유저 로딩
    path('files/loadShareUser/<int:id>', views.loadShareUser.as_view()),
    # 공유문서함 유저 추가 <int:id> data: username
    path('files/createShareUser/<int:id>', views.createShareUser.as_view()),
    # 공유문서함 유저 삭제 <int:id>?userId=userId
    path('files/deleteShareUser/<int:id>', views.deleteShareUser.as_view()),
    # 공유문서함 파일 추가 <int:id>
    path('files/createShareFile/<int:id>', views.createShareFile.as_view()),
    # 공유문서함 파일 삭제 <int:id>?fileId=fileId
    path('files/deleteShareFile/<int:id>', views.deleteShareFile.as_view()),



    # path('files/uploadFolder', views.FolderView.as_view()),
]
