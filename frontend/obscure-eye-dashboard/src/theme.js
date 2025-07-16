import { createTheme } from '@mui/material/styles';
import '@fontsource/orbitron';

const darkPurple = '#2d0036';
const neonPurple = '#a259f7';
const neonLime = '#cfff04';
const black = '#181818';
const white = '#ffffff';

const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: neonPurple,
      contrastText: black,
    },
    secondary: {
      main: neonLime,
      contrastText: black,
    },
    background: {
      default: black,
      paper: darkPurple,
    },
    text: {
      primary: white,
      secondary: neonLime,
    },
  },
  typography: {
    fontFamily: 'Orbitron, Roboto, Arial',
    h1: { fontWeight: 700, letterSpacing: 2 },
    h2: { fontWeight: 700, letterSpacing: 2 },
    h3: { fontWeight: 700, letterSpacing: 2 },
    h4: { fontWeight: 700, letterSpacing: 2 },
    h5: { fontWeight: 700, letterSpacing: 2 },
    h6: { fontWeight: 700, letterSpacing: 2 },
    button: { fontWeight: 700 },
  },
  components: {
    MuiAppBar: {
      styleOverrides: {
        root: {
          background: darkPurple,
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          background: darkPurple,
          border: `1.5px solid ${neonPurple}`,
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 12,
        },
      },
    },
  },
});

export default theme;