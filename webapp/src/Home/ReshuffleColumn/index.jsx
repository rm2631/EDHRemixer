import {Button} from 'react-bootstrap';
import { useState } from 'react';
import axiosInstance from '../../axiosConfig';

const ReshuffleColumn = ({ collections }) => {

    const [loading, setLoading] = useState(false);

    const sendReshuffleRequest = async () => {
        setLoading(true);
        try {
            const response = await axiosInstance.post('/reshuffle', collections, {
                responseType: 'blob', // Tell axios to get the response as a Blob
            });

            // Create a new Blob object from the response data
            const blob = new Blob([response.data], { type: 'application/vnd.ms-excel' });

            // Create a URL representing the Blob
            const downloadUrl = URL.createObjectURL(blob);

            // Create a new 'a' element and use it to download the file
            const link = document.createElement('a');
            link.href = downloadUrl;
            link.download = 'reshuffled_collections.xlsx'; // The filename of the downloaded file
            link.click();

            // URL.revokeObjectURL(downloadUrl); // Optional: free up memory by revoking the Blob URL
        } catch (error) {
            console.error('Error downloading file:', error);
        } finally {
            setLoading(false);
        }
    }

    return (
        <div className='home-column-container'>
            <Button
                variant="primary"
                className="btn"
                block 
                disabled={collections.length === 0 || loading}
                onClick={sendReshuffleRequest}
            >
                {loading ? 'Loading...' : 'Reshuffle'}
            </Button>
        </div>
    )

}

export default ReshuffleColumn;