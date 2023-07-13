import React from 'react';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Stack from '@mui/material/Stack';
import Button from '@mui/material/Button';
import PersonIcon from '@mui/icons-material/Person';
import Tooltip from '@mui/material/Tooltip';
import IconButton from './StyledIconButton';

export default function Filters({ metadata, setFilter }) {

    const buildChildren = (children) => <>
        {children.map((child) =>
            <Stack key={child.name}>
                <Tooltip title={child.name}>
                    <IconButton color={child.name} onClick={() => setFilter(child.name)} variant="outlined" key={child.name}><PersonIcon /></IconButton>
                </Tooltip>
                <Box sx={{ display: 'flex', gap: '5px' }}>
                    {buildChildren(child.children)}
                </Box>
            </Stack>
        )}
    </>;

    if (metadata) {
        // ignore the root
        const sections = metadata.children;
        return (<Box sx={{ display: 'flex', gap: '10px' }}>
            {sections.map((section) =>
            (<Box key={section.name}>
                <Typography variant="h5">{section.name}</Typography>
                <Box sx={{ display: 'flex', gap: '5px' }}>
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
