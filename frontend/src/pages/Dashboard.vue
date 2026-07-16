<template>
  <div class="dashboard-container">
    <!-- Header -->
    <header class="header">
      <div class="header-content">
        <div class="header-right">
          <button @click="logout" class="logout-btn">Logout</button>
        </div>
      </div>
    </header>
    <!-- Main Content -->
    <main class="main-content">
      <div class="content-container">

        <!--Title-->
        <div class="header-center">
          <h2 class="header-tagline">Museum of Articles</h2>
          <p class="header-subtitle">A collection of favourites :)</p>
        </div>

        <!-- Welcome Section -->
        <section class="welcome-section">
          <h4 class="welcome-title">
            Hello {{ user?.username }} 
          </h4>
        </section>

        <!-- Add Form -->
        <div class="add-form">
          <input 
            type="url" 
            v-model="newLinkUrl" 
            placeholder="Paste article link..."
            @keydown.enter="addLink"
          >
          <button @click="addLink" :disabled="isLoading">Add</button>
        </div>

        <!-- Article Grid -->
        <div class="card-grid">
          <div v-for="link in sortedLinks" :key="link.id" class="tile">
            <div class="tile-image">
              <img 
                v-if="link.image" 
                :src="link.image" 
                alt="preview" 
                loading="lazy"
                @error="handleImageError($event, link)"
              >
              <div v-else class="fallback">
                <span>📄</span>
                {{ getHostname(link.url) }}
              </div>
            </div>
            <div class="tile-content">
              <div class="tile-title">
                <a :href="link.url" target="_blank" rel="noopener noreferrer">
                  {{ link.title || link.url }}
                </a>
              </div>
              <div v-if="link.description" class="tile-desc">
                {{ link.description }}
              </div>
              <div class="tile-footer">
                <span class="added-by">Added by {{ link.addedBy || 'anonymous' }}</span>
                <a class="tile-link" :href="link.url" target="_blank" rel="noopener noreferrer">
                  Read
                </a>
              </div>
            </div>
          </div>
        </div>

      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import api from '../services/api'

const router = useRouter()
const authStore = useAuthStore()
const user = authStore.user

const stats = ref({
  total_users: 0,
  new_users_today: 0,
  recent_users: []
})

// Article functionality
const newLinkUrl = ref('')
const isLoading = ref(false)
const links = ref<any[]>([])

const sortedLinks = computed(() => {
  return [...links.value].sort((a, b) => (b.timestamp || 0) - (a.timestamp || 0))
})

const getHostname = (url: string) => {
  try {
    return new URL(url).hostname.replace('www.', '').slice(0, 18)
  } catch (_) {
    return 'article'
  }
}

const handleImageError = (event: Event, link: any) => {
  const img = event.target as HTMLImageElement
  img.style.display = 'none'
  const parent = img.parentElement
  if (parent) {
    const fallback = document.createElement('div')
    fallback.className = 'fallback'
    fallback.innerHTML = `<span>📄</span>${getHostname(link.url)}`
    parent.appendChild(fallback)
  }
}

const fetchMetadata = async (url: string) => {
  try {
    const apiUrl = `https://api.microlink.io/?url=${encodeURIComponent(url)}&meta=title,description,image`
    const response = await fetch(apiUrl)
    if (!response.ok) throw new Error('API error')
    const data = await response.json()
    if (data.status === 'success' && data.data) {
      const meta = data.data
      return {
        title: meta.title || '',
        description: meta.description || '',
        image: meta.image?.url || meta.image || '',
      }
    }
    return null
  } catch (_) {
    return null
  }
}

const fallbackMetadata = (url: string) => {
  try {
    const host = new URL(url).hostname.replace('www.', '')
    return {
      title: host,
      description: `Article from ${host}`,
      image: `https://t0.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=${encodeURIComponent(url)}&size=128`,
    }
  } catch (_) {
    return { title: 'Article', description: 'Shared link', image: '' }
  }
}

const generateId = () => {
  return Date.now().toString(36) + Math.random().toString(36).substring(2, 6)
}

const loadLinks = () => {
  const stored = localStorage.getItem('museum_articles_links')
  if (stored) {
    try {
      const parsed = JSON.parse(stored)
      if (Array.isArray(parsed)) {
        links.value = parsed
        return
      }
    } catch (_) {}
  }
  links.value = []
}

const saveLinks = () => {
  localStorage.setItem('museum_articles_links', JSON.stringify(links.value))
}

