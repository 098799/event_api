from django.db import models


class Event(models.Model):
    name = models.CharField(max_length=100, blank=True, default="")
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    owner = models.ForeignKey("auth.User", related_name="events", on_delete=models.CASCADE)

    @property
    def timezone(self):
        return self.start_date.tzinfo.zone

    class Meta:
        ordering = ["id"]


class Session(models.Model):
    name = models.CharField(max_length=100, blank=True, default="")
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    speaker = models.CharField(max_length=100, blank=True, default="")
    owner = models.ForeignKey("auth.User", related_name="sessions", on_delete=models.CASCADE)
    event = models.ForeignKey(Event, related_name="sessions", on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ["id"]
