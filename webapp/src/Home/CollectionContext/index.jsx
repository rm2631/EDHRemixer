import React, { createContext, useContext, useState, useEffect } from 'react';


class Collection {
  constructor(name, url, isSource) {
      this.id = Math.random().toString(36).substr(2, 9);
      this.name = name;
      this.url = url;
      this.is_source = isSource;
      this.creationDate = new Date();
  }
}

const CollectionContext = createContext();

export const CollectionProvider = ({ children }) => {
  const [initalLoading, setInitialLoading] = useState(false);
  const [collections, setCollections] = useState([]);

  // Memory management
  useEffect(() => {
    // Load collections from local storage
    if (initalLoading) { return; }
    const collections = localStorage.getItem('collections');
    if (collections) {
      setCollections(JSON.parse(collections));
    }
  }, []);
  
  useEffect(() => {
    localStorage.setItem('collections', JSON.stringify(collections));
  }, [collections]);

  const addCollection = (name, url, isSource) => {
    const newCollection = new Collection(name, url, isSource);
    setCollections([...collections, newCollection]);
  };

  const removeCollection = (id) => {
    const newCollections = collections.filter((collection) => collection.id !== id);
    setCollections(newCollections);
  };

  const updateCollection = (id, name, url, isSource) => {
    const updatedCollections = collections.map((collection) => {
      if (collection.id === id) {
        return { ...collection, name, url, isSource };
      }
      return collection;
    });
    setCollections(updatedCollections);
  };

  const value = {
    collections,
    addCollection,
    removeCollection,
    updateCollection,
  };
  
  return <CollectionContext.Provider value={value}>{children}</CollectionContext.Provider>;
};

export const useCollection = () => {
    const context = useContext(CollectionContext);
    if (context === undefined) {
      throw new Error('useCollection must be used within a CollectionProvider');
    }
    return context;
  };
  
  export default CollectionProvider;