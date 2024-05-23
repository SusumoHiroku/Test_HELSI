from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone
from django.http import HttpResponse
from .models import Currency, Rate
from .serializers import CurrencySerializer, AvailableListCurrencySerializer, CreateCurrencySerializer, \
    RateHistorySerializer


class CurrencyViewSet(viewsets.ViewSet):

    def list(self, request):
        currencies = Currency.objects.all()
        serializer = CurrencySerializer(currencies, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def available(self, request):
        available_currencies = Currency.objects.filter(is_monitored=False).values('alpha3_a', 'name_a').distinct()
        serializer = AvailableListCurrencySerializer(available_currencies, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = CreateCurrencySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put'])
    def toggle(self, request, pk=None):
        try:
            currency = Currency.objects.get(pk=pk)
            previous_state = currency.is_monitored
            currency.is_monitored = not currency.is_monitored
            currency.save()

            if previous_state != currency.is_monitored:
                if currency.is_monitored:
                    return Response({'status': 'success', 'message': 'Currency monitoring enabled'},
                                    status=status.HTTP_200_OK)
                else:
                    return Response({'status': 'success', 'message': 'Currency monitoring disabled'},
                                    status=status.HTTP_200_OK)
            else:
                return Response({'status': 'error', 'message': 'Currency monitoring state not changed'},
                                status=status.HTTP_200_OK)

        except Currency.DoesNotExist:
            return Response({'status': 'not found'}, status=status.HTTP_404_NOT_FOUND)


class RateViewSet(viewsets.ViewSet):
    @action(detail=True, methods=['get'], url_path='history/(?P<start_date>[^/.]+)/(?P<end_date>[^/.]+)')
    def history(self, request, pk=None, start_date=None, end_date=None):
        rates = Rate.objects.filter(currency__code_a=pk, date__range=[start_date, end_date])
        serializer = RateHistorySerializer(rates, many=True)
        return Response(serializer.data)
