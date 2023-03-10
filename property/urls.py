from django.urls import path

from property.views.create_property import CreatePropertyView
from property.views.list_property import ListPropertyView
from property.views.update_property import UpdatePropertyView
from property.views.comments_views import PropertyCommentView, CreateReservationCommentView

app_name = 'property'
urlpatterns = [
    path('create/', CreatePropertyView.as_view(), name='create'),
    path('update/<int:pk>/', UpdatePropertyView.as_view(), name='update'),
    path('search/', ListPropertyView.as_view(), name='search'),
    path('comments/<int:pk>', PropertyCommentView.as_view(), name='view_property_comments'),
    path('comments/add/reservation/<int:pk>', CreateReservationCommentView.as_view(), name='add_reservation_comment'),
]
