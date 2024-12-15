import { useState } from 'react';
import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';
import { Form } from 'react-bootstrap';
import { useCollection } from "../../CollectionContext";
import { useEffect } from 'react';
import URLValidator from './URLValidator';

const CollectionModal = ({ is_source, collection }) => {

  const {
      addCollection,
      removeCollection,
      updateCollection
  } = useCollection();

  const [show, setShow] = useState(false);
  const [valid, setValid] = useState(false);

  const handleClose = () => {
    setShow(false);
  };
  const handleShow = () => setShow(true);

  const is_new = !collection;
  const id = collection ? collection.id : null;

  const [name, setName] = useState(collection ? collection.name : '');
  const [url, setUrl] = useState(collection ? collection.url : '');

  // Update name and url whenever collection changes
  useEffect(() => {
    setName(collection ? collection.name : '');
    setUrl(collection ? collection.url : '');
  }, [collection]);

  const handleSave = () => {
    if (is_new) {
      addCollection(name, url, is_source);
    } else {
      updateCollection(id, name, url, is_source);
    }
    setName('');
    setUrl('');
    handleClose();
  }  

  const handleDelete = () => {
    removeCollection(id);
    handleClose();
  }

  return (
    <>
      {is_new ? 
        <Button variant="primary" onClick={handleShow}>
              {is_source ? 'Add Source' : 'Add Target'}
        </Button> :
        <Button variant="outline-primary" onClick={handleShow}>
          {collection.name}
        </Button>
      }

      <Modal
        show={show}
        onHide={handleClose}
        backdrop="static"
        keyboard={false}
      >
        <Modal.Header closeButton>
          <Modal.Title>
            {is_new ? 'Add' : 'Edit'} {is_source ? 'Source' : 'Target'} Collection
          </Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form>
            <Form.Group controlId="formCollectionName">
              <Form.Label>Name</Form.Label>
              <Form.Control
                type="text"
                placeholder="Enter collection name"
                value={name}
                onChange={(e) => setName(e.target.value)}
              />
            </Form.Group>
            <br />
            <Form.Group controlId="formCollectionUrl">
              <Form.Label>URL</Form.Label>
              <Form.Control
                type="text"
                placeholder="Enter collection URL"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
              />
              <URLValidator url={url} setValid={setValid} />
            </Form.Group>
          </Form>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={handleClose}>
            Close
          </Button>
          {!is_new && <Button variant="danger" onClick={handleDelete}>Delete</Button>}
          <Button variant="primary" onClick={handleSave}
            disabled={!valid}
          >
            Save
          </Button>
        </Modal.Footer>
      </Modal>
    </>
  );
}

export default CollectionModal;