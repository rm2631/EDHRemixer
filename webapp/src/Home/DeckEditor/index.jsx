import CardInput from "./CardInput";
import SubmitButton from "./SubmitButton";
import { useState } from "react";


function DeckEditor({selectedDeck, updateDeck, deleteDeck, setSelectedDeckId}) {
  const ObjectToString = (object) => {
      if (!object) return null;
      return `${object.quantity} ${object.card_name}`
  }
      
  const stringToObject = (string) => {
      if (!string) return null;
      const quantity = string.match(/^\d+x? /)
      let card_name = string.replace(/^\d+x? /, '')
      const END_CHARACTERS_LIST = ['(', ')', '!', '?']
      // Strip all after end characters
      END_CHARACTERS_LIST.forEach(character => {
          const index = card_name.indexOf(character);
          if (index !== -1) card_name = card_name.slice(0, index);
      })
      card_name = card_name.trim();
      if (!card_name) return null;
      return {
        quantity: quantity ? +quantity[0].replace(/x? /, '') : 1, 
        card_name: card_name
      }
  }

  const cardList = selectedDeck.cards  || [];// array of card objects
  const [deckString, setDeckString] = useState(cardList.map(card => ObjectToString(card)).join('\n'));


  const updateCardList = () => {
      const newCardList = deckString
      .split('\n').map(card_name => (stringToObject(card_name)))
      .filter(card => card);
      const newDeck = {...selectedDeck, cards: newCardList}
      updateDeck(selectedDeck.source, newDeck)
  }

  const deck = selectedDeck.deck;
  const source = selectedDeck.source;

  const updateDeckName = (e) => {
    const newDeck = {...selectedDeck, deck: e.target.value};
    updateDeck(source, newDeck);
  }

  return (
    <div className="deck-editor-container">
      <h2>Deck Editor</h2>
      <input type="text" placeholder="Deck Name" value={deck} onChange={updateDeckName} />
      <CardInput deckString={deckString} setDeckString={setDeckString} />
      <SubmitButton updateCardList={updateCardList} setSelectedDeckId={setSelectedDeckId} />
    </div>
  );
}

export default DeckEditor;

