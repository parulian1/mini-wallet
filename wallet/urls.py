from django.urls import path, include

from wallet.views import WalletView, api_init, WalletTransactionView, WalletTransactionDepositView, \
    WalletTransactionWithdrawView

urlpatterns = [
    path('init/', api_init,  name='init'),
    path('wallet/', include([
        path('', WalletView.as_view(), name='wallet'),
        path('transactions/', WalletTransactionView.as_view(), name='transactions-list'),
        path('deposits/', WalletTransactionDepositView.as_view(), name='deposit'),
        path('withdrawals/', WalletTransactionWithdrawView.as_view(), name='withdrawals'),
    ])),
]