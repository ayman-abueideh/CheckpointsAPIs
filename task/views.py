import datetime
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from task.serializer import UserSubscribedPointsInputSerializer, UserSubscribedPointsOutputSerializer, \
    ClaimCheckPointInputSerializer
from task.models import User, Claim, SubscribedPoints, Checkpoint
from django.db.models import Sum


# Create your views here.


class HelloView(APIView):
    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)


class UserSubscribedPoints(APIView):
    def get(self, request, user_id):
        input_serializer = UserSubscribedPointsInputSerializer(data={'user_id': user_id})
        if input_serializer.is_valid(raise_exception=True):
            subscribed_checkpoints = SubscribedPoints.objects.filter(user_id=user_id) \
                .values_list("checkpoint_id", flat=True)

            min_time_stamp = (datetime.datetime.now() - datetime.timedelta(minutes=15)).timestamp()
            user_claims = Claim.objects.filter(user_id=user_id, checkpoint_id__in=subscribed_checkpoints,
                                               timestamp__gte=min_time_stamp) \
                .values("checkpoint__location_name", "checkpoint__min_number", "state").annotate(
                status_summation=Sum("state"))
            output_serializer = UserSubscribedPointsOutputSerializer(user_claims, many=True)
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
