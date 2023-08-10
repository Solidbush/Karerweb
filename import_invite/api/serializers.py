from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from core.api.serializers import CarSerializer, DriverSerializer
from core.models import Karer
from import_invite.models import OrgImportInvite, get_invite
from marketplace.api.serializers import ProductSerializer


class InviteShowSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    product = ProductSerializer(read_only=True)
    car = CarSerializer(read_only=True)
    driver = DriverSerializer(read_only=True)
    weight = serializers.FloatField(read_only=True)
    status = serializers.CharField(read_only=True)


class InviteCheckSerializer(serializers.Serializer):
    status = serializers.BooleanField(read_only=True)
    invite = InviteShowSerializer(read_only=True, required=False)
    plate = serializers.CharField(write_only=True)
    karer = serializers.SlugRelatedField("slug", queryset=Karer.objects.all(), write_only=True)

    def validate(self, attrs):
        plate: str = attrs.get("plate")
        karer: Karer = attrs.get('karer')
        invite = OrgImportInvite.check_plate(plate, karer.slug)
        accept_statuses = ["payed"]
        if invite.status not in accept_statuses:
            raise ValidationError({"invite": f"Invite status is {invite.status}. Mest be {', '.join(accept_statuses)}"})
        return {
            "status": bool(invite),
            "invite": invite
        }


class InviteDoneSerializer(serializers.Serializer):
    invite = serializers.UUIDField(write_only=True)
    weight = serializers.FloatField(write_only=True)
    invite_data = InviteShowSerializer(read_only=True, required=False)

    def validate_invite(self, value):
        invite = get_invite(value)
        if not invite:
            raise ValidationError({"invite_id": ["Invite not found"]})
        accept_statuses = ["payed"]
        if invite.status not in accept_statuses:
            raise ValidationError({"invite": [f"Invite status is {invite.status}. "
                                              f"Must be {', '.join(accept_statuses)}"]})
        return invite

    def validate(self, attrs):
        invite = attrs.get('invite')
        weight = attrs.get('weight')
        if invite.weight < weight - invite.weight * 0.05:
            raise ValidationError({"weight": "Weight much more then in invite"})
        if invite.weight > weight + invite.weight * 0.05:
            invite_model = type(invite)
            invite_model.objects.create(
                order=invite.order, product=invite.product, car=invite.car,
                driver=invite.driver, weight=invite.weight - weight,
                status=invite.status, position=invite.position + 1
            )
            invite.weight = weight
        invite.finish_at = timezone.now()
        invite.status = "finished"
        invite.save()
        return {"invite_data": invite}
