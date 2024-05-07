from rest_framework import serializers
from .models import Vendor,PO,Performance


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'

class POSerializer(serializers.ModelSerializer):
    class Meta:
        model = PO
        fields = '__all__'

class PerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performance
        fields = '__all__'