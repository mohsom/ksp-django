from django.test import TestCase
from django.urls import reverse

from .models import Task


class TodoTests(TestCase):
    def test_empty_list(self):
        self.assertContains(self.client.get(reverse('task_list')), 'Задач поки немає')

    def test_add_toggle_delete(self):
        self.client.post(reverse('task_list'), {'title': 'Learn Django'})
        task = Task.objects.get()
        self.assertFalse(task.done)
        self.client.post(reverse('task_toggle', args=[task.pk]))
        task.refresh_from_db()
        self.assertTrue(task.done)
        self.client.post(reverse('task_delete', args=[task.pk]))
        self.assertEqual(Task.objects.count(), 0)

    def test_empty_title_rejected(self):
        r = self.client.post(reverse('task_list'), {'title': ''})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(Task.objects.count(), 0)

    def test_actions_require_post_and_404(self):
        task = Task.objects.create(title='x')
        self.assertEqual(self.client.get(reverse('task_delete', args=[task.pk])).status_code, 405)
        self.assertEqual(self.client.post(reverse('task_toggle', args=[999])).status_code, 404)
