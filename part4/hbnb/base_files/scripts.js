document.addEventListener('DOMContentLoaded', () => {
  checkAuthentication();

  const loginForm = document.getElementById('login-form');
  const priceFilter = document.getElementById('price-filter');
  const placeDetailsSection = document.getElementById('place-details');
  const reviewForm = document.getElementById('review-form');

  if (loginForm) {
    loginForm.addEventListener('submit', async (event) => {
      event.preventDefault();
      const email = document.getElementById('email').value;
      const password = document.getElementById('password').value;

      if (!email || !password) return alert('Please enter both email and password.');

      try {
        await loginUser(email, password);
      } catch (error) {
        console.error('Login error:', error);
        alert('An unexpected error occurred.');
      }
    });
  }

  else if (placeDetailsSection) {
    const placeId = getPlaceIdFromURL();
    const token = getCookie('token');
    const addReviewSection = document.getElementById('add-review');

    if (addReviewSection) {
      addReviewSection.style.display = token ? 'block' : 'none';
    }

    if (placeId) {
      fetchPlaceDetails(token, placeId);
    }
  }

  else if (reviewForm) {
    const token = getCookie('token');
    const placeId = getPlaceIdFromURL();
    if (!token) window.location.href = 'index.html';

    reviewForm.addEventListener('submit', async (event) => {
      event.preventDefault();
      const reviewText = document.getElementById('review-text').value.trim();
      if (!reviewText) return alert('Please write a review.');

      try {
        const response = await fetch(`http://127.0.0.1:5000//api/v1/places/${placeId}/reviews`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ text: reviewText })
        });

        if (response.ok) {
          alert('Review submitted successfully!');
          reviewForm.reset();
        } else {
          const error = await response.json();
          alert(`Error: ${error.message || 'Failed to submit review'}`);
        }
      } catch (err) {
        console.error('Review error:', err);
        alert('Unexpected error during review submission.');
      }
    });
  }

  else {
    if (priceFilter) priceFilter.addEventListener('change', handlePriceFilter);
  }
});

async function loginUser(email, password) {
  const response = await fetch('http://127.0.0.1:5000//api/v1/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
  });

  if (response.ok) {
    const data = await response.json();
    document.cookie = `token=${data.access_token}; path=/`;
    window.location.href = 'index.html';
  } else {
    const errorData = await response.json();
    alert(`Login failed: ${errorData.message || response.statusText}`);
  }
}

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  return parts.length === 2 ? parts.pop().split(';').shift() : null;
}

function checkAuthentication() {
  const token = getCookie('token');
  const loginLink = document.getElementById('login-link');
  const logoutBtn = document.getElementById('logout-btn');

  if (token) {
    if (loginLink) loginLink.style.display = 'none';
    if (logoutBtn) logoutBtn.style.display = 'inline-block';
    fetchPlaces(token);
  } else {
    if (loginLink) loginLink.style.display = 'inline-block';
    if (logoutBtn) logoutBtn.style.display = 'none';
  }

  if (logoutBtn) {
    logoutBtn.addEventListener('click', () => {
      document.cookie = 'token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
      window.location.href = 'login.html';
    });
  }
}

async function fetchPlaces(token) {
  try {
    const response = await fetch('http://127.0.0.1:5000/api/v1/places', {
      method: 'GET',
      cache: 'no-store',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });

    if (!response.ok) throw new Error('Failed to fetch places');
    const places = await response.json();

    console.log('📦 Places reçues :', places);

    displayPlaces(places);
  } catch (error) {
    console.error('Error loading places:', error);
    alert('Could not load places.');
  }
}

function displayPlaces(places) {
  const placesList = document.getElementById('places-list');
  if (!placesList) return;
  placesList.innerHTML = '';

  if (!places || places.length === 0) {
    const noResult = document.createElement('p');
    noResult.className = 'no-result';
    noResult.textContent = 'No places available.';
    placesList.appendChild(noResult);
    return;
  }

  places.forEach(place => {
    const placeCard = document.createElement('div');
    placeCard.className = 'place-card';
    placeCard.dataset.price = place.price;

    placeCard.innerHTML = `
      <img src="${place.image_url || 'images/default.jpg'}" alt="${place.name}" class="place-image">
      <div class="place-info">
        <h2 class="place-title">${place.name}</h2>
        <p class="place-price">$${place.price} per night</p>
        <a class="details-button" href="place.html?id=${place.id}">View Details</a>
      </div>
    `;
    placesList.appendChild(placeCard);
  });
}

function handlePriceFilter(event) {
  const selectedValue = event.target.value;
  const cards = document.querySelectorAll('#places-list .place-card');

  cards.forEach(card => {
    const price = parseFloat(card.dataset.price);
    if (selectedValue === 'all' || price <= parseFloat(selectedValue)) {
      card.style.display = 'block';
    } else {
      card.style.display = 'none';
    }
  });
}

function getPlaceIdFromURL() {
  const params = new URLSearchParams(window.location.search);
  return params.get('id');
}

async function fetchPlaceDetails(token, placeId) {
  try {
    const headers = token ? { 'Authorization': `Bearer ${token}` } : {};
    const response = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}`, {
      method: 'GET',
      headers
    });

    if (!response.ok) throw new Error('Failed to fetch place details');

    const place = await response.json();
    displayPlaceDetails(place);
  } catch (error) {
    console.error('Error loading place details:', error);
    alert('Could not load place details.');
  }
}

function displayPlaceDetails(place) {
  const container = document.getElementById('place-details');
  if (!container) return;
  container.innerHTML = '';

  const title = document.createElement('h2');
  title.textContent = place.name;

  const description = document.createElement('p');
  description.textContent = place.description;

  const price = document.createElement('p');
  price.textContent = `Price per night: $${place.price_by_night}`;

  const amenities = document.createElement('ul');
  amenities.innerHTML = '<strong>Amenities:</strong>';
  (place.amenities || []).forEach(amenity => {
    const li = document.createElement('li');
    li.textContent = amenity.name;
    amenities.appendChild(li);
  });

  const reviews = document.createElement('div');
  const reviewTitle = document.createElement('h3');
  reviewTitle.textContent = 'Reviews:';
  reviews.appendChild(reviewTitle);

  if (place.reviews && place.reviews.length > 0) {
    place.reviews.forEach(review => {
      const p = document.createElement('p');
      p.innerHTML = `<strong>${review.user_name}</strong>: ${review.text}`;
      reviews.appendChild(p);
    });
  } else {
    const noReview = document.createElement('p');
    noReview.textContent = 'No reviews yet.';
    reviews.appendChild(noReview);
  }

  container.appendChild(title);
  container.appendChild(description);
  container.appendChild(price);
  container.appendChild(amenities);
  container.appendChild(reviews);
}
