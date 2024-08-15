from django.urls import path
from django.contrib import admin
from .views import register_voter, voter_login, voter_dashboard, election_commission_dashboard, election_commissioner_login, election_not_active, logout_view, ConstituencyVoteCountView, ElectionResultsView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register_voter, name='register_voter'),
    path('login/', voter_login, name='login'),
    path('voter_dashboard/', voter_dashboard, name='voter_dashboard'),
    path('election_commission_dashboard/', election_commission_dashboard, name='election_commission_dashboard'),
    path('logout/', logout_view, name='logout'),
    path('election_commission_officer_login/', election_commissioner_login, name='election_commission_officer_login'),
    path('gevs/constituency/<str:constituency_details>/', ConstituencyVoteCountView.as_view(), name='constituency_vote_count'),
    path('gevs/results/', ElectionResultsView.as_view(), name='election_results'),
    path('election_not_active/', election_not_active, name='election_not_active'),
]
