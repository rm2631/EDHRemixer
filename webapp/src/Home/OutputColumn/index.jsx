import axiosConfig from '@/axiosConfig';
import React, {useState} from 'react'
import {Button} from 'react-bootstrap'
import {Card} from 'react-bootstrap'

function OutputColumn({sourceDecks, targetDecks}) {
    const [loading, setLoading] = useState(false);
    const emptyDeckList = sourceDecks.length === 0 || targetDecks.length === 0;
    const emptyDeck = sourceDecks.concat(targetDecks).some(deck => deck.cards.length === 0);

    const disabled = emptyDeckList || emptyDeck;


    const sourceFormatted = sourceDecks.map(deck => {
        return deck.cards.map(card => {
            return {
                ...card,
                deck: deck.deck
            }
        })
    }).flat()

    const targetDecksFormatted = targetDecks.map(deck => {
        return deck.cards.map(card => {
            return {
                ...card,
                deck: deck.deck
            }
        })
    }).flat()

    const body = {
        "source" : sourceFormatted,
        "target" : targetDecksFormatted
    }

    const handleClick = () => {
        setLoading(true);
        //An excel file is downloaded with the reshuffled decks
        axiosConfig.post('/reshuffle', body).then(response => {
            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            const date = new Date();
            link.setAttribute('download', `reshuffled_${date.toISOString()}.xlsx`);
            document.body.appendChild(link);
            link.click();
            link.parentNode.removeChild(link);
    }).finally(() => {
            setLoading(false);
        })
    }


    return (
        <div className="home-column-container">
            <h2>Output</h2>
            <Button disabled={disabled} onClick={handleClick}>
                Reshuffle
                {loading && <span className="spinner-border spinner-border-sm ms-2" role="status" aria-hidden="true"></span>}
            </Button>
            <Card className="mt-2 home-column-card">
                <Card.Title>Instructions</Card.Title>
                <Card.Body>
                    <Card.Text>
                        <ol>
                            <li>Add a deck to the source column, add cards in it.</li>
                            <li>Add a deck to the target column, add cards in it.</li>
                            <li>Click the reshuffle button to download the resulting excel file.</li>
                        </ol>
                    </Card.Text>
                </Card.Body>
            </Card>
        </div>
    )
}

export default OutputColumn