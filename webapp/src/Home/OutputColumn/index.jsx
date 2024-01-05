

function OutputColumn({sourceDecks, targetDecks}) {
    const disabled = sourceDecks.length === 0 || targetDecks.length === 0;

    const body = {
        "source" : sourceDecks,
        "target" : targetDecks
    }

    const handleClick = () => {
        console.log('asd')
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