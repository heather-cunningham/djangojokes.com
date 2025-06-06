window.addEventListener('load', 
  () => {
    if (document.getElementById('like-button')) { // If like button exists
      const likeButton = document.getElementById('like-button');
      const dislikeButton = document.getElementById('dislike-button');

      likeButton.addEventListener('click', () => { register(1); })
      dislikeButton.addEventListener('click', () => { register(-1); })
    }
  }
)


// This essentially opens up the communication gateway between JavaScript and Django. 
// You can then pass JSON data back and forth between the two.
function register(vote) {
  // if (!isAuthenticated) {
  //   const outputDiv = document.getElementById('output');
  //   outputDiv.innerHTML = 'Sorry, only logged-in users can vote.';
  //   return false;
  // }

  const csrfInput =  document.querySelector("input[name='csrfmiddlewaretoken']");
  const csrfToken = csrfInput.value;
  const likes = Number(document.getElementById('likes').innerHTML);
  const dislikes = Number(document.getElementById('dislikes').innerHTML);

  const data = {
    'vote': vote,
    'likes': likes,
    'dislikes': dislikes
  }

  fetch(ajaxURL, 
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken
      },
      body: JSON.stringify(data),
  }
).then(response => response.json())
  .then(
    data => {
      const numVotes = data.dislikes + data.likes;
      let voteText = `${numVotes} vote`;

      if (numVotes !== 1) {
        voteText += 's'
      }
      
      document.getElementById('output').innerHTML = data.msg;
      document.getElementById('likes').innerHTML = data.likes;
      document.getElementById('dislikes').innerHTML = data.dislikes;
      document.getElementById('num-votes').innerHTML = voteText;
    }
  );
}