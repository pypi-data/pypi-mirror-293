from django.urls import path

from . import views

api_urlpatterns = [
    path(
        "locations/<int:pk>/completeness/",
        views.LocationCompletenessReportView.as_view(),
        name="plank_locations_completeness",
    ),
    path(
        "checks/<int:pk>/check-out-form.pdf",
        views.CheckOutFormView.as_view(),
        name="plank_check_out_form",
    ),
    path(
        "checks/<int:pk>/check-in-form.pdf",
        views.CheckInFormView.as_view(),
        name="plank_check_in_form",
    ),
]
