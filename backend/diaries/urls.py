from django.urls import path
from . import views

urlpatterns = [
    path('api/diaries', views.DiaryCreate.as_view(), name='create-diary'),  # 创建日记
    path('api/diaries/my-diaries', views.UserDiaries.as_view(), name='my-diaries'),  # 获取用户日记
    path('api/diaries/<int:diaryId>', views.DiaryUpdate.as_view(), name='update-diary'),  # 更新日记
    path('api/diaries/<int:diaryId>/delete', views.DiaryDelete.as_view(), name='delete-diary'),  # 删除日记
]
