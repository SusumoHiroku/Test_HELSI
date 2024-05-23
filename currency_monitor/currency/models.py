from django.db import models


class Currency(models.Model):
    code_a = models.CharField(max_length=10)
    code_b = models.CharField(max_length=10)
    name_a = models.CharField(max_length=50, blank=True, null=True)
    name_b = models.CharField(max_length=50, blank=True, null=True)
    alpha3_a = models.CharField(max_length=5, blank=True, null=True)
    alpha3_b = models.CharField(max_length=5, blank=True, null=True)
    is_monitored = models.BooleanField(default=False)


    class Meta:
        unique_together = ('code_a', 'code_b')

    def __str__(self):
        return f"{self.code_a}/{self.code_b} - {self.name_a}/{self.name_b}"


class Rate(models.Model):
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    rate_buy = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    rate_sell = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    rate_cross = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    date = models.DateTimeField()

    def __str__(self):
        return f"{self.currency} - {self.date}"
