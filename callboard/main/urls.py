from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', index, name='index'),
    path('board', BoardAll.as_view(), name='board'),
    path('board/create', AdvertisementCreate.as_view(), name='create'),
    path('board/<int:pk>', AdvertisementDetails.as_view(), name='details'),
    path('board/<int:pk>/respond', ResponseCreate.as_view(), name='response'),
    path('board/<int:post_id>/respond/<int:pk>/answer', response_answer, name='response_answer'),
    path('board/<int:post_id>/respond/<int:pk>/delete', ResponseDelete.as_view(), name='response_delete'),
    path('board/<int:pk>/edit', AdvertisementUpdate.as_view(), name='edit'),
    path('board/<int:pk>/delete', AdvertisementDelete.as_view(), name='delete'),
    path('me', my_advertisements, name='me'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
