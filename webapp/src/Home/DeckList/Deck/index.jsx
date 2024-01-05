function Deck({deck, setSelectedDeckId}) {

    const handleClick = () => {
        setSelectedDeckId(deck.deck_id);
    }

    return (
        <button onClick={handleClick}>
            {deck.deck_name}
        </button>
    )
}

export default Deck