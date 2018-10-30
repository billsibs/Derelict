# Use include() to add paths from the catalog application
from django.conf.urls import include
from django.urls import path

urlpatterns += [
    path('gambit/', include('gambitapp.urls')),
]
