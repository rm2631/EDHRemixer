import Deck from "./Deck";
import { useDeck } from "../DeckContext";
import NewDeck from "./NewDeck";


function DeckList({ source }) {
    
    const {
        sourceDecks,
        targetDecks,
        createDeck,
        updateDeck,
        deleteDeck,
        setSelectedDeckId,
        selectedDeck,
    } = useDeck();

    const header = source ? 'Source deck' : 'Target deck';
    const deck = source ? sourceDecks : targetDecks; 
    
    return (
        <div className='home-column-container'>
            <h2>{header}</h2>
            <div className="deck-list">
                <NewDeck source={source} createDeck={createDeck} />
                {
                    deck.map((deck, index) => {
                        return (
                            <Deck key={index} deck={deck} setSelectedDeckId={setSelectedDeckId}/>
                        )
                    })
                }
            </div>
        </div>
    );
}

export default DeckList;