from django.db import models


class Enum(models.Model):
    title = models.CharField(max_length=64)


class EnumItem(models.Model):
    enum = models.ForeignKey(Enum, related_name="items")
    label = models.CharField(max_length=128)
    value = models.CharField(max_length=128)
