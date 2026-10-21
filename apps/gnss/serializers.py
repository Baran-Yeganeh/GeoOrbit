from rest_framework import serializers
from .models import Mission, Receiver, SatelliteSystem, ProcessingReport



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
    satellite_systems = SatelliteSystemSerializer(many=True, read_only=True)

    receiver_id = serializers.PrimaryKeyRelatedField(
        source='receiver',
        queryset=Receiver.objects.all(),
        required=False,
        allow_null=True,
        write_only=True
    )

    satellite_system_ids = serializers.PrimaryKeyRelatedField(
        source='satellite_systems',
        queryset=SatelliteSystem.objects.all(),
        many=True,
        required=False,
        write_only=True
    )
    class Meta:
        model = Mission
        fields = '__all__'

class ProcessingReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessingReport
        fields = '__all__'
