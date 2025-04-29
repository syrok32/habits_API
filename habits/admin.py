from django.contrib import admin

from habits.models import Habits


# Register your models here.
@admin.register(Habits)
class HabitAdmin(admin.ModelAdmin):
    list_display = ("id", "owner", "action", "place", "pleasant_habit")
