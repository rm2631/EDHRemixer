import Home from './Home'
import './App.css'
import DeckProvider from './Home/DeckContext'

function App() {

  return (
    <>
      <DeckProvider>
        <div className='container'>
          <Home />  
        </div>
      </DeckProvider>
    </>
  )
}

export default App
