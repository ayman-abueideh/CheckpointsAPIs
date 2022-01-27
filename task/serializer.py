from rest_framework import serializers


class UserIdSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()


class UserSubscribedPointsOutputSerializer(serializers.Serializer):
    checkpoint__location_name = serializers.CharField()
    status = serializers.SerializerMethodField()

    def get_status(self, claim):
        number_of_open = claim.get("status_summation")
        if number_of_open >= claim.get("checkpoint__min_number"):
            return "open"
        else:
            return "close"


class ClaimCheckPointInputSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    checkpoint_id = serializers.IntegerField()
    state = serializers.BooleanField()