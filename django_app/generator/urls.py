from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="generator-home"),
    path("table_create", views.table_create, name="tables"),

    path("api/generate_json_copypress/", views.query_json_copypress, name="generate-api-copypress"),
    path("api/generate_json_focusgroup/", views.query_json_focusgroup, name="generate-api-focusgroup"),
    path("api/img_filter/", views.img_filter, name="img-filter"),
    path("api/img_similarity/", views.img_similarity, name="img-similarity"),
]