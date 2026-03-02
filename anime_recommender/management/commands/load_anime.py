import csv
from django.core.management.base import BaseCommand
from anime_recommender.models import Anime

class Command(BaseCommand):
    help = 'Load anime and ratings CSV files into the database'
    
    def parse_int(self,value):
        if value in ('', 'Unknown', 'None', None):
            return None
        return int(value)

    def parse_decimal(self, value):
        if value in ('', 'Unknown', 'None', None):
            return None
        return float(value)
    

    def add_arguments(self, parser):
        parser.add_argument(
            'anime_csv',
            type=str,
            help='Path to the anime CSV file'
        )
        parser.add_argument(
            'ratings_csv',
            type=str,
            help='Path to the ratings CSV file'
        )

    def handle(self, *args, **kwargs):
        anime_csv = kwargs['anime_csv']

        # Load Anime data
        with open(anime_csv, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                episodes = self.parse_int(row['episodes'])
                rating = self.parse_decimal(row['rating'])
                members = self.parse_int(row['members'])

                Anime.objects.get_or_create(
                    anime_id=row['anime_id'],
                    defaults={
                        'name': row['name'],
                        'genre': row['genre'],
                        'type': row['type'],
                        'episodes': episodes,
                        'rating': rating,
                        'members': members,
                    }
                )

        self.stdout.write(self.style.SUCCESS('Anime data imported successfully'))

        # # Load Ratings data
        # ratings_to_create = []

        # with open(ratings_csv, newline='', encoding='utf-8') as f:
        #     reader = csv.DictReader(f)
        #     for row in reader:
        #         # Parse values and handle potential None/Null values
        #         user_id = self.parse_int(row['user_id'])
        #         anime_id = self.parse_int(row['anime_id'])
        #         rating = self.parse_int(row['rating'])

        #         # Validation: Only add if we have valid integers
        #         if user_id is not None and anime_id is not None and rating is not None:
        #             ratings_to_create.append(
        #                 Ratings(
        #                     user_id=user_id,
        #                     anime_id=anime_id,
        #                     rating=rating
        #                 )
        #             )

        #         # Batch save every 5,000 rows to keep memory usage low
        #         if len(ratings_to_create) >= 5000:
        #             Ratings.objects.bulk_create(ratings_to_create)
        #             ratings_to_create = [] # Clear the list for the next batch

        # # Save any remaining records
        # if ratings_to_create:
        #     Ratings.objects.bulk_create(ratings_to_create)

        # self.stdout.write(self.style.SUCCESS('Ratings data imported successfully'))