# Anime Recommender

Small Django project providing anime recommendations using a KNN model.

## Quick start

1. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

If you don't have a `requirements.txt`, install the minimum packages:

```bash
pip install django pandas scikit-learn
```

3. Apply migrations and run server

```bash
python manage.py migrate
python manage.py load_anime anime_recommender/data/anime.csv
python manage.py runserver
```

4. Open the site at http://127.0.0.1:8000/

## Data

- The app expects CSV data under `anime_recommender/data/` named `anime.csv` and `rating.csv`.
- If you want to keep data files out of the repository, confirm `data/` is listed in `.gitignore` (it's commented by default).

## Notes

- Startup initialization that loads CSVs is in `anime_recommender/startup.py`.
- If you see errors about missing CSVs, ensure the files exist at `anime_recommender/data/anime.csv` and `anime_recommender/data/rating.csv`.

## Contributing

Feel free to open issues or submit PRs with improvements.
