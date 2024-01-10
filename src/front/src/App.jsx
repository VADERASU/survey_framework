import { React, useEffect, useState } from 'react';
import Grid from '@mui/material/Grid';
import Stack from '@mui/material/Stack';
import './App.css'

import { createTheme, ThemeProvider } from '@mui/material/styles';
// edit SURVEY_NAME to correspond to your survey
import Box from '@mui/material/Box';
import CircularProgress from '@mui/material/CircularProgress';
import Typography from '@mui/material/Typography';
import { SURVEY_NAME } from './api/Constants';
import ImageCard from './components/ImageCard';
import PaperModal from './components/PaperModal';
import Filters from './components/Filters';
import { getHeaders } from './api/utils';

function App() {
    const [images, setImages] = useState([]);
    const [papers, setPapers] = useState({});
    const [metadata, setMetadata] = useState(null);
    const [selected, setSelected] = useState(null);
    const [filter, setFilter] = useState({});
    const [theme, setTheme] = useState(createTheme());
    const [isPageLoaded, setIsPageLoaded] = useState(false);
    const [icons, setIcons] = useState({});

    const createThemeFromMetadata = (md, themeDict, parentColor) => {
        const useColor = (md.color === "") ? parentColor : md.color;
        themeDict[md.name] = { main: useColor };
        // TODO: proper inversion function
        themeDict[`inverted_${md.name}`] = { main: "#d6d6d6" };
        for (const child of md.children) {
            createThemeFromMetadata(child, themeDict, themeDict[md.name].main);
        }

        themeDict.white = { main: "#FFFFFF" };
        themeDict.black = { main: "#000000" };
        return themeDict;
    };

    useEffect(() => {
        const jsonURL = new URL(`./data/${SURVEY_NAME}.json`, import.meta.url).href;

        fetch(jsonURL, { method: "GET" })
            .then((response) => {
                if (response.ok) {
                    return response.json();
                }
                throw new Error("Something went wrong.");
            })
            .then((data) => {
                const igs = data.images.map((i) => ({ ...i, url: new URL(`./images/${i.fname}`, import.meta.url).href }));
                setImages(igs);
                setPapers(data.papers);
                setMetadata(data.metadata);
                setIcons(data.icons);

                const filters = {};
                getHeaders(data.metadata).forEach((section) => { filters[section] = [] });
                setFilter(filters);

                setTheme(createTheme({ palette: createThemeFromMetadata(data.metadata, {}, "") }));
                setIsPageLoaded(true);
            }).catch((e) => {
                alert(e);
            });
    }, []);

    const toggleFilter = (filterName, sectionName) => {
        const filterArray = filter[sectionName];

        if (!filterArray.includes(filterName)) {
            // if its a section header, set the entire section to ALL
            if (filterName === sectionName) {
                setFilter({ ...filter, [sectionName]: [filterName] });
            } else if (filterArray.includes(sectionName)) {
                const idx = filterArray.indexOf(sectionName);
                setFilter({ ...filter, [sectionName]: [...filterArray.slice(0, idx), ...filterArray.slice(idx + 1), filterName] });
            } else {
                setFilter({ ...filter, [sectionName]: [...filterArray, filterName] });
            }
        } else {
            const idx = filterArray.indexOf(filterName);
            setFilter({ ...filter, [sectionName]: [...filterArray.slice(0, idx), ...filterArray.slice(idx + 1)] });
        }
    }

    /* this function allows you to dynamically build a bool statement
     based on the filters that are selected
     filters within a section are treated as ORs
     between sections are ANDS */
    const filterFunc = (Object.values(filter).every((d) => d.length === 0)) ? () => true : (i) =>
        Object.keys(filter).filter((section) => {
            // filter out the sections without filters selected
            const filters = filter[section];
            return filters.length > 0;
        }).map((section) => {
            const filters = filter[section];
            return filters.map((d) => i.keywords.includes(d)).some((d) => d);
        }).every((d) => d);

    if (isPageLoaded) {
        return (
            <ThemeProvider theme={theme}>
                <Stack gap={2} sx={{ padding: '1rem' }} >
                    <Filters metadata={metadata} setFilter={toggleFilter} filter={filter} />
                    <Grid container justifyContent="center">
                        {images.map((i) => {
                            const display = (filterFunc(i)) ? 'block' : 'none';
                            return (<Grid sx={{ display, margin: '10px' }} key={i._id} item>
                                <ImageCard fileSrc={i.url} onClick={() => {
                                    const headers = getHeaders(metadata);
                                    setSelected({
                                        icons,
                                        fileSrc: i.url,
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
    return <Box sx={{ position: 'absolute', top: '50%', left: '50%', transform: "translate(-50%, -50%)" }}>
        <Typography variant="h5">Fetching data...</Typography>
        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <CircularProgress />
        </Box>
    </Box >


}
export default App;
