import { useEffect, useState } from 'react';
import Grid from '@mui/material/Grid';
import Typography from '@mui/material/Typography';
import Stack from '@mui/material/Stack';
import './App.css'

import { API_URL } from './api/Constants';
import ImageCard from './components/ImageCard';
import PaperModal from './components/PaperModal';
import Filters from './components/Filters';
function App() {
    const [images, setImages] = useState([]);
    const [papers, setPapers] = useState({});
    const [metadata, setMetadata] = useState(null);
    const [selected, setSelected] = useState(null);
    const [filter, setFilter] = useState(null);

    useEffect(() => {
        fetch(`${API_URL}/get_db/survey`, { method: "GET" })
            .then((response) => {
                if (response.ok) {
                    return response.json();
                }
                throw new Error("Something went wrong.");
            })
            .then((data) => {
                setImages(data.images);
                setPapers(data.papers);
                setMetadata(data.metadata);
            }).catch((e) => {
                alert(e);
            });
    }, []);

    return (
        <Stack gap={2}>
            <Typography variant="h1">Survey</Typography>
            <Filters metadata={metadata} setFilter={setFilter} />
            <Grid container spacing={2}>
                {images.filter((i) => {
                    if (filter !== null) {
                        return i.keywords.includes(filter);
                    }
                    return true;
                }).map((i) =>
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
        </Stack>
    );
}
export default App;
