from django.db import models
class Party(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Constituency(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name

class Candidate(models.Model):
    name = models.CharField(max_length=255)
    party = models.ForeignKey(Party, on_delete=models.CASCADE , default='Independent')
    constituency = models.ForeignKey(Constituency, on_delete=models.CASCADE)
    vote_count = models.IntegerField(default=0)
    def __str__(self):
        return self.name

class Voter(models.Model):
    voter_id = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    password = models.CharField(max_length=255)
    constituency = models.ForeignKey(Constituency, on_delete=models.CASCADE)
    unique_voter_code = models.CharField(max_length=8, unique=True)
    has_voted = models.BooleanField(default=False)
    def vote(self, candidate):
        if not self.has_voted:
            self.has_voted = True
            self.save()
            candidate.vote_count += 1
            candidate.save()
        else:
            print("You have already voted!") 
    def __str__(self):
        return self.voter_id

class ElectionCommissionOfficer(models.Model):
    login_name = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)

class ElectionResult(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    constituency = models.ForeignKey(Constituency, on_delete=models.CASCADE)
    vote_count = models.IntegerField(default=0)
    def __str__(self):
        return f"{self.candidate.name} - {self.constituency.name} - Votes: {self.vote_count}"

class Election(models.Model):
    name = models.CharField(max_length=255, default='Default Election')
    is_active = models.BooleanField(default=False)
    def __str__(self):
        return self.name