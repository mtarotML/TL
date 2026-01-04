let currentProfile = null;
let isEditing = false;

document.addEventListener("DOMContentLoaded", async () => {
  const token = localStorage.getItem("token");
  if (!token) {
    window.location.href = "/login.html";
    return;
  }

  await loadProfile();

  document.getElementById("profileForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    await saveProfile();
  });
});

async function loadProfile() {
  const token = localStorage.getItem("token");
  const loading = document.getElementById("loading");

  try {
    const res = await fetch("/profile/me", {
      headers: { "Authorization": `Bearer ${token}` }
    });

    if (res.status === 401) {
      localStorage.removeItem("token");
      window.location.href = "/login.html";
      return;
    }

    const data = await res.json();

    loading.style.display = "none";

    if (data.profile_exists) {
      currentProfile = data.profile;
      showProfileView();
    } else {
      document.getElementById("profileForm").style.display = "flex";
      document.getElementById("formTitle").textContent = "Créer mon profil";
    }
  } catch (error) {
    loading.style.display = "none";
    showMessage("Erreur lors du chargement du profil", "error");
  }
}

function showProfileView() {
  const profileView = document.getElementById("profileView");
  const profileData = document.getElementById("profileData");
  
  const genderLabels = {
    "homme": "Homme",
    "femme": "Femme",
    "autre": "Autre"
  };
  
  const lookingForLabels = {
    "homme": "Des hommes",
    "femme": "Des femmes",
    "tous": "Peu importe"
  };

  profileData.innerHTML = `
    <div class="info-row">
      <span class="info-label">Âge</span>
      <span class="info-value">${currentProfile.age} ans</span>
    </div>
    <div class="info-row">
      <span class="info-label">Genre</span>
      <span class="info-value">${genderLabels[currentProfile.gender] || currentProfile.gender}</span>
    </div>
    <div class="info-row">
      <span class="info-label">Recherche</span>
      <span class="info-value">${lookingForLabels[currentProfile.looking_for] || currentProfile.looking_for}</span>
    </div>
    <div class="info-row">
      <span class="info-label">Ville</span>
      <span class="info-value">${currentProfile.city}</span>
    </div>
    <div class="info-row">
      <span class="info-label">Biographie</span>
      <span class="info-value">${currentProfile.bio}</span>
    </div>
    ${currentProfile.photo_url ? `
    <div class="info-row">
      <span class="info-label">Photo</span>
      <span class="info-value"><a href="${currentProfile.photo_url}" target="_blank" style="color: #667eea;">Voir la photo</a></span>
    </div>
    ` : ''}
  `;

  profileView.classList.add("active");
  document.getElementById("profileForm").style.display = "none";
}

function toggleEdit() {
  const profileView = document.getElementById("profileView");
  const profileForm = document.getElementById("profileForm");
  const formTitle = document.getElementById("formTitle");

  profileView.classList.remove("active");
  profileForm.style.display = "flex";
  formTitle.textContent = "Modifier mon profil";
  isEditing = true;

  document.getElementById("age").value = currentProfile.age;
  document.getElementById("gender").value = currentProfile.gender;
  document.getElementById("looking_for").value = currentProfile.looking_for;
  document.getElementById("city").value = currentProfile.city;
  document.getElementById("bio").value = currentProfile.bio;
  document.getElementById("photo_url").value = currentProfile.photo_url || "";
}

async function saveProfile() {
  const token = localStorage.getItem("token");
  const messageDiv = document.getElementById("message");

  const profileData = {
    age: parseInt(document.getElementById("age").value),
    gender: document.getElementById("gender").value,
    looking_for: document.getElementById("looking_for").value,
    city: document.getElementById("city").value,
    bio: document.getElementById("bio").value,
    photo_url: document.getElementById("photo_url").value || null
  };

  try {
    const endpoint = isEditing ? "/profile/update" : "/profile/create";
    const method = isEditing ? "PUT" : "POST";

    const res = await fetch(endpoint, {
      method: method,
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
      },
      body: JSON.stringify(profileData)
    });

    const data = await res.json();

    if (res.ok) {
      showMessage(data.message, "success");
      currentProfile = data.profile;
      isEditing = false;
      setTimeout(() => {
        showProfileView();
        messageDiv.innerHTML = "";
      }, 1500);
    } else {
      showMessage(`Erreur : ${data.detail}`, "error");
    }
  } catch (error) {
    showMessage("Erreur lors de l'enregistrement", "error");
  }
}

function showMessage(text, type) {
  const messageDiv = document.getElementById("message");
  messageDiv.textContent = text;
  messageDiv.className = `message ${type}`;
  messageDiv.style.display = "block";
}

function logout() {
  localStorage.removeItem("token");
  window.location.href = "/";
}