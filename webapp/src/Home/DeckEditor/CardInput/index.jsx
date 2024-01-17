

function CardInput({deckString, setDeckString}) {

    const handleClick = (e) => {
        setDeckString(e.target.value)
    }

    const placeholder = "1 Card Name"

    return (
        <div className='card-input-container'>
            <textarea className='card-input' 
                value={deckString}
                onChange={handleClick}
                placeholder={placeholder}
            />
        </div>
    );
}

export default CardInput;