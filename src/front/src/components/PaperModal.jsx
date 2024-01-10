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
import SvgIcon from '@mui/material/SvgIcon';
import SVG from 'react-inlinesvg';
import CircularProgress from '@mui/material/CircularProgress';

export default function PaperModal({
    open,
    handleClose = () => { },
    selected = null,
}) {
    const fileSrc = (selected) ? selected.fileSrc : '';
    const title = (selected) ? selected.paper.title : '';
    const author = (selected) ? selected.paper.author : '';
    const keywords = (selected) ? selected.keywords : [];
    const doi = (selected) ? selected.paper.doi : '';
    const icons = (selected) ? selected.icons : {};
    const link = `https://doi.org/${doi}`;
    const theme = useTheme();

    // TODO: move to utils, need to have the entirety of the project rely on the icons dict
    // even better would be to have the tree structure only contain ids and have another dict to access
    // metadata info directly
    const buildIcon = (section) => {
        const icon = icons[section];
        console.log(section, icon);
        if (icon !== undefined && icon !== '') {
            const imgUrl = new URL(`../icons/${icon}`, import.meta.url).href;
            return <SvgIcon>
                <SVG src={imgUrl} loader={<CircularProgress />} />
            </SvgIcon>
        }
        return <PersonIcon />
    };

    return (
        <Dialog fullWidth maxWidth='sm' open={open} onClose={handleClose} scroll="body">
            <DialogContent>
                <Stack direction="row" gap={2}>
                    <Box sx={{ alignItems: 'center', alignContent: 'center', justifyContent: 'center', display: 'flex' }} >
                        <a style={{ color: 'black' }} href={link}>
                            <img className="paperImage" height={200} width={200} src={fileSrc} />
                        </a>
                    </Box>
                    <Stack spacing={2}>
                        <Typography><b>{title}</b></Typography>
                        <Typography>{author}</Typography>
                        <Grid container>
                            {keywords.map((k) => <Grid sx={{ marginRight: '5px', marginBottom: '5px' }} item key={k}>
                                <Tooltip title={k}>
                                    <Box className="borderOnHover">
                                        {buildIcon(k)}
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
