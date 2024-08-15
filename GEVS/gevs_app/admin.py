from django.contrib import admin
from .models import Election, Candidate, Party, Constituency, Voter, ElectionResult

# Register your models here.
admin.site.register(Election)
admin.site.register(Candidate)
admin.site.register(Party)
admin.site.register(Constituency)
admin.site.register(Voter)
admin.site.register(ElectionResult)