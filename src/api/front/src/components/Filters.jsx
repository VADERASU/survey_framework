import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Stack from '@mui/material/Stack';
import Button from '@mui/material/Button';

export default function Filters({ metadata, setFilter }) {

    const buildChildren = (children) => <>
        {children.map((child) =>
            <Stack key={child.name}>
                <Button color={child.name} onClick={() => setFilter(child.name)} variant="contained" key={child.name}>{child.name}</Button>
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
