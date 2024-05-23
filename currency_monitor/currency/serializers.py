from rest_framework import serializers
from .models import Currency, Rate
from django.db.models import Q



class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rate
        fields = ['rate_buy', 'rate_sell', 'rate_cross', 'date']


class RateHistorySerializer(serializers.ModelSerializer):
    currency_name_a = serializers.CharField(source='currency.name_a', read_only=True)
    currency_name_b = serializers.CharField(source='currency.name_b', read_only=True)

    class Meta:
        model = Rate
        fields = ['currency_name_a', 'currency_name_b', 'rate_buy', 'rate_sell', 'rate_cross', 'date']


class CurrencySerializer(serializers.ModelSerializer):
    latest_rate = serializers.SerializerMethodField()

    class Meta:
        model = Currency
        fields = ['name_a', 'alpha3_a', 'name_b', 'alpha3_b', 'latest_rate']

    def get_latest_rate(self, obj):
        rate = Rate.objects.filter(currency=obj).order_by('-date').first()
        if rate:
            return RateSerializer(rate).data
        return None


class AvailableListCurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ['alpha3_a', 'name_a']


class CreateCurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ['code_a', 'name_a', 'alpha3_a']

    def validate_code_a(self, value):
        if not str(value).isdigit():
            raise serializers.ValidationError("Currency code must be a numeric value.")
        return value

    def validate(self, data):
        code_a = data.get('code_a')
        alpha3_a = data.get('alpha3_a')
        if Currency.objects.filter(
                Q(code_a=code_a) | Q(alpha3_a=alpha3_a)
        ).exists():
            raise serializers.ValidationError("Currency with this code or alpha3 already exists.")

        return data

    def create(self, validated_data):
        validated_data['code_b'] = '980'
        validated_data['name_b'] = 'Ukrainian hryvnia'
        validated_data['alpha3_b'] = 'UAH'
        validated_data['is_monitored'] = True
        return super().create(validated_data)
