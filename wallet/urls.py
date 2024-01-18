from django.urls import path, include

from wallet.views import WalletView, api_init

urlpatterns = [
    path('init/', api_init,  name='init'),
    path('wallet/', include([
        path('', WalletView.as_view(), name='wallet'),
    #     path('transactions/', None, name='transactions-list'),
    #     path('deposits/', None, name='deposit'),
    #     path('withdrawals', None, name='withdrawals'),
    ])),
]