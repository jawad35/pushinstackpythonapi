from django.urls import path
from . import views

urlpatterns = [
    path('', views.apiOverview, name="api-overview"),
    path('task-list/', views.taskList, name="task-list"),
    path('task-detail/<str:pk>/', views.taskDetail, name="task-detail"),
    path('task-create/', views.taskCreate, name="task-create"),
    # new apis
    path('youtube-tags/', views.getYoutubeTags, name="youtube-tags"),
    path('webpage-load-checker/',
         views.getWebLoad,
         name="webpage-load-checker"),
    path('get-domain-info/', views.getDomainInfo, name="get-domain-info"),
    path('text-counter/', views.getTextCount, name="text-counter"),
    path('webpage-all-images/',
         views.getAllWebPageImages,
         name="webpage-all-images"),
    path('test-internet-speed/',
         views.TestMyInternetSpeed,
         name="test-internet-speed"),
    path('get-top-keywords/', views.GetTopKeywords, name="get-top-keywords"),
    path('emails-extractor/',
         views.GetExtractedEmails,
         name="emails-extractor"),
    path('webpage-source-code/',
         views.GetWebPageSourceCode,
         name="ewebpage-source-code"),

    # new apis closed
    path('task-update/<str:pk>/', views.taskUpdate, name="task-update"),
    path('task-delete/<str:pk>/', views.taskDelete, name="task-delete"),
]
