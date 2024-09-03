from rest_framework import serializers


class AfterEffectSerializer(serializers.Serializer):
    effect = serializers.CharField()
    effect_args = serializers.ListField(child=serializers.CharField())
    effect_kwargs = serializers.DictField()
