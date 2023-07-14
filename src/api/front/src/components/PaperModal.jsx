import React from 'react';
import Dialog from '@mui/material/Dialog';
import DialogContent from '@mui/material/DialogContent';
import Box from '@mui/material/Box';
import Stack from '@mui/material/Stack';
import Typography from '@mui/material/Typography';
import { useTheme } from '@mui/material/styles';
import Grid from '@mui/material/Grid';
import "../App.css"
import PersonIcon from '@mui/icons-material/Person';
import Tooltip from '@mui/material/Tooltip';

export default function PaperModal({
    open,
    handleClose = () => { },
    selected = null,
}) {
    const thumbnail = (selected) ? selected.thumbnail : '';
    const title = (selected) ? selected.paper.title : '';
    const author = (selected) ? selected.paper.author : '';
    const keywords = (selected) ? selected.keywords : [];
    const doi = (selected) ? selected.paper.doi : '';
    const link = `https://doi.org/${doi}`;
    const theme = useTheme();

    return (
        <Dialog fullWidth maxWidth='sm' open={open} onClose={handleClose} scroll="body">
            <DialogContent>
                <Stack direction="row" gap={2}>
                    <Box sx={{ alignItems: 'center', alignContent: 'center', justifyContent: 'center', display: 'flex' }} >
                        <a style={{ color: 'black' }} href={link}>
                            <img className="paperImage" height={200} width={200} src={`data:image/png;base64,${thumbnail}`} />
                        </a>
                    </Box>
                    <Stack spacing={2}>
                        <Typography><b>{title}</b></Typography>
                        <Typography>{author}</Typography>
                        <Grid container>
                            {keywords.map((k) => <Grid sx={{ marginRight: '5px', marginBottom: '5px' }} item key={k}>
                                <Tooltip title={k}>
                                    <Box className="borderOnHover" sx={{ backgroundColor: theme.palette[k].main }} >
                                        <PersonIcon color="white" />
                                    </Box>
                                </Tooltip>
                            </Grid>)}
                        </Grid>

                    </Stack>
                </Stack>
            </DialogContent>
        </Dialog >
    );
}
