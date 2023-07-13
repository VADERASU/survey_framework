import { IconButton, styled } from '@mui/material';

const StyledIconButton = styled(IconButton)
    (({ theme, variant, color }) => {
        const overrides = {};

        const colorAsVariant = color === undefined || color === 'inherit' || color === 'default' ? 'primary' : color;

        overrides.borderRadius = 0;
        if (variant === 'contained') {
            overrides.backgroundColor = theme.palette[colorAsVariant].main;
            overrides.color = theme.palette[colorAsVariant].contrastText;
        }

        if (variant === 'outlined') {
            overrides.border = `1px solid ${theme.palette[colorAsVariant].main}`;
            overrides.color = theme.palette[colorAsVariant].main;
        }

        return {
            ...overrides,
        };
    });
export default StyledIconButton;
