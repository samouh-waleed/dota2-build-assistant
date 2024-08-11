import axios from 'axios'

const API_BASE_URL = 'http://your-api-url'

const api = axios.create({
  baseURL: API_BASE_URL,
})

// Api for getting the build recomendations
export async function fetchBuild() {
  const response = await api.get('/build')
  return response.data
}