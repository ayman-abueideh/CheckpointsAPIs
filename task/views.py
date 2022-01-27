from django.db.models import Sum, Count
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from task.models import User, Claim, SubscribedPoints, Checkpoint
from task.serializer import UserIdSerializer, UserSubscribedPointsOutputSerializer, \
    ClaimCheckPointInputSerializer
from task.util import get_min_timestamp


# Create your views here.

class UserSubscribedPoints(APIView):
    def get(self, request, user_id):
        input_serializer = UserIdSerializer(data={'user_id': user_id})
        if input_serializer.is_valid(raise_exception=True):
            subscribed_checkpoints = SubscribedPoints.objects.filter(user_id=user_id) \
                .values_list("checkpoint_id", flat=True)

            min_time_stamp = get_min_timestamp()
            claims = list(
                Claim.objects.filter(checkpoint_id__in=subscribed_checkpoints, timestamp__gte=min_time_stamp) \
                    .values("checkpoint__location_name", "checkpoint__min_number", "state").annotate(
                    status_summation=Sum("state")))
            output_serializer = UserSubscribedPointsOutputSerializer(claims, many=True)
            return Response(output_serializer.data)


class ClaimCheckPoint(APIView):
    def post(self, request):
        input_serializer = ClaimCheckPointInputSerializer(data=request.data)
        if input_serializer.is_valid(raise_exception=True):
            user_id = input_serializer.data.get("user_id")
            checkpoint_id = input_serializer.data.get("checkpoint_id")
            state = input_serializer.data.get("state")
            user = User.objects.filter(id=user_id).first()
            checkpoint = Checkpoint.objects.filter(id=checkpoint_id).first()
            if user is None:
                return Response(status=HTTP_400_BAD_REQUEST, data={"msg": f"User does not exist"})
            elif checkpoint is None:
                return Response(status=HTTP_400_BAD_REQUEST, data={"msg": f"CheckPoint does not exist"})
            else:
                claim = Claim(user_id=user_id, checkpoint_id=checkpoint_id, state=state)
                claim.save()
                return Response({'message': 'claim created successfully'})


class UserTrustLevel(APIView):
    def get(self, request, user_id):
        input_serializer = UserIdSerializer(data={'user_id': user_id})
        if input_serializer.is_valid(raise_exception=True):
            trust_level = 0
            min_time_stamp = get_min_timestamp()
            number_of_claims = Claim.objects.filter(user_id=user_id, timestamp__gte=min_time_stamp).count()

            checkpoints_stats = list(
                Claim.objects.filter().values("checkpoint_id", "checkpoint__min_number").annotate(
                    checkpoint_status=Count("state")))

            checkpoints_stats = {
                checkpoint["checkpoint_id"]: checkpoint["checkpoint_status"] >= checkpoint["checkpoint__min_number"]
                for checkpoint in checkpoints_stats}

            user_claims = list(Claim.objects.filter(user_id=user_id, timestamp__gte=min_time_stamp) \
                               .values("user_id", "checkpoint_id", "state").annotate(status_summation=Sum("state")))

            for user_claim in user_claims:
                if checkpoints_stats[user_claim["checkpoint_id"]]:
                    trust_level += user_claim["status_summation"] / number_of_claims
            return Response({"trust_level": trust_level})
