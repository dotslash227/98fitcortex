from django.conf.urls import url
from analytics.views import CustomerGoogleClientView,CustomerTrackingView


urlpatterns = [
	url(r'^client/$' , CustomerGoogleClientView.as_view() , name = "customer-google-client"),
	url(r'^track/$' , CustomerTrackingView.as_view() , name = "customer-tracking")
]