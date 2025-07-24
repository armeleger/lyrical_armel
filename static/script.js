async function findLyrics() {
  const artist = document.getElementById('artist').value;
  const title = document.getElementById('title').value;

  const response = await fetch('/search', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ artist, title })
  });

  const resultDiv = document.getElementById('result');
  resultDiv.innerHTML = 'Fetching...';

  if (response.ok) {
    const data = await response.json();
    resultDiv.innerHTML = `
      <h2>${data.full_title}</h2>
      <img src="${data.thumbnail}" alt="Artwork">
      <p><a href="${data.url}" target="_blank">View Lyrics</a></p>
    `;
  } else {
    resultDiv.innerHTML = 'Lyrics not found. Try again.';
  }
}