import Home from './Home'
import './App.css'
import DeckProvider from './Home/DeckContext'

function App() {

  return (
    <>
      <DeckProvider>
        <Home />  
      </DeckProvider>
    </>
  )
}

export default App
