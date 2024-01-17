import { Button } from "react-bootstrap";

function NewDeck ({source, createDeck}) {
    const handleClick = () => {
        createDeck(source);
    }
    return (
        <Button onClick={handleClick}>Add Deck</Button>
    )
}

export default NewDeck;