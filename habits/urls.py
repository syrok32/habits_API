
from django.urls import path
from rest_framework.routers import DefaultRouter

from habits.apps import HabitsConfig
from habits.views import HabitViewSet, PublicHabitsListView, UserHabitsListView

app_name = HabitsConfig.name

router = DefaultRouter()
router.register(r"habits", HabitViewSet, basename="habits")

urlpatterns = [
                  path("habits/public/", PublicHabitsListView.as_view(), name="habits-public"),
                  path("habits/my/", UserHabitsListView.as_view(), name="habits-my"),
              ] + router.urls
