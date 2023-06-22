import { useEffect, useState } from 'react';
import Grid from '@mui/material/Grid';
import Typography from '@mui/material/Typography';
import Stack from '@mui/material/Stack';
import './App.css'

import { createTheme, ThemeProvider } from '@mui/material/styles';
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
    const [theme, setTheme] = useState(createTheme());

    const createThemeFromMetadata = (md, themeDict, parentColor) => {
        const useColor = (md.color === "") ? parentColor : md.color;
        themeDict[md.name] = { main: useColor };
        for (const child of md.children) {
            createThemeFromMetadata(child, themeDict, themeDict[md.name].main);
        }
        return themeDict;
    };

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
                setTheme(createTheme({ palette: createThemeFromMetadata(data.metadata, {}, "") }));
            }).catch((e) => {
                alert(e);
            });
    }, []);

    return (
        <ThemeProvider theme={theme}>
            <Stack gap={1} >
                <Typography variant="h1">Survey</Typography>
                <Filters metadata={metadata} setFilter={setFilter} />
                <Grid container gap={1}>
                    {images.filter((i) => {
                        if (filter !== null) {
                            return i.keywords.includes(filter);
                        }
                        return true;
                    }).map((i) =>
                        <Grid key={i._id} item>
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
            </Stack>
            <PaperModal
                open={selected !== null}
                handleClose={() => setSelected(null)}
                selected={selected}
            />
        </ThemeProvider>
    );
}
export default App;
