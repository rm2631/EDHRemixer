function Deck({deck, setSelectedDeckId}) {

    const handleClick = () => {
        setSelectedDeckId(deck.deck_id);
    }

    return (
        <button className='deck-select-btn' onClick={handleClick}>
            {deck.deck_name}
        </button>
    )
}

export default Deck