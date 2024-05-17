import Home from './Home'
import './App.css'
import CollectionProvider from './Home/CollectionContext'
import NavigationBar from './NavigationBar'


function App() {

  return (
    <>
      <CollectionProvider>
        <NavigationBar />
        <div className='container'>
          <Home />  
        </div>
      </CollectionProvider>
    </>
  )
}

export default App
