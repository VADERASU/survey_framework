import React from 'react';
import Dialog from '@mui/material/Dialog';
import DialogContent from '@mui/material/DialogContent';
import Chip from '@mui/material/Chip';
import Stack from '@mui/material/Stack';
import { Typography } from '@mui/material';
import { useTheme } from '@mui/material/styles';

export default function PaperModal({
    open,
    handleClose = () => { },
    selected = null,
}) {
    const thumbnail = (selected) ? selected.thumbnail : '';
    const title = (selected) ? selected.paper.title : '';
    const author = (selected) ? selected.paper.author : '';
    const keywords = (selected) ? selected.keywords : [];

    const theme = useTheme();

    return (
        <Dialog fullWidth maxWidth='sm' open={open} onClose={handleClose} scroll="body">
            <DialogContent>
                <Stack gap={1}>
                    <Stack direction="row" gap={1}>
                        <img width={200} height={200} style={{ border: '1px solid' }} src={`data:image/png;base64,${thumbnail}`} />
                        <Stack spacing={2}>
                            <Typography><b>{title}</b></Typography>
                            <Typography>{author}</Typography>
                        </Stack>
                    </Stack>
                    <Stack direction="row" gap={1}>
                        {keywords.map((k) => <Chip sx={{ backgroundColor: theme.palette[k].main }} key={k} variant="outlined" label={k} />)}
                    </Stack>
                </Stack>
            </DialogContent>
        </Dialog >
    );
}
