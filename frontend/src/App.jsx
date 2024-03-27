import { useState, useEffect } from 'react'
import MangaList from './MangaList'
import './App.css'

function App() {
  // Create a state variable to store the list of mangas
  const [mangas, setMangas] = useState([])

  useEffect(() => {
    // Fetch the list of mangas as soon as the component is mounted
    fetchMangas()
  }, [])

  const fetchMangas = async () => {
    // Fetch the list of mangas from the backend
    const response = await fetch("http://127.0.0.1:5000/mangas")
    // Convert the response to JSON
    const data = await response.json()
    setMangas(data.mangas)
    console.log(data.mangas)
  }
  return <MangaList mangas={mangas} />
}

export default App
