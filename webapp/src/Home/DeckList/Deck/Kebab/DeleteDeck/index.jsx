import { useDeck } from "../../../../DeckContext";

function DeleteDeck ({source, deck_id}) {

    const {
        sourceDecks,
        targetDecks,
        createDeck,
        updateDeck,
        deleteDeck,
        setSelectedDeckId,
        selectedDeck,
    } = useDeck();

    const handleClick = () => {
        deleteDeck(source, deck_id);
    }

    return (
        <a className="delete-deck-btn" onClick={handleClick}>
            Delete deck
        </a>
    )
}

export default DeleteDeck