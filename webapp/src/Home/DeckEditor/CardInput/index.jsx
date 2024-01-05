

function CardInput({deckString, setDeckString}) {

    const handleClick = (e) => {
        setDeckString(e.target.value)
    }

    return (
        <div className='card-input-container'>
            <textarea className='card-input' 
                value={deckString}
                onChange={handleClick}
            />
        </div>
    );
}

export default CardInput;