

const form = document.getElementById('lyrics-form');
const output = document.getElementById('output');

form.addEventListener('submit', async (e) => {
  e.preventDefault();

  const artist = document.getElementById('artist').value.trim();
  const title = document.getElementById('title').value.trim();

  if (!artist || !title) return;

  output.innerHTML = '<em>Searching on Genius...</em>';
  form.querySelector('button').disabled = true;

  try {
    const query = `${artist} ${title}`;
    const res = await fetch(`/api/lyrics?query=${encodeURIComponent(query)}`);

    if (!res.ok) throw new Error('Network error');

    const json = await res.json();
    const hits = json.response.hits;

    if (hits.length === 0) throw new Error('No lyrics found');

    const song = hits[0].result;
    output.innerHTML = `
      <h2>${song.full_title}</h2>
      <a href="${song.url}" target="_blank" rel="noopener">🔗 View Lyrics on Genius</a>
      <br><img src="${song.song_art_image_thumbnail_url}" alt="Album art" />
    `;
  } catch (err) {
    output.innerHTML = `<p style="color: #ff4081;">${err.message}</p>`;
  } finally {
    form.querySelector('button').disabled = false;
  }
});
