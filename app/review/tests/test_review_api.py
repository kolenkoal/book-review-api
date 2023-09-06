"""
Creating tests for review API.
"""
from django.test import TestCase

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

from rest_framework.test import APIClient

from core import models
from review.serializers import ReviewSerializer

REVIEWS_URL = reverse('review:review-list')


def detail_url(review_id):
    return reverse('review:review-detail', args=[review_id])


def create_user(**params):
    return get_user_model().objects.create_user(**params)


def create_review(user, **payload):
    book = models.Book.objects.create(
        user=user,
        title='Invasion',
        description='A real book based on real occasions',
        total_pages=246,
        published_date='2022-08-22'
    )
    author = models.Author.objects.create(
        user=user,
        first_name='Alexey',
        second_name='Mahnish'
    )

    genre = models.Genre.objects.create(
        user=user,
        name='Detective'
    )

    book.author.add(author)
    book.genres.add(genre)

    review = models.Review.objects.create(
        review='That book was so breathtaking. '
               'I read it during one evening and liked it very much!',
        user=user,
        book=book,
        rating=9,
    )

    return review


class PrivateReviewAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_user(
            email='user@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_reviews(self):
        create_review(user=self.user)

        res = self.client.get(REVIEWS_URL)

        authors = models.Review.objects.all().order_by('-id')
        serializer = ReviewSerializer(authors, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_update_review(self):
        """Test updating a review."""
        review = create_review(user=self.user)
        payload = {'review': 'I did not like that book at all.'
                             ' I was reading it very slow because of the '
                             'language the author used',
                   'rating': 3
                   }

        url = detail_url(review.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        review.refresh_from_db()
        self.assertEqual(review.rating, payload['rating'])

    def test_delete_review(self):
        """Test deleting a review."""
        review = create_review(user=self.user)

        url = detail_url(review.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(models.Review.objects.filter(id=review.id).exists())
