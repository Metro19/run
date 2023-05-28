import {
    Box,
    Button,
    Center,
    createStyles,
    Group,
    MantineProvider,
    PasswordInput, rem,
    TextInput
} from "@mantine/core";
import {Header} from "../navbar/Header";
import {HEADER_HEIGHT} from "../App";
import {isEmail, useForm} from "@mantine/form";
import {useEffect, useState} from "react";
import {  } from "react-router-dom";
import {API_URL} from "../api_interface/api_setup";
import {Notifications, notifications} from "@mantine/notifications";
import {IconX} from "@tabler/icons-react";

let signedIn = false;


const useStyles = createStyles((theme) => ({
    all: {
        marginTop: rem(HEADER_HEIGHT),
        marginLeft: `${theme.spacing.md}`,
    },

    form: {
        marginTop: rem((window.innerHeight / 2) - HEADER_HEIGHT),
    },

    passwordButton: {
    margin: `${theme.spacing.md}`,
    },

    text: {
        color: "white",
    }
}))

export function Login() {
    // data storage
    const [signedIn, setSignedIn] = useState(false);
    const [logInCount, setlogInCount] = useState(0);


    // create the form
    const form = useForm({
        initialValues: {
            username: "",
            password: "",
        },

        validate: {
            username: isEmail("Invalid Email"),
        }
    });

    const {classes, theme} = useStyles();
    return (
        <MantineProvider withGlobalStyles theme={{colorScheme:'dark'}}>
            <Notifications/>
            <div>
                <Header/>
                    <Center>
                        {console.log(logInCount)}
                        {signedIn && window.location.replace("/")}
                        {logInCount > 0 && console.log("Login failed")}
                        {/*TODO: ADD FAILED TO LOG IN NOTIFICATION*/}

                    {/*    TODO: REMOVE ERROR MESSAGES */}
                    <form className={classes.form} onSubmit={form.onSubmit((values) =>
                        fetch(API_URL + "/token", {method: 'POST',
                            headers: {
                                "username": values.username,
                                "password": values.password,
                                "accept": "application/json",
                                "Content-Type": "application/x-www-form-urlencoded",
                                "grant_type": "",
                                "scope": "",
                                "client_id": "",
                                "client_secret": "",
                            },
                            body: "username=" + values.username + "&password=" + values.password + "&grant_type=password&scope=&client_id=&client_secret="
                        })
                            .then((response) => response.json())
                            .then((response) => {setSignedIn(true); localStorage.setItem("token", response.access_token)})
                            .catch((error) => {setSignedIn(false); console.log(error); setlogInCount(logInCount + 1)})
                    )}>

                        <TextInput
                            className={classes.text}
                            label="Email"
                            placeholder="email@example.com"
                            withAsterisk
                            {...form.getInputProps("username")}
                        />

                        <PasswordInput
                            className={classes.text}
                            label="Password"
                            withAsterisk
                            {...form.getInputProps("password")}
                        />


                        <Group position="center">
                            <Button className={classes.passwordButton} type="submit">Login</Button>
                        </Group>
                    </form>
                </Center>
            </div>
        </MantineProvider>
    )
}