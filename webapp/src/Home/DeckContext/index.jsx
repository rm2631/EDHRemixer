import React, { createContext, useContext, useState, useEffect } from 'react';

// Creating the context
const DeckContext = createContext();

// The provider component that wraps the part of your app that needs access to this context
export const DeckProvider = ({ children }) => {
    const [sourceDecks, setSourceDecks] = useState(JSON.parse(localStorage.getItem('source_deck')) || []);
    const [targetDecks, setTargetDecks] = useState(JSON.parse(localStorage.getItem('target_deck')) || []);
    const [selectedDeckId, setSelectedDeckId] = useState(null);
    const selectedDeck = sourceDecks.concat(targetDecks).find(deck => deck.deck_id === selectedDeckId);

    const createDeck = (source) => {
        //create a random hash from date and time for the deck_id
        const deck_id = Date.now().toString(36) + Math.random().toString(36).substr(2);
        const deck = {
            deck_id: deck_id,
            source: source,
            deck: deck_id,
            cards: [],
        };
        if (source) {
            const newSourceDecks = [...sourceDecks, deck];
            setSourceDecks(newSourceDecks);
            localStorage.setItem('source_deck', JSON.stringify(newSourceDecks));
        } else {
            const newTargetDecks = [...targetDecks, deck];
            setTargetDecks(newTargetDecks);
            localStorage.setItem('target_deck', JSON.stringify(newTargetDecks));
        }
    }

    const updateDeck = (source, deck) => {
        const index = source ? sourceDecks.findIndex(d => d.deck_id === deck.deck_id) : targetDecks.findIndex(d => d.deck_id === deck.deck_id);
        if (source) {
            const newSourceDecks = [...sourceDecks];
            newSourceDecks[index] = deck;
            setSourceDecks(newSourceDecks);
            localStorage.setItem('source_deck', JSON.stringify(newSourceDecks));
        } else {
            const newTargetDecks = [...targetDecks];
            newTargetDecks[index] = deck;
            setTargetDecks(newTargetDecks);
            localStorage.setItem('target_deck', JSON.stringify(newTargetDecks));
        }
    }

    const deleteDeck = (source, deck_id) => {
        if (source) {
            const newSourceDecks = sourceDecks.filter(deck => deck.deck_id !== deck_id);
            setSourceDecks(newSourceDecks);
            localStorage.setItem('source_deck', JSON.stringify(newSourceDecks));
        } else {
            const newTargetDecks = targetDecks.filter(deck => deck.deck_id !== deck_id);
            setTargetDecks(newTargetDecks);
            localStorage.setItem('target_deck', JSON.stringify(newTargetDecks));
        }
    }

    const value = {
        sourceDecks,
        targetDecks,
        createDeck,
        updateDeck,
        deleteDeck,
        setSelectedDeckId,
        selectedDeck,
    };

  // The provider component itself
  return <DeckContext.Provider value={value}>{children}</DeckContext.Provider>;
};

// Custom hook that components can use to access the context value
export const useDeck = () => {
    const context = useContext(DeckContext);
    if (context === undefined) {
      throw new Error('useDeck must be used within a DeckProvider');
    }
    return context;
  };
  
  export default DeckProvider;