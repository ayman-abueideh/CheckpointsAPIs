from django.urls import path
from task.views import UserSubscribedPoints, ClaimCheckPoint, UserTrustLevel

urlpatterns = [
    path('user_subscribed_points/<user_id>', UserSubscribedPoints.as_view(),
         name='user_subscribed_points'),
    path('claim_checkpoint/', ClaimCheckPoint.as_view(), name="claim_checkpoint"),
    path('user_trust_level/<user_id>', UserTrustLevel.as_view(), name="user_trust_level")
]
