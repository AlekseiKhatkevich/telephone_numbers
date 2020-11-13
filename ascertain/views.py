from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import generics
from rest_framework.exceptions import NotFound, ValidationError

from ascertain.serializers import WhoIsOperatorSerializer
from telephone_numbers import constants, error_messages


@method_decorator(cache_page(constants.DEFAULT_CACHE_TTL), name='get')
class WhoIsOperatorDetailView(generics.RetrieveAPIView):
    """
    Вью для возврата респонса с оператором определенным по MSISDN.
    get_object_or_404 не использовал так как хотел отдать кастомные сообщения об
    ошибках и не хотел делать кастомный exception handler из-за одного view.
    """
    serializer_class = WhoIsOperatorSerializer
    model = serializer_class.Meta.model
    queryset = model.objects.all()

    def get_object(self):
        msisdn_dict = self.kwargs['msisdn']
        ndc = msisdn_dict['ndc']
        sn = msisdn_dict['sn']
        number = msisdn_dict['number']

        try:
            obj = self.model.objects.get(abc_or_def=ndc, numbers_range__contains=sn)
        except self.model.DoesNotExist as err:
            raise NotFound(
                *error_messages.NUMBER_NOT_FOUND,
            ) from err
        except self.model.MultipleObjectsReturned as err:
            raise ValidationError(
                *error_messages.MULTIPLE_NUMBERS,
            ) from err
        else:
            obj.number = number
            return obj





