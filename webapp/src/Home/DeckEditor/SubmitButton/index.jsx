

function SubmitButton({updateCardList, setSelectedDeckId}) {

    const handleSaveAndClose = () => {
        updateCardList();
        setSelectedDeckId(null);
    }
    
    return (
        <div className='save-container'>
            <button type="submit" className="btn btn-primary" onClick={() => {setSelectedDeckId(null)}}>Back</button>
            <button type="submit" className="btn btn-primary" onClick={updateCardList}>Save</button>
            <button type="submit" className="btn btn-primary" onClick={handleSaveAndClose}>Save and Close</button>
        </div>
    ) ;
}

export default SubmitButton;