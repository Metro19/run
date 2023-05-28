import {createStyles, MantineProvider, rem, Text} from '@mantine/core';
import {Header} from "./navbar/Header";
import * as ReactDOM from "react-dom/client";
import {createBrowserRouter, RouterProvider} from "react-router-dom";
import {Login} from "./login/Login";
import React from "react";
import {Notifications} from "@mantine/notifications";

export const HEADER_HEIGHT = 75;

// browser routing
const router = createBrowserRouter([
    {
        path: "/",
        element: <Homepage/>,
    },

    {
        path: "/login",
        element: <Login/>,
    }
]);

const useStyles = createStyles((theme) => ({
    all: {
        marginTop: rem(HEADER_HEIGHT),
    },

    text: {
        color: "white",
    }
}))

export function Homepage() {
  const {classes, theme} = useStyles();
  return (
          <MantineProvider withGlobalStyles withNormalizeCSS theme={{colorScheme:'dark'}}>
              <Notifications/>
              <Header />
              <div className={classes.all}>
                  <Text className={classes.text} >Welcome to Mantine!</Text>
              </div>
          </MantineProvider>
  );
}

export default function App() {
    return (
        <React.StrictMode>
            <RouterProvider router={router} />
        </React.StrictMode>
    )
}