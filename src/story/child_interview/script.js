const emojiContainer = document.querySelector('.emoji-container');
const emojis = ['😀', '😍', '🥳', '🐱', '🌈', '🍕', '🚀', '🎉', '🌸', '🐶'];
const maxEmojis = 50;
const maxClickableEmojis = 10;

// Function to generate a random emoji
function getRandomEmoji() {
  return emojis[Math.floor(Math.random() * emojis.length)];
}

// Function to populate the emoji container
function populateEmojis(count) {
  emojiContainer.innerHTML = '';
  for (let i = 0; i < count; i++) {
    const emoji = document.createElement('div');
    emoji.className = 'emoji';
    emoji.innerText = getRandomEmoji();
    emojiContainer.appendChild(emoji);
  }
}

// Event listener for emoji clicks
let clickableEmojis = maxClickableEmojis;
emojiContainer.addEventListener('click', (event) => {
  if (event.target.classList.contains('emoji') && clickableEmojis > 0) {
    event.target.style.display = 'none';
    clickableEmojis--;
    if (clickableEmojis === 0) {
      emojiContainer.innerHTML = '';
      for (let i = 0; i < maxClickableEmojis; i++) {
        const emoji = document.createElement('div');
        emoji.className = 'emoji';
        emoji.innerText = emojis[i];
        emojiContainer.appendChild(emoji);
      }
    }
  }
});

// Initialize the page
populateEmojis(maxEmojis);
