from __future__ import unicode_literals
from django.db import models
import re, bcrypt

NAME_REGEX = re.compile(r'^[a-zA-Z\s]+$')
USERNAME_REGEX = re.compile(r'^[\w\s]+$')
SPACE_REGEX = re.compile('.*\s')

class UserManager(models.Manager):
    def validate_reg(self, input):
        errors = []
        name = input['name']
        username = input['username']
        pw = input['pw']
        pw_conf = input['pw_confirm']
        if not name or name.isspace():
            errors.append(("Please enter your name!","name"))
        elif len(name) < 3 or not NAME_REGEX.match(name):
            errors.append(("Name is invalid!","name"))
        if not username or username.isspace():
            errors.append(("Please enter your username!","username"))
        elif len(username) < 3 or not USERNAME_REGEX.match(username):
            errors.append(("Username is invalid!","username"))
        elif self.filter(username__iexact=username).exists():
            errors.append(("Username already exists!","register"))
        if not pw or pw.isspace():
            errors.append(("Please create a new password.","pw"))
        elif SPACE_REGEX.match(pw) or len(pw) < 8:
            errors.append(("Please create a new password as per the criteria.","pw"))
        if not pw == pw_conf:
            errors.append(("The passwords entered don't match.","confirm"))

        if errors:
            return (False, errors)
        else:
            hashed = bcrypt.hashpw(pw.encode(), bcrypt.gensalt())
            user = self.create(name=name, username=username, pw_hash=hashed)
            return (True, user)

    def validate_log(self, input):
        errors = []
        user = User.objects.filter(username=input['username'])
        if user.exists():
            hashed_pw = user[0].pw_hash.encode()
            input_pw = input['pw'].encode()
            if bcrypt.checkpw(input_pw, hashed_pw):
                return (True, user[0])
            else:
                errors.append(("Incorrect password!","login_pw"))
        else:
            errors.append(("Username doesn't exist!","login_user"))
        return (False, errors)

class User(models.Model):
    name = models.CharField(max_length=55)
    username = models.CharField(max_length=55)
    pw_hash = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __unicode__(self):
        return self.name
