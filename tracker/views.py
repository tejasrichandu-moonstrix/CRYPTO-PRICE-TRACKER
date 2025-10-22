import requests
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.conf import settings
from django.core.cache import cache
from decimal import Decimal
from .models import Cryptocurrency, PriceHistory, SearchHistory
from .forms import CryptocurrencySearchForm

CACHE_TIMEOUT = 60  # Cache API response for 60 seconds

def get_crypto_data(symbol):
    """
    Fetch cryptocurrency data from CoinAPI with caching
    """
    cache_key = f"crypto_{symbol}"
    cached_data = cache.get(cache_key)
    if cached_data:
        return cached_data

    url = f"{settings.COINAPI_URL}/exchangerate/{symbol}/USD"
    headers = {'X-CoinAPI-Key': settings.COINAPI_KEY}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        cache.set(cache_key, data, CACHE_TIMEOUT)
        return data
    except requests.RequestException as e:
        print(f"CoinAPI Error: {e}")
        return None

def populate_cryptocurrencies():
    popular_cryptos = [
        {'symbol': 'BTC', 'name': 'Bitcoin'},
        {'symbol': 'ETH', 'name': 'Ethereum'},
        {'symbol': 'BNB', 'name': 'Binance Coin'},
        {'symbol': 'XRP', 'name': 'Ripple'},
        {'symbol': 'SOL', 'name': 'Solana'},
        {'symbol': 'ADA', 'name': 'Cardano'},
        {'symbol': 'DOGE', 'name': 'Dogecoin'},
        {'symbol': 'MATIC', 'name': 'Polygon'},
        {'symbol': 'LTC', 'name': 'Litecoin'},
        {'symbol': 'LINK', 'name': 'Chainlink'},
    ]
    for crypto in popular_cryptos:
        Cryptocurrency.objects.get_or_create(
            coin_id=crypto['symbol'],
            defaults={'name': crypto['name'], 'symbol': crypto['symbol']}
        )

def index(request):
    if not Cryptocurrency.objects.exists():
        populate_cryptocurrencies()

    form = CryptocurrencySearchForm()
    crypto_data = None
    selected_crypto = None

    if request.method == 'POST':
        form = CryptocurrencySearchForm(request.POST)
        if form.is_valid():
            selected_crypto = form.cleaned_data['cryptocurrency']
            api_data = get_crypto_data(selected_crypto.coin_id)

            if api_data and 'rate' in api_data:
                rate = api_data['rate']

                PriceHistory.objects.create(
                    cryptocurrency=selected_crypto,
                    price_usd=Decimal(str(rate))
                )

                session_key = request.session.session_key
                if not session_key:
                    request.session.create()
                    session_key = request.session.session_key

                SearchHistory.objects.create(
                    user=request.user if request.user.is_authenticated else None,
                    cryptocurrency=selected_crypto,
                    session_key=session_key
                )

                crypto_data = {
                    'name': selected_crypto.name,
                    'symbol': selected_crypto.symbol,
                    'price': rate
                }
            else:
                messages.error(request, 'Failed to fetch cryptocurrency data. Please try again.')

    session_key = request.session.session_key
    if request.user.is_authenticated:
        recent_searches = SearchHistory.objects.filter(user=request.user)[:5]
    else:
        recent_searches = SearchHistory.objects.filter(session_key=session_key)[:5] if session_key else []

    context = {
        'form': form,
        'crypto_data': crypto_data,
        'selected_crypto': selected_crypto,
        'recent_searches': recent_searches
    }

    return render(request, 'tracker/index.html', context)

def price_history(request, crypto_id):
    cryptocurrency = get_object_or_404(Cryptocurrency, id=crypto_id)
    history = PriceHistory.objects.filter(cryptocurrency=cryptocurrency)[:20]
    context = {'cryptocurrency': cryptocurrency, 'history': history}
    return render(request, 'tracker/history.html', context)

def api_refresh_price(request, crypto_id):
    if request.method == 'POST':
        cryptocurrency = get_object_or_404(Cryptocurrency, id=crypto_id)
        api_data = get_crypto_data(cryptocurrency.coin_id)

        if api_data and 'rate' in api_data:
            rate = api_data['rate']
            PriceHistory.objects.create(cryptocurrency=cryptocurrency, price_usd=Decimal(str(rate)))

            return JsonResponse({'success': True, 'data': {'price': rate}})
        return JsonResponse({'success': False, 'error': 'Failed to fetch data'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})
