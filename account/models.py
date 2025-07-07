from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password
from cryptography.fernet import Fernet

import base64
from KitGS.settings import FERNET_KEY


class GamAccount(models.Model):
    username = models.CharField(max_length=100, unique=True)
    gam_password = models.CharField(max_length=1000)
    desktop_ip = models.CharField(max_length=20)
    email = models.EmailField(null=True, blank=True)
    phone_num = models.CharField(max_length=11, null=True, blank=True)

    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)

    def set_password(self, raw_password):
        """Encrypts and stores the password."""
        fernet = Fernet(FERNET_KEY)
        encrypted = fernet.encrypt(raw_password.encode())
        self.gam_password = 'enc_' + encrypted.decode()

    def get_password(self):
        """Decrypts and returns the original password."""
        if self.gam_password.startswith('enc_'):
            encrypted = self.gam_password[4:].encode()
            fernet = Fernet(FERNET_KEY)
            return fernet.decrypt(encrypted).decode()
        return self.gam_password

    def save(self, *args, **kwargs):
        """Ensure password is encrypted only once."""
        if not self.gam_password.startswith('enc_'):
            self.set_password(self.gam_password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username
