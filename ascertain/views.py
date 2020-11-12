from rest_framework import generics
from ascertain.serializers import WhoIsOperatorSerializer


class WhoIsOperatorDetailView(generics.RetrieveAPIView):
    """
    Вью для возврата респонса с оператором определенным по MSISDN.
    """
    lookup_url_kwarg = 'msisdn'
    serializer_class = WhoIsOperatorSerializer
    model = serializer_class.Meta.model

