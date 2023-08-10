from django.core.validators import MinValueValidator
from django.utils import timezone
import uuid
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from core.api.serializers import CarSerializer, DriverSerializer
from core.models import Karer, Organization, Car, Driver, User
from invite.models import ClientInvite, OrgInvite, get_invite, OrgOrder
from marketplace.api.serializers import ProductSerializer
from marketplace.models import Product


class InviteShowSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    product = ProductSerializer(read_only=True)
    car = CarSerializer(read_only=True)
    driver = DriverSerializer(read_only=True)
    weight = serializers.FloatField(read_only=True)
    status = serializers.CharField(read_only=True)


class LegalEntityStatementSerializer(serializers.Serializer):
    id = serializers.UUIDField(default=uuid.uuid4)
    karer = serializers.SlugRelatedField("slug", queryset=Karer.objects.all(), write_only=True)
    desc = serializers.CharField(write_only=True)
    organization = serializers.SlugRelatedField("name", queryset=Organization.objects.all(), write_only=True)
    product = serializers.SlugRelatedField("id", queryset=Product.objects.all(), write_only=True)
    car = serializers.SlugRelatedField("number", queryset=Car.objects.all(), write_only=True)
    driver = serializers.SlugRelatedField("name", queryset=Driver.objects.all(), write_only=True)
    weight = serializers.FloatField(write_only=True, validators=[MinValueValidator(1)])

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['user'] = request.user
        else:
            validated_data['user'] = None

        OrgOrder.objects.create(
            id=validated_data['id'],
            karer=validated_data['karer'],
            desc=validated_data['desc'],
            organization=validated_data['organization'],
            user=validated_data['user']
        )
        OrgInvite.objects.create(
            order_id=validated_data['id'],
            product=validated_data['product'],
            car=validated_data['car'],
            driver=validated_data['driver'],
            weight=validated_data['weight'],
            position=1
        )

        return validated_data


class InviteCheckSerializer(serializers.Serializer):
    status = serializers.BooleanField(read_only=True)
    invite = InviteShowSerializer(read_only=True, required=False)
    plate = serializers.CharField(write_only=True)
    karer = serializers.SlugRelatedField("slug", queryset=Karer.objects.all(), write_only=True)

    def validate(self, attrs):
        plate: str = attrs.get("plate")
        karer: Karer = attrs.get('karer')
        invite = OrgInvite.check_plate(plate, karer.slug)
        if not invite:
            invite = ClientInvite.check_plate(plate, karer.slug)
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
