import './styles/base.css'
import { useCollection } from "../Home/CollectionContext";
import CollectionColumn from './CollectionColumn';
import ReshuffleColumn from './ReshuffleColumn';

function Home() {

    const {
        collections,
        addCollection,
        removeCollection,
        updateCollection
    } = useCollection();

    const sourceCollections = collections.filter((collection) => collection.is_source);
    const targetCollections = collections.filter((collection) => !collection.is_source);

    return (
        <div className='home-container'>
            <CollectionColumn
                is_source={true}
                collections={sourceCollections}
            />
            <CollectionColumn
                is_source={false}
                collections={targetCollections}
            />
            <ReshuffleColumn
                collections={collections}
            />
        </div>
    );
}

export default Home