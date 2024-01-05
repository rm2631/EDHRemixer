

function NewDeck ({source, createDeck}) {
    const handleClick = () => {
        createDeck(source);
    }
    return (
        <button onClick={handleClick}>
            + Create
        </button>
    )
}

export default NewDeck;