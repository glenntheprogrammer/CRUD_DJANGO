from django.db import models

class Profile(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    bday = models.DateField()

    def __str__(self):
        return self.name

    @staticmethod
    def get_all_records():
        return Profile.objects.all().values()