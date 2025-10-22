from django.db import models
from django.contrib.auth.models import User


class Cryptocurrency(models.Model):
    coin_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.symbol.upper()})"

    class Meta:
        ordering = ['name']


class PriceHistory(models.Model):
    cryptocurrency = models.ForeignKey(Cryptocurrency, on_delete=models.CASCADE)
    price_usd = models.DecimalField(max_digits=20, decimal_places=8)
    market_cap = models.BigIntegerField(null=True, blank=True)
    volume_24h = models.BigIntegerField(null=True, blank=True)
    price_change_24h = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.cryptocurrency.name} - ${self.price_usd} at {self.timestamp}"

    class Meta:
        ordering = ['-timestamp']


class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    cryptocurrency = models.ForeignKey(Cryptocurrency, on_delete=models.CASCADE)
    searched_at = models.DateTimeField(auto_now_add=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)

    def __str__(self):
        return f"Search for {self.cryptocurrency.name} at {self.searched_at}"

    class Meta:
        ordering = ['-searched_at']