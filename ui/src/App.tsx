import { MantineProvider, Text } from '@mantine/core';

export default function App() {
  return (
      <MantineProvider withGlobalStyles withNormalizeCSS theme={{colorScheme:'dark'}}>
        <Text>Welcome to Mantine!</Text>
      </MantineProvider>
  );
}