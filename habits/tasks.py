from datetime import datetime

from celery import shared_task

from habits.models import Habits
from habits.services import send_message


@shared_task
def send_habit_reminders():
    now = datetime.now()
    current_time = now.time()

    habits = Habits.objects.select_related("owner").all()

    for habit in habits:

        user = habit.owner
        if not user.tg_chat_id:
            continue

        if (
            habit.time_at.hour == current_time.hour and habit.time_at.minute == current_time.minute
        ):
            print("s")
            message = f"Пора: {habit.action} в {habit.place}"
            send_message(user.tg_chat_id, message)
