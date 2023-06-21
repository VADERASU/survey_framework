import Dialog from '@mui/material/Dialog';
import Chip from '@mui/material/Chip';
import Stack from '@mui/material/Stack';
import Box from '@mui/material/Box';
import { Typography } from '@mui/material';

export default function PaperModal({
    open,
    handleClose = () => { },
    selected = null,
}) {
    const thumbnail = (selected) ? selected.thumbnail : "";
    const title = (selected) ? selected.paper.title : "";
    const author = (selected) ? selected.paper.author : "";
    const keywords = (selected) ? selected.keywords : [];

    return (<Dialog open={open} onClose={handleClose} scroll="body">
        <Box sx={{ display: 'flex', margin: 3, gap: '10px' }}>
            <img width={200} height={200} style={{ border: '1px solid' }} src={`data:image/png;base64,${thumbnail}`} />
            <Stack spacing={2}>
                <Typography><b>{title}</b></Typography>
                <Typography>{author}</Typography>
                <Box sx={{ display: 'flex', gap: '3px' }}>
                    {keywords.map((k) => <Chip key={k} label={k} />)}
                </Box>
            </Stack>
        </Box>
    </Dialog>);
}
