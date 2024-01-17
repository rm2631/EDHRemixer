import { Button } from "react-bootstrap";
import { Badge } from 'react-bootstrap'

function NewDeckButton({}) {
    return (
        <div>
            <Button className="deck-select-btn" onClick={handleClick}>{deck.deck}</Button>
            <Badge className="deck-select-badge" variant="secondary">{deck_length}</Badge>
        </div>
    )
}

export default NewDeckButton