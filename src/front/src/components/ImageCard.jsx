import React from 'react';
import Card from '@mui/material/Card';
import CardMedia from '@mui/material/CardMedia';
import Paper from '@mui/material/Paper';

export default function ImageCard({ fileName = "", onClick = () => { } }) {
    const imageURL = new URL(`../images/${fileName}`, import.meta.url).href;
 
    return (
        <Card className="borderOnHover showClickOnHover" sx={{ 'width': 200, 'height': 200 }}
            variant="outlined"
            component={Paper}
            onClick={onClick}>
            <CardMedia component="img"
                sx={{ 'width': 200, 'height': 200 }}
                image={imageURL} />
        </Card >
    );
}
