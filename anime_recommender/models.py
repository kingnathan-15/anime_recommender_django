from django.db import models

class Anime(models.Model):
    anime_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=255)
    genre = models.CharField(max_length=255)
    type = models.CharField(max_length=50)
    episodes = models.PositiveIntegerField(null=True, blank=True)
    rating = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    members = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.type})"


class Predictions(models.Model):
    anime_id = models.ForeignKey(
        Anime,
        to_field='anime_id',
        on_delete=models.CASCADE,
        related_name='ratings'
    )
    prediction = models.CharField()
    pred_assessment = models.BooleanField()

    def __str__(self):
        return self.prediction