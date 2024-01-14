import axiosConfig from '@/axiosConfig';
import React from 'react'
import {Button} from 'react-bootstrap'

function OutputColumn({sourceDecks, targetDecks}) {

    //TODO: Add a loading state


    const disabled = sourceDecks.length === 0 || targetDecks.length === 0;
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
        //An excel file is downloaded with the reshuffled decks
        axiosConfig.post('/reshuffle', body).then(response => {
            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', 'reshuffled.xlsx');
            document.body.appendChild(link);
            link.click();
            link.parentNode.removeChild(link);
    })}


    return (
        <div className="home-column-container">
            <h2>Output</h2>
            <Button disabled={disabled} onClick={handleClick}>Reshuffle</Button>
        </div>
    )
}

export default OutputColumn