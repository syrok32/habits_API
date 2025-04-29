from rest_framework import serializers

from habits.models import Habits
from habits.validators import validate_habit, validate_period, validate_time_to_complete


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habits
        fields = "__all__"

    def validate_time_to_complete(self, value):
        validate_time_to_complete(value)
        return value

    def validate_period(self, value):
        validate_period(value)
        return value

    def validate(self, attrs):
        # Для обновления добавляем pk, если есть
        instance = self.instance
        if instance:
            for attr, value in attrs.items():
                setattr(instance, attr, value)
        else:
            instance = Habits(**attrs)

        validate_habit(instance)
        return attrs
