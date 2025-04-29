import json
from datetime import timedelta

from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from users.models import User
from habits.models import Habits


class HabitViewSetTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", email="testuser@example.com", password="testpass"
        )
        self.other_user = User.objects.create_user(
            username="otheruser", email="otheruser@example.com", password="otherpass"
        )
        self.habit_private = Habits.objects.create(
            owner=self.user,
            place="Дом",
            time_at="07:00:00",
            action="разминка",
            pleasant_habit="пить кофе",
            period=1,
            time_to_complete=timedelta(seconds=60),
            is_public=False,
        )
        self.habit_public = Habits.objects.create(
            owner=self.user,
            place="Парк",
            time_at="08:00:00",
            action="бег",
            pleasant_habit="слушать музыку",
            period=1,
            time_to_complete=timedelta(seconds=60),
            is_public=True,
        )
        self.list_url = reverse("habits:habits-list")
        self.detail_url = lambda habit_id: reverse(
            "habits:habits-detail", args=[habit_id]
        )

    def test_create_authenticated(self):
        """Тест для создания привычки авторизованным пользователем"""
        self.client.force_authenticate(user=self.user)
        data = {
            "place": "ZAHAE",
            "time_at": "08:30:00",
            "action": "бегать",
            "pleasant_habit": "",  # Допустимо с blank=True
            "period": 2,
            "time_to_complete": "00:02:00",
            "is_public": True,
        }
        response = self.client.post(
            self.list_url, data=json.dumps(data), content_type="application/json"
        )
        print("test_create_authenticated response:", response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["owner"], self.user.id)

    def test_create_with_pleasant_habit_and_invalid_data(self):
        """Тест для проверки валидации pleasant_habit с reward или related_habit"""
        self.client.force_authenticate(user=self.user)
        data = {
            "place": "ZAHAE",
            "time_at": "08:30:00",
            "action": "бегать",
            "pleasant_habit": "кушать сладкое",
            "period": 2,
            "time_to_complete": "00:02:00",
            "is_public": True,
            "reward": "шоколадка",
        }
        response = self.client.post(
            self.list_url, data=json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("reward", response.data)

    def test_create_with_invalid_time_to_complete(self):
        """Тест для проверки валидации time_to_complete (> 120 секунд)"""
        self.client.force_authenticate(user=self.user)
        data = {
            "place": "ZAHAE",
            "time_at": "08:30:00",
            "action": "бегать",
            "pleasant_habit": "",
            "period": 2,
            "time_to_complete": "00:03:00",
            "is_public": True,
        }
        response = self.client.post(
            self.list_url, data=json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("time_to_complete", response.data)

    def test_list_authenticated(self):
        """Тест для получения списка привычек авторизованным пользователем"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        habits = response.data.get("results", response.data)
        habit_ids = [habit["id"] for habit in habits]
        self.assertIn(self.habit_private.id, habit_ids)
        self.assertIn(self.habit_public.id, habit_ids)

    def test_list_unauthenticated(self):
        """Тест для получения списка привычек неавторизованным пользователем"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        habits = response.data.get("results", response.data)
        habit_ids = [habit["id"] for habit in habits]
        self.assertIn(self.habit_public.id, habit_ids)
        self.assertNotIn(self.habit_private.id, habit_ids)

    def test_retrieve_public(self):
        """Тест для получения публичной привычки"""
        response = self.client.get(self.detail_url(self.habit_public.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.habit_public.id)

    def test_retrieve_private_owner(self):
        """Тест для получения личной привычки владельцем"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.detail_url(self.habit_private.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.habit_private.id)

    def test_update_authenticated_owner(self):
        """Тест для обновления привычки владельцем"""
        self.client.force_authenticate(user=self.user)
        data = {
            "place": "Стадион",
            "time_at": "09:00:00",
            "action": "бегать",
            "pleasant_habit": "",  # Допустимо с blank=True
            "period": 3,
            "time_to_complete": "00:01:00",
            "is_public": False,
        }
        response = self.client.put(
            self.detail_url(self.habit_private.id),
            data=json.dumps(data),
            content_type="application/json",
        )
        print("test_update_authenticated_owner response:", response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["place"], "Стадион")

    def test_delete_authenticated_owner(self):
        """Тест для удаления привычки владельцем"""
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.detail_url(self.habit_private.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Habits.objects.filter(id=self.habit_private.id).exists())

    def test_create_with_related_habit(self):
        """Тест для создания привычки со связанной приятной привычкой"""
        self.client.force_authenticate(user=self.user)
        pleasant_habit = Habits.objects.create(
            owner=self.user,
            place="Кухня",
            time_at="06:30:00",
            action="завтрак",
            pleasant_habit="есть фрукты",
            period=1,
            time_to_complete=timedelta(seconds=60),
            is_public=True,
        )
        data = {
            "place": "ZAHAE",
            "time_at": "08:30:00",
            "action": "бегать",
            "pleasant_habit": "",  # Допустимо с blank=True
            "related_habit": pleasant_habit.id,
            "period": 2,
            "time_to_complete": "00:02:00",
            "is_public": True,
        }
        response = self.client.post(
            self.list_url, data=json.dumps(data), content_type="application/json"
        )
        print("test_create_with_related_habit response:", response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["related_habit"], pleasant_habit.id)
