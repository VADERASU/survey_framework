import { useEffect, useState } from 'react';
import Grid from '@mui/material/Grid';
import './App.css'

import { API_URL } from './api/Constants';
import ImageCard from './components/ImageCard';
import PaperModal from './components/PaperModal';

function App() {
    const [images, setImages] = useState([]);
    const [papers, setPapers] = useState({});
    const [metadata, setMetadata] = useState({});
    const [selected, setSelected] = useState(null);

    useEffect(() => {
        fetch(`${API_URL}/get_db/survey`, { method: "GET" })
            .then((response) => response.json())
            .then((data) => {
                console.log(data);
                setImages(data.images);
                setPapers(data.papers);
                setMetadata(data.metadata);
            })
    }, []);

    return (
        <div>
            <h1>Survey</h1>
            <Grid container spacing={2}>
                {images.map((i) =>
                    <Grid key={i._id} item xs={4}>
                        <ImageCard data={i.data} onClick={() =>
                            setSelected({
                                thumbnail: i.data,
                                keywords: i.keywords,
                                paper: papers[i.paper]
                            })
                        } />
                    </Grid>
                )}
            </Grid>
            <PaperModal
                open={selected !== null}
                handleClose={() => setSelected(null)}
                selected={selected}
            />
        </div>
    );
}
export default App;
