import React from 'react';
import Box from '@mui/material/Box';
import Stack from '@mui/material/Stack';
import Button from '@mui/material/Button';
import PersonIcon from '@mui/icons-material/Person';
import Tooltip from '@mui/material/Tooltip';
import SvgIcon from '@mui/material/SvgIcon';
import SVG from 'react-inlinesvg';
import CircularProgress from '@mui/material/CircularProgress';
import Container from '@mui/material/Container';
import IconButton from './StyledIconButton';

export default function Filters({ metadata, setFilter, filter }) {

    const buildIcon = (section) => {
        if (section.icon !== '') {
            const imgUrl = new URL(`../icons/${section.icon}`, import.meta.url).href;
            return <SvgIcon>
                <SVG src={imgUrl} loader={<CircularProgress />} />
            </SvgIcon>
        }
        return <PersonIcon />
    };

    const buildChildren = (children) => <>
        {children.map((child) => {
            const color = (child.name === filter) ? `inverted_${child.name}` : child.name;

            return (<Stack key={child.name} sx={{ flex: 1 }}>
                <Tooltip title={child.name}>
                    <IconButton size="small"
                        color={color} sx={{ margin: '5px' }} onClick={() => setFilter(child.name)} variant="outlined" key={child.name}>{buildIcon(child)}</IconButton>
                </Tooltip>
                <Box sx={{ display: 'flex', flex: 1, gap: '5px' }}>
                    {buildChildren(child.children)}
                </Box>
            </Stack>);

        })}
    </>

    if (metadata) {
        // ignore the root
        const sections = metadata.children;
        return (<Container maxWidth={false} sx={{ display: { "lg": 'flex' }, justifyContent: { "lg": "center" }, gap: { "lg": '5px' } }}>

            {sections.map((section) => {
                const color = (section.name === filter) ? `inverted_${section.name}` : section.name;
                return (<>
                    <Box sx={{ display: 'flex', justifyContent: 'center' }}>
                        <Button color={color}
                            size="small"
                            onClick={() => setFilter(section.name)}
                            variant="contained">
                            {section.name}</Button>
                    </Box>
                    <Box sx={{ display: 'flex', flexWrap: { "md": 'wrap', "lg": 'none' }, justifyContent: 'center' }}>
                        {buildChildren(section.children)}
                    </Box>
                </>);
            })
            }
        </Container>);
    }
    return <Box sx={{ display: 'flex' }} />;
}
