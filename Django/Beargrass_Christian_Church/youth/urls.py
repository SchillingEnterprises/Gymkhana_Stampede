from django.conf.urls import url, include
from rest_framework import routers

from youth import views
from youth import api

router = routers.DefaultRouter()
router.register(r'churchgoer', api.ChurchGoerViewSet)


urlpatterns = (
    # urls for ChurchGoer
    url(r'^youth/$', views.ChurchGoerListView.as_view(), name='list'),
    url(r'^youth/(?P<pk>\d+)/$', views.ChurchGoerDetailView.as_view(), name='detail'),
    url(r'^youth/create/$', views.ChurchGoerCreateView.as_view(), name='create'),
    url(r'^youth/edit/(?P<pk>\d+)/$', views.ChurchGoerUpdateView.as_view(), name='update'),
    # url(r'^delete/(?P<pk>\d+)/$', views.ChurchGoerDeleteView.as_view(), name='delete'),

    url(r'search/$', views.search, name='search'),

    # urls for Django Rest Framework API
    url(r'^$', views.ListCreateChurchGoer.as_view(),
        name='api_list'),
    url(r'^(?P<pk>\d+)/$',
        views.RetrieveUpdateDestroyChurchGoer.as_view(),
        name='api_detail'),
    url(r'^api/v1/', include(router.urls)),
    url(r'^api/v2/', include(router.urls)),
)
