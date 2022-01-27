from django.urls import path
from task.views import HelloView, UserSubscribedPoints, ClaimCheckPoint

urlpatterns = [
    path('hello/', HelloView.as_view(), name='hello'),
    path('user_subscribed_points/<user_id>', UserSubscribedPoints.as_view(),
         name='user_subscribed_points'),
    path('claim_checkpoint/', ClaimCheckPoint.as_view(), name="claim_checkpoint")
]
