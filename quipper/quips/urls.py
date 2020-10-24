from django.urls import path, include

from quips.views import *

urlpatterns = [
    # will redirect to login view otherwise
    path("", QuipListView.as_view(), name="quip_list"),
    path("c/<int:pk>", QuipDetailView.as_view(), name="quip_detail"),
    path("c/create_quip/", QuipCreateView.as_view(), name="quip_create"),
    path("c/update_quip/<int:pk>", QuipUpdateView.as_view(), name="quip_update"),
    path("c/delete_quip/<int:pk>", QuipDeleteView.as_view(), name="quip_delete"),
]
