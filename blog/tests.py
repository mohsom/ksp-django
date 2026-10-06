from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Post


class BlogTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('tester', password='pass12345')
        self.published = Post.objects.create(
            author=self.user, title='Pub', text='t', published_date=timezone.now())
        self.draft = Post.objects.create(author=self.user, title='Draft', text='t')

    def test_list_shows_only_published(self):
        r = self.client.get(reverse('post_list'))
        self.assertContains(r, 'Pub')
        self.assertNotContains(r, 'Draft')

    def test_detail_404(self):
        self.assertEqual(self.client.get(reverse('post_detail', args=[999])).status_code, 404)

    def test_login_required(self):
        for name, args in [('post_new', []), ('post_edit', [self.draft.pk]), ('post_draft_list', [])]:
            r = self.client.get(reverse(name, args=args))
            self.assertEqual(r.status_code, 302)
            self.assertIn('/accounts/login/', r['Location'])

    def test_create_publish_delete(self):
        self.client.login(username='tester', password='pass12345')
        r = self.client.post(reverse('post_new'), {'title': 'New', 'text': 'body'})
        post = Post.objects.get(title='New')
        self.assertRedirects(r, reverse('post_detail', args=[post.pk]))
        self.assertIsNone(post.published_date)
        self.client.post(reverse('post_publish', args=[post.pk]))
        post.refresh_from_db()
        self.assertIsNotNone(post.published_date)
        self.client.post(reverse('post_remove', args=[post.pk]))
        self.assertFalse(Post.objects.filter(pk=post.pk).exists())

    def test_publish_and_remove_require_post(self):
        self.client.login(username='tester', password='pass12345')
        self.assertEqual(self.client.get(reverse('post_remove', args=[self.draft.pk])).status_code, 405)
