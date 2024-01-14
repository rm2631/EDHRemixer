import Home from './Home'
import './App.css'
import DeckProvider from './Home/DeckContext'
import NavigationBar from './NavigationBar'


function App() {

  return (
    <>
      <DeckProvider>
        <NavigationBar />
        <div className='container'>
          <Home />  
        </div>
      </DeckProvider>
    </>
  )
}

export default App
