import CardInput from "./CardInput";
import SubmitButton from "./SubmitButton";
import { useState } from "react";


function DeckEditor({selectedDeck, updateDeck, deleteDeck, setSelectedDeckId}) {
  const ObjectToString = (object) => {
      if (!object) return null;
      return `${object.quantity} ${object.card_text}`
  }
      
  const stringToObject = (string) => {
      const quantity = string.match(/^\d+x? /)
      const card_text = string.replace(/^\d+x? /, '')
      if (!card_text) return null;
      return {quantity: quantity ? +quantity[0].replace(/x? /, '') : 1, card_text: card_text}
  }

  const cardList = selectedDeck.cards  || [];// array of card objects
  const [deckString, setDeckString] = useState(cardList.map(card => ObjectToString(card)).join('\n'));


  const updateCardList = () => {
      const newCardList = deckString.split('\n').map(card_text => (stringToObject(card_text)))
      const newDeck = {...selectedDeck, cards: newCardList}
      updateDeck(selectedDeck.source, newDeck)
  }

  const deck_name = selectedDeck.deck_name;
  const source = selectedDeck.source;

  const updateDeckName = (e) => {
    const newDeck = {...selectedDeck, deck_name: e.target.value};
    updateDeck(source, newDeck);
  }

  return (
    <div className="deck-editor-container">
      <h2>Deck Editor</h2>
      <input type="text" placeholder="Deck Name" value={deck_name} onChange={updateDeckName} />
      <CardInput deckString={deckString} setDeckString={setDeckString} />
      <SubmitButton updateCardList={updateCardList} setSelectedDeckId={setSelectedDeckId} />
    </div>
  );
}

export default DeckEditor;

