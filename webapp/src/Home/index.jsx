import './styles/base.css'
import DeckList from './DeckList';
import OutputColumn from './OutputColumn';
import { useDeck } from "../Home/DeckContext";
import DeckEditor from './DeckEditor';

function Home() {

    const {
        sourceDecks,
        targetDecks,
        createDeck,
        updateDeck,
        deleteDeck,
        setSelectedDeckId,
        selectedDeck,
    } = useDeck();



    const deckListDisplay = (
        <>
            <DeckList source={true} />
            <DeckList source={false} />
            <OutputColumn sourceDecks={sourceDecks} targetDecks={targetDecks}/>
        </>
    )

    const deckEditDisplay = (
        <>
            <DeckEditor selectedDeck={selectedDeck} updateDeck={updateDeck} deleteDeck={deleteDeck} setSelectedDeckId={setSelectedDeckId}/>
        </>
    )

    const displayed = selectedDeck ? deckEditDisplay : deckListDisplay;

    return (
        <div className='home-container'>
            {displayed}
        </div>
    );
}

export default Home