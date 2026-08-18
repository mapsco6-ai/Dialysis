from rest_framework import serializers

from .models import StockMovement, Supplier, SupplyItem, SupplyStock


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")


class SupplyItemSerializer(serializers.ModelSerializer):
    quantity_on_hand = serializers.IntegerField(read_only=True)

    class Meta:
        model = SupplyItem
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")


class SupplyStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplyStock
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")


class StockMovementSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockMovement
        fields = "__all__"
        read_only_fields = ("id", "performed_by", "movement_date", "created_at", "updated_at")
