from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.DiaryCreate.as_view(), name='create-diary'),  # 创建日记
    path('my-diaries/', views.UserDiaries.as_view(), name='my-diaries'),  # 获取用户日记
    path('update/<int:diaryId>/', views.DiaryUpdate.as_view(), name='update-diary'),  # 更新日记
    path('delete/<int:diaryId>/', views.DiaryDelete.as_view(), name='delete-diary'),  # 删除日记
    path('get_all_diaries/', views.GetAllDiariesView.as_view(), name='get_all_diaries'),
    path('rate/',views.RateDiary.as_view(),name = 'rate_diary'),
]
