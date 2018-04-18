from django.urls import path, include
from rest_framework import routers

from . import api
from . import views

router = routers.DefaultRouter()
router.register(r'location', api.LocationViewSet)
router.register(r'legislation', api.LegislationViewSet)
router.register(r'staff', api.StaffViewSet)
router.register(r'clinic', api.ClinicViewSet)
router.register(r'revenue', api.RevenueViewSet)
router.register(r'volunteer', api.VolunteerViewSet)
router.register(r'demographics', api.DemographicsViewSet)


urlpatterns = (
    # urls for Django Rest Framework API
    path('api/v1/', include(router.urls)),
)

urlpatterns += (
    # urls for Location
    path('location/', views.LocationListView.as_view(), name='location_list'),
    path('location/create/', views.LocationCreateView.as_view(),
         name='location_create'),
    path('location/detail/<int:pk>/', views.LocationDetailView.as_view(),
         name='location_detail'),
    path('location/update/<int:pk>/', views.LocationUpdateView.as_view(),
         name='location_update'),
)

urlpatterns += (
    # urls for Legislation
    path('legislation/', views.LegislationListView.as_view(),
         name='legislation_list'),
    path('legislation/create/', views.LegislationCreateView.as_view(),
         name='legislation_create'),
    path('legislation/detail/<int:pk>/', views.LegislationDetailView.as_view(),
         name='legislation_detail'),
    path('legislation/update/<int:pk>/', views.LegislationUpdateView.as_view(),
         name='legislation_update'),
)

urlpatterns += (
    # urls for Staff
    path('staff/', views.StaffListView.as_view(), name='staff_list'),
    path('staff/create/', views.StaffCreateView.as_view(), name='staff_create'),
    path('staff/detail/<int:pk>/', views.StaffDetailView.as_view(),
         name='staff_detail'),
    path('staff/update/<int:pk>/', views.StaffUpdateView.as_view(),
         name='staff_update'),
)

urlpatterns += (
    # urls for Clinic
    path('clinic/', views.ClinicListView.as_view(), name='clinic_list'),
    path('clinic/create/', views.ClinicCreateView.as_view(),
         name='clinic_create'),
    path('clinic/detail/<int:pk>/', views.ClinicDetailView.as_view(),
         name='clinic_detail'),
    path('clinic/update/<int:pk>/', views.ClinicUpdateView.as_view(),
         name='clinic_update'),
)

urlpatterns += (
    # urls for Revenue
    path('revenue/', views.RevenueListView.as_view(), name='revenue_list'),
    path('revenue/create/', views.RevenueCreateView.as_view(),
         name='revenue_create'),
    path('revenue/detail/<int:pk>/', views.RevenueDetailView.as_view(),
         name='revenue_detail'),
    path('revenue/update/<int:pk>/', views.RevenueUpdateView.as_view(),
         name='revenue_update'),
)

urlpatterns += (
    # urls for Volunteer
    path('volunteer/', views.VolunteerListView.as_view(), name='volunteer_list'),
    path('volunteer/create/', views.VolunteerCreateView.as_view(),
         name='volunteer_create'),
    path('volunteer/detail/<int:pk>/', views.VolunteerDetailView.as_view(),
         name='volunteer_detail'),
    path('volunteer/update/<int:pk>/', views.VolunteerUpdateView.as_view(),
         name='volunteer_update'),
)

urlpatterns += (
    # urls for Demographics
    path('demographics/', views.DemographicsListView.as_view(),
         name='demographics_list'),
    path('demographics/create/', views.DemographicsCreateView.as_view(),
         name='demographics_create'),
    path('demographics/detail/<int:pk>/', views.DemographicsDetailView.as_view(),
         name='demographics_detail'),
    path('demographics/update/<int:pk>/', views.DemographicsUpdateView.as_view(),
         name='demographics_update'),
)
