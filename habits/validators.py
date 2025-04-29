from datetime import timedelta

from django.core.exceptions import ValidationError


def validate_time_to_complete(value):
    if value > timedelta(seconds=120):
        raise ValidationError("Время на выполнение не должно превышать 120 секунд.")


def validate_period(value):
    if value < 1 or value > 7:
        raise ValidationError("Периодичность должна быть от 1 до 7 дней.")


def validate_habit(instance):
    errors = {}

    if instance.reward and instance.related_habit:
        errors["reward"] = (
            "Нельзя одновременно указывать вознаграждение и связанную привычку."
        )
        errors["related_habit"] = (
            "Нельзя одновременно указывать вознаграждение и связанную привычку."
        )

    if instance.related_habit and not instance.related_habit.pleasant_habit:
        errors["related_habit"] = (
            "В связанные привычки можно выбирать только приятные привычки."
        )

    if instance.pleasant_habit:
        if instance.reward:
            errors["reward"] = "У приятной привычки не может быть вознаграждения."
        if instance.related_habit:
            errors["related_habit"] = (
                "У приятной привычки не может быть связанной привычки."
            )
    if errors:
        raise ValidationError(errors)
