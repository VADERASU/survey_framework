import React from 'react';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Stack from '@mui/material/Stack';
import Button from '@mui/material/Button';
import PersonIcon from '@mui/icons-material/Person';
import Tooltip from '@mui/material/Tooltip';
import SvgIcon from '@mui/material/SvgIcon';
import SVG from 'react-inlinesvg';
import CircularProgress from '@mui/material/CircularProgress';
import IconButton from './StyledIconButton';

export default function Filters({ metadata, setFilter }) {

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
        {children.map((child) =>
            <Stack key={child.name} sx={{ flex: 1 }}>
                <Tooltip title={child.name}>
                    <IconButton color={child.name} sx={{ margin: '5px' }} onClick={() => setFilter(child.name)} variant="outlined" key={child.name}>{buildIcon(child)}</IconButton>
                </Tooltip>
                <Box sx={{ display: 'flex', flex: 1, gap: '5px' }}>
                    {buildChildren(child.children)}
                </Box>
            </Stack>
        )}
    </>;

    if (metadata) {
        // ignore the root
        const sections = metadata.children;
        return (<Box sx={{ display: 'flex', justifyContent: 'center', gap: '5px' }}>
            {sections.map((section) =>
            (<Box sx={{ flex: 1, justifyContent: 'center' }} key={section.name}>
                <Typography variant="h5">{section.name}</Typography>
                <Box sx={{ display: 'flex' }}>
                    <Button color={section.name}
                        onClick={() => setFilter(section.name)}
                        variant="contained">
                        All</Button>
                    {buildChildren(section.children)}
                </Box>
            </Box>)
            )}
        </Box>);
    }
    return <Box sx={{ display: 'flex' }} />;
}
