from rest_framework import serializers

from ascertain import models


class WhoIsOperatorSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для "WhoIsOperatorDetailView".
    """
    number = serializers.ReadOnlyField()

    class Meta:
        model = models.TelephoneNumbersModel
        fields = ('number', 'operator', 'region',)
        read_only_fields = fields
