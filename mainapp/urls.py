from django.urls import path

from .views import create_user_view, login_view, whoami, list_documents_view, list_criteria_view, get_criteria_view,\
    list_indicator_view, get_indicator_view, DocumentView, create_document_view, complete_profile_view, \
    get_document_by_indicator_view, image_validation_view

urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', create_user_view, name='register'),
    # path('profile/', ProfileView.as_view(), name='profile'),
    path('whoami/', whoami, name='whoami'),
    path('complete-profile/', complete_profile_view, name='complete-profile'),
    path('criteria/', list_criteria_view, name='list-criteria'),
    path('criteria/<str:id>/', get_criteria_view, name='get-criterion'),
    path('criteria/<str:criterion_id>/indicators/', list_indicator_view, name='list-indicators'),
    path('indicators/<str:id>/', get_indicator_view, name='get-indicator'),
    path('indicators/<str:indicator_id>/view-doc/', get_document_by_indicator_view, name='get-doc-by-indicator'),##########################################
    path('documents/', list_documents_view, name='list-documents'),
    path('documents/<str:id>/', DocumentView.as_view(), name='list-documents'),
    path('document/create/', create_document_view, name='create-document'),
    path("validate-image/", image_validation_view, name="validate-image"),
]