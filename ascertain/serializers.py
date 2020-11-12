from rest_framework import serializers

from ascertain import models


class WhoIsOperatorSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для "WhoIsOperatorDetailView".
    """
# Еще вернуть номер
    class Meta:
        model = models.TelephoneNumbersModel
        fields = ('operator', 'region', )
        read_only_fields = fields
