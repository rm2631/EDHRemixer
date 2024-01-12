import axiosConfig from '@/axiosConfig';

function OutputColumn({sourceDecks, targetDecks}) {
    const disabled = sourceDecks.length === 0 || targetDecks.length === 0;

    // Flatten all decks into a list of cards and add the deck name to each card
    const sourceFormatted = sourceDecks.map(deck => {
        return deck.cards.map(card => {
            return {
                ...card,
                deck: deck.deck
            }
        })
    }).flat()

    const targetDecksFormatted = targetDecks.map(deck => {
        return deck.cards.map(card => {
            return {
                ...card,
                deck: deck.deck
            }
        })
    }).flat()

    const body = {
        "source" : sourceFormatted,
        "target" : targetDecksFormatted
    }

    const handleClick = () => {
        axiosConfig.post('/reshuffle', body)
    }

    return (
        <div className="home-column-container">
            <h2>Output</h2>
            <button disabled={disabled} onClick={handleClick}>
                Reshuffle
            </button>
        </div>
    )
}

export default OutputColumn