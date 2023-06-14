import Dialog from '@mui/material/Dialog';
import Chip from '@mui/material/Chip';
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

    return (<Dialog open={open} onClose={handleClose}>
        <img width={200} height={200} src={`data:image/png;base64,${thumbnail}`} />
        <Typography>{title}</Typography>
        <Typography>by {author}</Typography>
        {keywords.map((k) => <Chip key={k} label={k} />)}
    </Dialog>);
}
