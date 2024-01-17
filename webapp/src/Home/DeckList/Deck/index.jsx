import { Button } from "react-bootstrap";
import { Badge } from 'react-bootstrap'
import Kebab from "./Kebab";

function Deck({deck, setSelectedDeckId}) {
    const deck_length = deck.cards.reduce((acc, card) => {
        return acc + card.quantity;
    }, 0);

    const handleClick = () => {
        setSelectedDeckId(deck.deck_id);
    }

    return (
        <div className="deck-select-container">
            <Button className="deck-select-btn" onClick={handleClick}>
                <div className="deck-select-btn-text">
                    {deck.deck}
                    <Badge pill className="deck-select-badge" bg="secondary">{deck_length}</Badge>
                </div>
            </Button>
            <div className="kebab-container">
                <Kebab deck={deck} />
            </div>
        </div>
    )
}

export default Deck