async function addRecommendationCard(result) {
    const container = document.getElementById('recommendationsList');
    container.innerHTML = ''; // optional: clear previous cards

    const animeList = [];

    for (const id of result.similar_anime_ids) {
        console.log('Fetching anime:', id);

        const response = await fetch(`/api/anime/${id}`);
        if (!response.ok) {
            console.error(`Failed to fetch anime ${id}`);
            continue;
        }

        const anime = await response.json();
        animeList.push(anime);
    }

    animeList.forEach((anime, index) => {
        const card = document.createElement('div');
        card.className = 'card mb-2 recommendation-card';
        card.style.width = '18rem';

        const img = document.createElement('img');
        img.className = 'card-img-top';
        img.src = anime.main_picture?.medium ?? '';
        img.alt = anime.title ?? 'No image';

        const cardBody = document.createElement('div');
        cardBody.className = 'card-body p-2';

        const title = document.createElement('h6');
        title.className = 'card-title mb-1';
        title.textContent = anime.title ?? 'No Title';

        const body = document.createElement('p');
        body.className = 'card-text collapse';
        body.id = `synopsis_${index}`;
        body.textContent = anime.synopsis ?? 'N/A';

        const toggleBtn = document.createElement('button');
        toggleBtn.className = 'btn btn-sm btn-link p-0';
        toggleBtn.textContent = 'More';
        toggleBtn.setAttribute('data-bs-toggle', 'collapse');
        toggleBtn.setAttribute('data-bs-target', `#${body.id}`);

        cardBody.append(title, toggleBtn, body);
        card.append(img, cardBody);
        container.appendChild(card);
    });
}