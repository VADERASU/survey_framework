import Card from '@mui/material/Card';
import Paper from '@mui/material/Paper';

export default function ImageCard({ data = "", onClick = () => { } }) {
    return (
        <Card component={Paper} onClick={onClick}>
            <img width={200} height={200} src={`data:image/png;base64,${data}`} />
        </Card >
    );
}