const addLink = async () => {
  let cleanUrl = newLinkUrl.value.trim()
  if (!cleanUrl) {
    alert('Please paste a link')
    return
  }
  
  if (!cleanUrl.startsWith('http://') && !cleanUrl.startsWith('https://')) {
    cleanUrl = 'https://' + cleanUrl
  }
  
  try {
    new URL(cleanUrl)
  } catch (_) {
    alert('Please enter a valid URL')
    return
  }

  isLoading.value = true

  try {
    let meta = await fetchMetadata(cleanUrl)
    if (!meta) {
      meta = fallbackMetadata(cleanUrl)
    }

    const newLink = {
      id: generateId(),
      url: cleanUrl,
      title: meta.title || cleanUrl,
      description: meta.description || '',
      image: meta.image || '',
      addedBy: user?.username || 'anonymous',
      timestamp: Date.now(),
    }

    links.value.push(newLink)
    saveLinks()
    newLinkUrl.value = ''
  } catch (error) {
    console.error('Failed to add link:', error)
    alert('Failed to add article. Please try again.')
  } finally {
    isLoading.value = false
  }
}

const logout = async () => {
  await authStore.logout()
  router.push('/login')
}

onMounted(async () => {
  loadLinks()
  try {
    const response = await api.get('dashboard/stats/')
    stats.value = response.data
  } catch (error) {
    console.error('Failed to fetch stats:', error)
  }
})
</script>

<style scoped>
.dashboard-container {
  min-height: 100vh;
  background: #f7fafc;
  min-width: 1024px;
}

.header {
  background: white;
  border-bottom: 1px solid #e2ecf9;
  padding: 0.75rem 2rem;
  display: flex;
  justify-content: flex-end;
}

.header-content {
  width: 100%;
  max-width: 1400px;
  margin: 0 auto;
}

.header-right {
  display: flex;
  justify-content: flex-end;
}

.logout-btn {
  padding: 0.4rem 1.2rem;
  background: #f0f4f8;
  border: 1px solid #dce6f0;
  border-radius: 6px;
  color: #1f4a7a;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 0.8rem;
}

.logout-btn:hover {
  background: #e2ecf9;
}

.main-content {
  padding: 1.5rem 2rem;
  max-width: 1400px;
  margin: 0 auto;
}

.content-container {
  max-width: 1400px;
  margin: 0 auto;
}

.header-center {
  text-align: center;
  margin-bottom: 1.5rem;
}

.header-tagline {
  font-size: 1.8rem;
  color: #0b1e33;
  margin-bottom: 0.15rem;
  font-weight: 600;
}

.header-subtitle {
  color: #5a7a9a;
  font-size: 0.9rem;
}

.welcome-section {
  margin-bottom: 1.5rem;
}

.welcome-title {
  color: #0b1e33;
  font-size: 1rem;
  font-weight: 500;
}

.add-form {
  display: flex;
  gap: 0.5rem;
  max-width: 500px;
  margin-bottom: 1.5rem;
}

.add-form input {
  flex: 1;
  padding: 0.5rem 0.8rem;
  border: 1px solid #dce6f0;
  border-radius: 6px;
  font-size: 0.85rem;
  background: white;
}

.add-form input:focus {
  outline: none;
  border-color: #1f4a7a;
}

.add-form button {
  padding: 0.5rem 1.5rem;
  background: #1f4a7a;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 0.85rem;
  font-weight: 500;
  cursor: pointer;
  white-space: nowrap;
}

.add-form button:hover:not(:disabled) {
  background: #163a5e;
}

.add-form button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.card-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.2rem;
}

.tile {
  background: white;
  border-radius: 10px;
  overflow: hidden;
  border: 1px solid #e2ecf9;
  display: flex;
  flex-direction: column;
  transition: transform 0.2s, box-shadow 0.2s;
}

.tile:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(0,0,0,0.06);
}

.tile-image {
  position: relative;
  width: 100%;
  padding-top: 56.25%;
  background: #dde6f0;
  overflow: hidden;
}

.tile-image img {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.tile-image .fallback {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: #dde6f0;
  color: #2f4b6e;
  font-size: 0.65rem;
}

.tile-image .fallback span {
  font-size: 1.8rem;
  opacity: 0.5;
}

.tile-content {
  padding: 0.6rem 0.8rem 0.8rem;
  display: flex;
  flex-direction: column;
  flex: 1;
}

.tile-title {
  font-size: 0.85rem;
  font-weight: 600;
  color: #0b1e33;
  line-height: 1.3;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  margin-bottom: 0.1rem;
}

.tile-title a {
  color: #0b1e33;
  text-decoration: none;
}

.tile-title a:hover {
  color: #1f4a7a;
}

.tile-desc {
  font-size: 0.75rem;
  color: #3d5a78;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  line-height: 1.4;
  flex: 1;
  margin-top: 0.1rem;
}

.tile-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 0.4rem;
}

.added-by {
  font-size: 0.65rem;
  color: #8a9aaa;
  font-weight: 400;
}

.tile-link {
  display: inline-block;
  background: #eef3f9;
  color: #1f4a7a;
  font-weight: 500;
  font-size: 0.7rem;
  padding: 0.2rem 1rem;
  border-radius: 30px;
  text-decoration: none;
  transition: background 0.2s;
}

.tile-link:hover {
  background: #dce6f0;
}
</style>