from django.db import models


class Session(models.Model):
    name = models.CharField(max_length=100, blank=True, default="")
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    speaker = models.CharField(max_length=100, blank=True, default="")
    owner = models.ForeignKey("auth.User", related_name="sessions", on_delete=models.CASCADE)

    class Meta:
        ordering = ["start_date"]


class TimeZone(models.Model):
    """Time zone abbreviation class.

    For more information, consult https://en.wikipedia.org/wiki/List_of_time_zone_abbreviations.
    """

    abbreviation = models.CharField(max_length=5, blank=False, default="")  # at most 5 characters
    name = models.CharField(max_length=5, blank=False, default="")
    utc_offset = models.FloatField()

    class Meta:
        ordering = ["utc_offset"]


class Event(models.Model):
    name = models.CharField(max_length=100, blank=True, default="")
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    timezone = TimeZone()
    speaker = models.CharField(max_length=100, blank=True, default="")

    class Meta:
        ordering = ["start_date"]
