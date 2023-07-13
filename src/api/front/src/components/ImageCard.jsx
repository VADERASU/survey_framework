import React from 'react';
import Card from '@mui/material/Card';
import CardMedia from '@mui/material/CardMedia';
import Paper from '@mui/material/Paper';

export default function ImageCard({ data = "", onClick = () => { } }) {
    return (
        <Card sx={{ 'width': 200, 'height': 200 }} component={Paper} onClick={onClick}>
            <CardMedia component="img"
                sx={{ 'width': 200, 'height': 200 }}
                image={`data:image/png;base64,${data}`} />
        </Card >
    );
}
