# Create your views here.
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from habits.models import Habits
from habits.pagination import MyPagination
from habits.permissions import IsOwnerOrPublic
from habits.serializers import HabitSerializer


class HabitViewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializer
    queryset = Habits.objects.all()
    pagination_class = MyPagination

    print(queryset)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Habits.objects.filter(Q(is_public=True) | Q(owner=user)).distinct()
        return Habits.objects.filter(is_public=True)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.action == "retrieve":
            return [IsOwnerOrPublic()]
        if self.action in ["update", "destroy", "partial_update"]:
            return [IsOwnerOrPublic()]
        if self.action in ["create"]:
            return [IsAuthenticated()]
        if self.action == "list":
            return []
        return super().get_permissions()
