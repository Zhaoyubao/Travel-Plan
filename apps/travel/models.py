from __future__ import unicode_literals
from django.db import models
from ..login_register.models import User
from datetime import datetime

class TravelManager(models.Manager):
    def validate_travel(self, input):
        errors = []
        dest = input['destination']
        plan = input['plan']
        date_from = input['date_from']
        date_to = input['date_to']
        if not dest or dest.isspace():
            errors.append("Please enter the destination!")
        if not plan or plan.isspace():
            errors.append("Please enter the plan!")
        if not date_from:
            errors.append("Please select your travel date from!")
        if not date_to:
            errors.append("Please select your travel date to!")
        if date_from and date_to:
            date_delta = (datetime.now() - datetime.strptime(date_from, '%Y-%m-%d')).days
            trip_delta = (datetime.strptime(date_to, '%Y-%m-%d') - datetime.strptime(date_from, '%Y-%m-%d')).days
            if date_delta >= 0:
                errors.append("Travel dates should be future-dated!")
            if trip_delta < 0:
                errors.append('Travel date to should not be before the Travel date from!')
        if errors:
            return (False, errors)
        u = User.objects.get(id=request.session['user'])
        self.create(destination=dest, plan=plan, date_from=date_from, date_to=date_to, user=u)
        return (True, "Trip added Successfully!")


class Travel(models.Model):
    destination = models.CharField(max_length=55)
    plan = models.TextField()
    date_from = models.DateField()
    date_to = models.DateField()
    users = models.ManyToManyField(User, related_name='travels')
    user = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TravelManager()

    def __unicode__(self):
        return self.destination
