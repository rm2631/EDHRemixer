import CollectionModal from "./CollectionModal";

const CollectionColumn = ({ is_source, collections }) => {
    return (
        <div className="home-column-container">
            <CollectionModal is_source={is_source} />
            {
                collections.map((collection, index) => (
                    <CollectionModal
                        key={index}
                        is_source={is_source}
                        collection={collection} />
                ))
            }
        </div>
    );
};

export default CollectionColumn;