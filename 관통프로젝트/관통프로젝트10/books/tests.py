import json
import os
from types import SimpleNamespace
from unittest.mock import patch

from django.core.cache import cache
from django.test import Client, TestCase
from django.urls import reverse
from openai import OpenAIError

from .models import Book, Category


class RecommendationTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        fiction = Category.objects.create(name='소설')
        essay = Category.objects.create(name='에세이')
        cls.reference = cls.create_book(fiction, '우주 여행', '은하와 별을 탐험하는 여행', 9)
        cls.related = cls.create_book(fiction, '은하 탐험', '은하와 별을 탐험하는 기록', 8)
        cls.same_genre = cls.create_book(fiction, '도시 편지', '도시에서 만난 사람들', 10)
        cls.other_genre = cls.create_book(essay, '정원 일기', '식물을 돌보는 방법', 7)

    @staticmethod
    def create_book(category, title, description, rating):
        return Book.objects.create(
            category=category, title=title, description=description,
            author=f'{title} 저자', pub_date='2026-01-01', customer_review_rank=rating,
        )

    def setUp(self):
        self.url = reverse('books:recommendations', args=[self.reference.pk])
        cache.clear()
        self.addCleanup(cache.clear)

    def test_detail_form_posts_with_csrf_and_returns_local_recommendations(self):
        client = Client(enforce_csrf_checks=True)
        detail = client.get(reverse('books:detail', args=[self.reference.pk]))
        self.assertContains(detail, f'action="{self.url}"')
        self.assertEqual(client.post(self.url).status_code, 403)
        token = client.cookies['csrftoken'].value

        with patch.dict(os.environ, {'GMS_KEY': ''}):
            response = client.post(self.url, {'csrfmiddlewaretoken': token})

        html = response.json()['html']
        self.assertIn('장르, 저자, 책 소개', html)
        self.assertLess(html.index(self.related.title), html.index(self.same_genre.title))
        self.assertNotIn(self.reference.title, html)

    @patch.dict(os.environ, {'GMS_KEY': 'test-key', 'GMS_URL': 'https://gms.example/v1'})
    @patch('books.recommendations.OpenAI')
    def test_ai_reorders_valid_candidates_and_caches_the_result(self, openai):
        completion = openai.return_value.__enter__.return_value.chat.completions.create
        ids = [self.other_genre.pk, self.related.pk, self.same_genre.pk]
        completion.return_value = self.completion_for(ids)

        html = self.client.post(self.url).json()['html']
        self.assertIn('AI가 책의 주제', html)
        self.assertLess(html.index(self.other_genre.title), html.index(self.related.title))
        self.assertEqual(self.client.post(self.url).json()['html'], html)
        completion.assert_called_once()
        payload = json.loads(completion.call_args.kwargs['messages'][1]['content'])
        self.assertEqual(payload['reference']['id'], self.reference.pk)
        self.assertCountEqual([book['id'] for book in payload['candidates']], ids)

    @patch.dict(os.environ, {'GMS_KEY': 'test-key', 'GMS_URL': 'https://gms.example/v1'})
    @patch('books.recommendations.OpenAI')
    def test_invalid_ai_response_and_api_error_use_local_ranking(self, openai):
        completion = openai.return_value.__enter__.return_value.chat.completions.create
        invalid_responses = [
            self.completion_for([self.reference.pk, self.related.pk, self.related.pk]),
            OpenAIError('GMS unavailable'),
        ]
        completion.side_effect = invalid_responses

        with self.assertLogs('books.recommendations', level='WARNING'):
            for failure in ('invalid IDs', 'API error'):
                with self.subTest(failure=failure):
                    cache.clear()
                    html = self.client.post(self.url).json()['html']
                    self.assertIn('장르, 저자, 책 소개', html)
                    self.assertLess(html.index(self.related.title), html.index(self.same_genre.title))
                    self.assertNotIn(self.reference.title, html)

    def test_empty_catalog_results_and_endpoint_methods(self):
        Book.objects.exclude(pk=self.reference.pk).delete()
        self.assertIn('추천할 다른 도서가 아직 없습니다.', self.client.post(self.url).json()['html'])
        self.assertEqual(self.client.get(self.url).status_code, 405)
        missing = reverse('books:recommendations', args=[self.reference.pk + 100])
        self.assertEqual(self.client.post(missing).status_code, 404)

    @staticmethod
    def completion_for(ids):
        message = SimpleNamespace(content=json.dumps({'book_ids': ids}))
        return SimpleNamespace(choices=[SimpleNamespace(message=message)])
