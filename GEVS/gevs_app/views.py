from django.contrib import messages  # Import messages module
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import Voter, ElectionCommissionOfficer, Election, ElectionResult, Constituency, Candidate
from .forms import VoterRegistrationForm, LoginForm, VoteForm, ElectionCommissionLoginForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import JsonResponse
from django.views import View
from .models import ElectionResult

def register_voter(request):
    if request.method == 'POST':
        form = VoterRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = VoterRegistrationForm()
    return render(request, 'gevs_app/register_voter.html', {'form': form})

def voter_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('voter_dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
            print('Invalid credentials!')
    else:
        form = LoginForm()
    return render(request, 'gevs_app/login.html', {'form': form})

def voter_dashboard(request):
    if request.user.is_authenticated:
        election = Election.objects.first() 
        if not election.is_active:
            messages.error(request, 'Election is not active. You cannot cast your vote.')
            return render(request, 'gevs_app/election_not_active.html')
        voter = Voter.objects.get(pk=request.user.pk)
        candidates = Candidate.objects.all()
        if request.method == 'POST':
            form = VoteForm(request.POST)
            if form.is_valid():
                candidate = form.cleaned_data['candidate']
                voter.vote(candidate)
                election_result, created = ElectionResult.objects.get_or_create(
                    candidate=candidate,
                    constituency=candidate.constituency
                )
                election_result.vote_count += 1
                election_result.save()
                return redirect('logout')
        else:
            form = VoteForm()

        return render(request, 'gevs_app/voter_dashboard.html', {'form': form, 'candidates': candidates})
    else:
        return redirect('login')



def election_commissioner_login(request):
    if request.method == 'POST':
        form = ElectionCommissionLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user and user.username == 'election@shangrila.gov.sr' and user.check_password('dummypassword'):
                login(request, user)
                print('Login successful!')
                return HttpResponseRedirect(reverse('election_commission_dashboard'))
            else:
                messages.error(request, 'Invalid username or password.')
                print('Invalid credentials!')
    else:
        form = ElectionCommissionLoginForm()

    return render(request, 'gevs_app/election_commision_officer_login.html', {'form': form})

def election_commission_dashboard(request):
    election = Election.objects.first()  
    results = ElectionResult.objects.all()

    party_results = {}  

    for result in results:
        party_name = result.candidate.party.name
        if party_name not in party_results:
            party_results[party_name] = 0
        party_results[party_name] += result.vote_count

    if request.method == 'POST':
        if 'start_election' in request.POST:
            election.is_active = True
            election.save()
            messages.success(request, 'Election started successfully.')
        elif 'end_election' in request.POST:
            election.is_active = False
            election.save()
            messages.success(request, 'Election ended successfully.')
            # Pass the request object to declare_results
            declare_results(request, party_results)
        return redirect('election_commission_dashboard')

    return render(request, 'gevs_app/election_commission_dashboard.html', {'election': election, 'results': results, 'party_results': party_results})

def declare_results(request, party_results):
    total_seats = sum(party_results.values())

    winner_party = max(party_results, key=party_results.get)
    winner_vote_count = party_results[winner_party]

    if winner_vote_count > total_seats / 2:
        messages.success(request, f'The winner is {winner_party} with {winner_vote_count} votes.')
    else:
        messages.success(request, 'Hung Parliament. No party secured an overall majority.')
    for party, vote_count in party_results.items():
        if party != winner_party:
            messages.info(request, f'{party} received {vote_count} votes.')


def logout_view(request):
    logout(request)
    return render(request, 'gevs_app/logout.html')

def election_not_active(request):
    logout(request)
    return render(request, 'gevs_app/election_not_active.html')

class ConstituencyVoteCountView(View):
    def get(self, request, constituency_details):
        results = ElectionResult.objects.filter(constituency__name=constituency_details)

        #JSON response
        response_data = {
            "constituency": constituency_details,
            "result": [
                {
                    "name": result.candidate.name,
                    "party": result.candidate.party.name,
                    "vote": result.vote_count,
                }
                for result in results
            ],
        }

        return JsonResponse(response_data)

from collections import defaultdict

class ElectionResultsView(View):
    def get(self, request):
        election = Election.objects.first()
        all_results = ElectionResult.objects.all()
        party_results = defaultdict(int)
        for result in all_results:
            party_name = result.candidate.party.name
            party_results[party_name] += result.vote_count
        winner = max(party_results, key=party_results.get)
        seats = [{"party": party, "seat": count} for party, count in party_results.items()]
        status = "Completed" if not election.is_active else "Pending"

        if status == "Completed":
            if all(count == seats[0]["seat"] for party, count in party_results.items()):
                winner = "Hung Parliament"

        response_data = {
            "status": status,
            "winner": winner if status == "Completed" else "Not Declared-Ongoing Election",
            "seats": seats,
        }

        return JsonResponse(response_data)
