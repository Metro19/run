import {createStyles, MantineProvider, rem, Text} from '@mantine/core';
import {Header} from "./navbar/Header";

export const HEADER_HEIGHT = 75;

const useStyles = createStyles((theme) => ({
    all: {
        marginTop: rem(HEADER_HEIGHT),
    },

    text: {
        color: "white",
    }
}))

export default function App() {
  const {classes, theme} = useStyles();
  return (
      <MantineProvider withGlobalStyles withNormalizeCSS theme={{colorScheme:'dark'}}>
          <Header />
          <div className={classes.all}>
              <Text className={classes.text} >Welcome to Mantine!</Text>
          </div>
      </MantineProvider>
  );
}