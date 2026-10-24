from rest_framework import serializers
from .models import Mission, Receiver, SatelliteSystem, ProcessingReport
from django.utils import timezone



class ReceiverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receiver
        fields = '__all__'


class SatelliteSystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SatelliteSystem
        fields = '__all__'


class MissionSerializer(serializers.ModelSerializer):
    receiver = ReceiverSerializer(read_only=True)
    satellite_systems = SatelliteSystemSerializer(many=True,read_only=True,)

    receiver_id = serializers.PrimaryKeyRelatedField(
        source='receiver',
        queryset=Receiver.objects.all(),
        required=False,
        allow_null=True,
        write_only=True,
    )

    satellite_system_ids = serializers.PrimaryKeyRelatedField(
        source='satellite_systems',
        queryset=SatelliteSystem.objects.all(),
        many=True,
        required=False,
        write_only=True,
    )

    class Meta:
        model = Mission
        fields = '__all__'


    def validate(self, attrs):
        now = timezone.now()

        if self.instance is None:
            start_date = attrs.get("surveying_start_date", now)
            end_date = attrs.get("surveying_end_date", now)
        else:
            start_date = attrs.get(
                "surveying_start_date",
                self.instance.surveying_start_date,
            )
            end_date = attrs.get(
                "surveying_end_date",
                self.instance.surveying_end_date,
            )

        if start_date and end_date and end_date < start_date:
            raise serializers.ValidationError({
                "surveying_end_date":
                    "End date cannot be before the start date."
            })

        return attrs



class ProcessingReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessingReport
        fields = '__all__'
