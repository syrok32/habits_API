from django.db import models

from Tracker_habits import settings



# Create your models here.
class Habits(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="habits",
        blank=True,
        null=False,
        verbose_name="создатель привычке",
    )
    place = models.CharField(max_length=30, blank=False, verbose_name="место")
    time_at = models.TimeField(
        auto_now=False, auto_created=False, auto_now_add=False, verbose_name="время"
    )
    action = models.CharField(
        max_length=50, blank=False, null=False, verbose_name="действие"
    )
    pleasant_habit = models.BooleanField(
        default=False, verbose_name="это приятная привычка"
    )
    related_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="related_to",
        verbose_name="связанная привычка",
    )
    period = models.PositiveSmallIntegerField(
        default=1, verbose_name="периодичность (дни)"
    )
    reward = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="вознаграждение"
    )
    time_to_complete = models.DurationField(verbose_name="время на выполнение")
    is_public = models.BooleanField(default=False, verbose_name="публичная привычка")

    class Meta:
        verbose_name = "привычка"
        verbose_name_plural = "привычки"

    def __str__(self):
        return f"{self.action} в {self.time_at} в {self.place}"
