from django.db import models
from django.contrib.auth.models import User


RATE = (
    (5.0, 5.0),
    (4.0, 4.0),
    (3.0, 3.0),
    (2.0, 2.0),
    (1.0, 1.0),
)


class Comment(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    rating = models.DecimalField(null=True, blank=True, max_digits=9, decimal_places=1)

    def __str__(self):
        return f'Comment nr {self.id}'
