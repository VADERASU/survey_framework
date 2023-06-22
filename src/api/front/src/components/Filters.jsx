import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Stack from '@mui/material/Stack';
import Button from '@mui/material/Button';

export default function Filters({ metadata, setFilter }) {

    const buildChildren = (children) => {
        return <>
            {children.map((child) =>
                <Stack key={child.name}>
                    <Button onClick={() => setFilter(child.name)} variant="contained" key={child.name}>{child.name}</Button>
                    <Box sx={{ display: 'flex' }}>
                        {buildChildren(child.children)}
                    </Box>
                </Stack>
            )}
        </>
    };

    if (metadata) {
        // ignore the root
        const sections = metadata.children;
        return (<Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
            {sections.map((section) =>
            (<Box key={section.name}>
                <Typography variant="h5">{section.name}</Typography>
                <Box sx={{ display: 'flex' }}>
                    <Button onClick={() => setFilter(section.name)} variant="contained">All</Button>
                    {buildChildren(section.children)}
                </Box>
            </Box>)
            )}
        </Box>);
    }
    return <Box sx={{ display: 'flex' }} />;
}
