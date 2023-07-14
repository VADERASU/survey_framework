import { React, useEffect, useState, useTransition } from 'react';
import Grid from '@mui/material/Grid';
import Stack from '@mui/material/Stack';
import './App.css'

import { createTheme, ThemeProvider } from '@mui/material/styles';
// edit SURVEY_NAME to correspond to your survey
import { API_URL, SURVEY_NAME } from './api/Constants';
import ImageCard from './components/ImageCard';
import PaperModal from './components/PaperModal';
import Filters from './components/Filters';
import getHeaders from './api/utils';

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
        fetch(`${API_URL}/get_db/${SURVEY_NAME}`, { method: "GET" })
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

    const filterFunc = (filter === null) ? () => true : (i) => i.keywords.includes(filter);
    return (
        <ThemeProvider theme={theme}>
            <Stack gap={2} >
                <Filters metadata={metadata} setFilter={setFilter} />
                <Grid container justifyContent="center">
                    {images.map((i) => {
                        const display = (filterFunc(i)) ? 'block' : 'none';
                        return (<Grid sx={{ display, margin: '10px' }} key={i._id} item>
                            <ImageCard data={i.data} onClick={() => {
                                const headers = getHeaders(metadata);
                                setSelected({
                                    thumbnail: i.data,
                                    keywords: i.keywords.filter((e) => !headers.includes(e)),
                                    paper: papers[i.paper]
                                })
                            }
                            } />
                        </Grid>);
                    }
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
