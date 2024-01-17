import KebabIcon from '../../../../assets/icons/kebab.svg?react'
import { Button } from 'react-bootstrap'
import Dropdown from 'react-bootstrap/Dropdown';
import DeleteDeck from './DeleteDeck';

function Kebab({deck}) {

    const dropDownComponents = [
        <DeleteDeck deck_id={deck.deck_id} source={deck.source} />
    ]     

    return (
        <Dropdown drop="start">
            <Dropdown.Toggle  className='kebab-btn' id="dropdown-basic">
                <KebabIcon width={20} height={20} />
            </Dropdown.Toggle>
            <Dropdown.Menu>
                {dropDownComponents.map((component, index) => (
                    <Dropdown.Item key={index}>{component}</Dropdown.Item>
                ))}
            </Dropdown.Menu>
        </Dropdown>
    )
}

export default Kebab