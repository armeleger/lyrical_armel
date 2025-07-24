const token = 'YtshLNbLI2N_hOOY0W4YTq7xRb9x5JmXCAYHaBx3mQaPEduKDP7-XIWZU9gH6Vu-'; // Replace this

document.getElementById('lyrics-form').addEventListener('submit', async function(e) {
  e.preventDefault();

  const artist = document.getElementById('artist').value.trim();
  const title = document.getElementById('title').value.trim();
  const output = document.getElementById('output');

  output.innerHTML = 'Searching on Genius...';

  try {
    const query = `${artist} ${title}`;
    const res = await fetch(`https://api.genius.com/search?q=${encodeURIComponent(query)}`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });

    const json = await res.json();
    const hits = json.response.hits;

    if (hits.length === 0) throw new Error('No lyrics found');

    const song = hits[0].result;
    output.innerHTML = `
      <h2>${song.full_title}</h2>
      <a href="${song.url}" target="_blank">🔗 View Lyrics on Genius</a>
      <br><img src="${song.song_art_image_thumbnail_url}" alt="Album art">
    `;
  } catch (err) {
    output.innerHTML = `<p style="color:red;">Error: ${err.message}</p>`;
  }
});