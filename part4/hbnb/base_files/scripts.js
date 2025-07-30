/* global alert, confirm */
function parseJwt (token) {
  try {
    const payload = token.split('.')[1];
    return JSON.parse(atob(payload));
  } catch (e) {
    return null;
  }
}

function getCookie (name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  return parts.length === 2 ? parts.pop().split(';').shift() : null;
}

function logout () {
  document.cookie = 'token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
  window.location.href = 'login.html';
}

document.addEventListener('DOMContentLoaded', () => {
  const token = getCookie('token');
  const payload = parseJwt(token);

  const userMenu = document.getElementById('user-menu');
  const userButton = document.getElementById('user-name-button');
  const logoutLink = document.getElementById('logout-link');
  const dropdownWelcome = document.getElementById('dropdown-welcome');
  const isMyPlacesPage = window.location.pathname.includes('my-places.html');

  if (isMyPlacesPage) {
    const token = getCookie('token');
    const payload = parseJwt(token);

    if (!token || !payload?.sub) {
      window.location.href = 'index.html';
    } else {
      fetchMyPlaces(token);
    }
  }

  const loginButton = document.getElementById('login-button');

  if (token && payload?.first_name) {
    const fullName = payload.first_name;
    if (dropdownWelcome) dropdownWelcome.textContent = `Welcome, ${fullName}`;
    if (userMenu) userMenu.style.display = 'inline-block';
    if (loginButton) loginButton.remove();
  } else {
    const isPlacePage = window.location.pathname.includes('place.html');
    if (loginButton && !isPlacePage) {
      loginButton.style.display = 'inline-block';
    } else if (loginButton && isPlacePage) {
      loginButton.remove();
    }
  }

  userButton?.addEventListener('click', (e) => {
    e.stopPropagation();
    userMenu.classList.toggle('show');
  });

  window.addEventListener('click', (e) => {
    if (!userMenu.contains(e.target)) {
      userMenu.classList.remove('show');
    }
  });

  logoutLink?.addEventListener('click', (e) => {
    e.preventDefault();
    logout();
  });

  checkAuthentication();

  const loginForm = document.getElementById('login-form');
  if (loginForm) {
    loginForm.addEventListener('submit', async (event) => {
      event.preventDefault();
      const email = document.getElementById('login-email')?.value.trim();
      const password = document.getElementById('login-password')?.value;
      if (!email || !password) return alert('Please enter both email and password.');
      try {
        await loginUser(email, password);
      } catch (error) {
        console.error('Login error:', error);
        alert('An unexpected error occurred.');
      }
    });
  }

  const registerForm = document.getElementById('register-form');
  if (registerForm) {
    registerForm.addEventListener('submit', async (event) => {
      event.preventDefault();
      const firstName = document.getElementById('first-name')?.value.trim();
      const lastName = document.getElementById('last-name')?.value.trim();
      const email = document.getElementById('register-email')?.value.trim();
      const password = document.getElementById('register-password')?.value;

      if (!firstName || !lastName || !email || !password) {
        return alert('All fields are required for registration.');
      }

      try {
        const response = await fetch('http://127.0.0.1:5000/api/v1/users/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ first_name: firstName, last_name: lastName, email, password })
        });

        if (response.ok) {
          const result = await response.json();
          alert(`✅ Welcome ${result.first_name}, your account was created!`);
          window.location.href = 'login.html';
        } else {
          const errorData = await response.json();
          alert(`❌ Registration failed: ${errorData.message || response.statusText}`);
        }
      } catch (error) {
        console.error('Registration error:', error);
        alert('Unexpected error during registration.');
      }
    });
  }

  const placeId = getPlaceIdFromURL();
  const placeDetailsSection = document.getElementById('place-details');
  const addReviewSection = document.getElementById('add-review');
  const reviewForm = document.getElementById('review-form');

  if (placeDetailsSection && placeId) {
    if (addReviewSection) {
      addReviewSection.style.display = token ? 'block' : 'none';
    }
    fetchPlaceDetails(token, placeId);
  }

  if (reviewForm && token && placeId) {
    reviewForm.addEventListener('submit', async (event) => {
      event.preventDefault();
      const reviewText = document.getElementById('review-text')?.value.trim();
      const ratingValue = parseInt(document.getElementById('review-rating')?.value, 10);
      if (!reviewText || isNaN(ratingValue)) {
        return alert('Please fill out both the review and the rating.');
      }

      try {
        const response = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}/reviews`, {
          method: 'POST',
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ text: reviewText, rating: ratingValue })
        });

        if (response.ok) {
          alert('Review submitted successfully!');
          reviewForm.reset();
          fetchPlaceDetails(token, placeId);
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

  const priceFilter = document.getElementById('price-filter');
  if (priceFilter) {
    priceFilter.addEventListener('change', handlePriceFilter);
  }
});

async function loginUser (email, password) {
  const response = await fetch('http://127.0.0.1:5000/api/v1/auth/login', {
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

function checkAuthentication () {
  const token = getCookie('token');
  const createButton = document.querySelector('.create-button');

  if (token) {
    if (createButton) createButton.style.display = 'inline-block';
    fetchPlaces(token);
  } else {
    if (createButton) createButton.style.display = 'none';
  }
}

async function fetchPlaces (token) {
  try {
    const response = await fetch('http://127.0.0.1:5000/api/v1/places/', {
      method: 'GET',
      headers: { Authorization: `Bearer ${token}` }
    });

    if (!response.ok) throw new Error('Failed to fetch places');
    const places = await response.json();
    displayPlaces(places);
  } catch (error) {
    console.error('Error loading places:', error);
    alert('Could not load places.');
  }
}

function displayPlaces (places) {
  const placesList = document.getElementById('places-list');
  if (!placesList) return;

  placesList.innerHTML = '';

  if (!places || places.length === 0) {
    const message = document.createElement('p');
    message.className = 'no-result';

    if (window.location.pathname.includes('my-places.html')) {
      message.textContent = 'You have not created any places yet.';
    } else {
      message.textContent = 'No places available.';
    }

    placesList.appendChild(message);
    return;
  }

  places.forEach(place => {
    const title = place.name || place.title || 'Untitled';
    const price = place.price || 0;
    const imageUrl = place.image_url || 'images/places.png';

    const placeCard = document.createElement('div');
    placeCard.className = 'place-card';
    placeCard.dataset.price = price;

    placeCard.innerHTML = `
      <img src="${imageUrl}" alt="${title}" class="place-image">
      <h2 class="place-title">${title}</h2>
      <p class="place-price">Price per night: $${price}</p>
      <a class="details-button btn view-button" href="place.html?id=${place.id}">View Details</a>
    `;
    placesList.appendChild(placeCard);
  });
}

function handlePriceFilter (event) {
  const selectedValue = event.target.value;
  const cards = document.querySelectorAll('#places-list .place-card');

  cards.forEach(card => {
    const price = parseFloat(card.dataset.price);
    card.style.display = (selectedValue === 'all' || price <= parseFloat(selectedValue)) ? 'block' : 'none';
  });
}

function getPlaceIdFromURL () {
  const params = new URLSearchParams(window.location.search);
  return params.get('id');
}

async function fetchPlaceDetails (token, placeId) {
  const headers = token ? { Authorization: `Bearer ${token}` } : {};

  try {
    const response = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}`, {
      method: 'GET',
      headers
    });

    if (!response.ok) throw new Error('Failed to fetch place details');
    const place = await response.json();

    displayPlaceDetails(place);

    const reviewResponse = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}/reviews`, {
      method: 'GET',
      headers
    });

    const reviews = reviewResponse.ok ? await reviewResponse.json() : [];
    displayReviews(reviews);
  } catch (error) {
    console.error('Error loading place details:', error);
    alert('Could not load place details.');
  }
}

function displayPlaceDetails (place) {
  const container = document.getElementById('place-details');
  if (!container) return;

  const title = place.title || 'Untitled Place';
  const host = place.owner?.first_name + ' ' + place.owner?.last_name || 'Unknown';
  const description = place.description || 'No description available.';
  const price = typeof place.price === 'number' ? place.price.toFixed(2) : 'N/A';
  const amenities = place.amenities || [];

  container.innerHTML = `
    <h1 class="place-name">${title}</h1>
    <div class="place-box">
      <p><strong>Host:</strong> ${host}</p>
      <p><strong>Price per night:</strong> $${price}</p>
      <p><strong>Description:</strong> ${description}</p>
      <p><strong>Amenities:</strong> ${amenities.map(a => a.name).join(', ') || 'None'}</p>
    </div>
    <h2 class="review-title">Reviews</h2>
    <div class="reviews-container"></div>
  `;

  const token = getCookie('token');
  const payload = parseJwt(token);
  const userId = payload?.sub;
  const isAdmin = payload?.is_admin;

  const addReviewSection = document.getElementById('add-review');
  if (token && place.owner?.id === userId && addReviewSection) {
    addReviewSection.style.display = 'none';
  }

  if (token && (isAdmin || place.owner?.id === userId)) {
    const deleteButton = document.createElement('button');
    deleteButton.className = 'delete-place-btn';
    deleteButton.innerHTML = '🗑️ Delete this place';

    deleteButton.addEventListener('click', async () => {
      if (!confirm('Are you sure you want to delete this place?')) return;
      try {
        const res = await fetch(`http://127.0.0.1:5000/api/v1/places/${place.id}`, {
          method: 'DELETE',
          headers: { Authorization: `Bearer ${token}` }
        });
        if (res.ok) {
          alert('✅ Place deleted');
          window.location.href = 'index.html';
        } else {
          const err = await res.json();
          alert(`Error: ${err.message || 'Failed to delete place'}`);
        }
      } catch (err) {
        console.error('Error deleting place:', err);
        alert('Network error while deleting place.');
      }
    });

    const actionBar = document.createElement('div');
    actionBar.className = 'action-bar';
    actionBar.appendChild(deleteButton);

    const main = document.querySelector('main');
    if (main) {
      main.insertBefore(actionBar, main.firstChild);
    }
  }
}
function displayReviews (reviews) {
  const reviewSection = document.querySelector('.reviews-container');
  if (!reviewSection) return;
  reviewSection.innerHTML = '';

  if (!reviews.length) {
    reviewSection.innerHTML = '<p class="no-review">No reviews yet.</p>';
    return;
  }

  const token = getCookie('token');
  const payload = parseJwt(token);
  const currentUserId = payload?.sub;
  const isAdmin = payload?.is_admin;

  reviews.forEach(review => {
    const card = document.createElement('div');
    card.className = 'review-card';

    const canDelete = review.user_id === currentUserId || isAdmin;
    card.innerHTML = `
      <p><strong>${review.user_name || 'Anonymous'}:</strong></p>
      <p>${review.text}</p>
      ${review.rating ? `<p>Rating: ${'★'.repeat(review.rating)}${'☆'.repeat(5 - review.rating)}</p>` : ''}
      ${canDelete ? `<button class="delete-btn" data-id="${review.id}"><i class="fas fa-trash-alt"></i> Delete</button>` : ''}
    `;

    if (canDelete) {
      const deleteBtn = card.querySelector('.delete-btn');
      deleteBtn.addEventListener('click', async () => {
        if (!confirm('Are you sure you want to delete this review?')) return;
        try {
          const res = await fetch(`http://127.0.0.1:5000/api/v1/reviews/${review.id}`, {
            method: 'DELETE',
            headers: { Authorization: `Bearer ${token}` }
          });
          if (res.ok) {
            alert('Review deleted successfully');
            fetchPlaceDetails(token, getPlaceIdFromURL());
          } else {
            const err = await res.json();
            alert(`Error: ${err.error || 'Failed to delete review'}`);
          }
        } catch (e) {
          console.error('Delete error:', e);
          alert('Unexpected error during deletion.');
        }
      });
    }

    reviewSection.appendChild(card);
  });
}

async function fetchMyPlaces (token) {
  try {
    const response = await fetch('http://127.0.0.1:5000/api/v1/places/user/me', {
      method: 'GET',
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    if (response.status === 401) {
      window.location.href = 'login.html';
      return;
    }

    if (!response.ok) throw new Error('Failed to fetch user places');
    const places = await response.json();
    displayPlaces(places);
  } catch (error) {
    console.error('Error loading user places:', error);
    const placesList = document.getElementById('places-list');
    if (placesList) {
      placesList.innerHTML = '<p class="no-result">Failed to load your places.</p>';
    }
  }
}
