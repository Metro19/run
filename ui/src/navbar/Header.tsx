import {Button, Center, rem, createStyles, Skeleton} from "@mantine/core";
import {HEADER_HEIGHT} from "../App";
import {API_URL} from "../api_interface/api_setup";
import {useEffect, useState} from "react";


// styles
const useStyles = createStyles((theme) => ({
    header: {
        position: "fixed",
        top: 0,
        width: "100%",

        backgroundColor: theme.primaryColor,
        height: rem(HEADER_HEIGHT),
    },

    title: {
        margin: "auto",
        position: "absolute",

        marginLeft: `${theme.spacing.md}`,
    },

    user_menu: {
        margin: "auto",
        position: "absolute",

        right: `${theme.spacing.md}`,
    },

    button: {
        backgroundColor: theme.colors.blue[6],
    }
}))



function UserMenu() {
    const {classes, theme} = useStyles();

    // data storage
    const [userData, setUserData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    // get user data
    useEffect(() => {
        // check if need to fetch
        if (userData !== null || error !== null) return;

        fetch(API_URL + "/user/info", {headers: {Authorization: "Bearer " + localStorage.getItem("token")}})
            .then((response) => response.json())
            .then((response) => {setUserData(response.username); setError(null);})
            .catch((error) => {setError(error); setUserData(null);})
            .finally(() => setLoading(false));
    })

    // return information
    return (
        <div>
            <Skeleton visible={loading}>
                {/* On error, display log in page */}
                {error &&
                <div>
                    <Button className={classes.button} onClick={() => window.location.href = "/login"}>Login</Button>
                </div>
                }
                {userData &&
                <div>
                    <Button className={classes.button} onClick={() => localStorage.removeItem("token")}>{userData}</Button>
                </div>
                }
            </Skeleton>
        </div>
    )
}

export function Header() {
    const {classes, theme} = useStyles();
    return (
        <div className={classes.header}>
            <Center h={HEADER_HEIGHT} className={classes.title}>
                <h1><a href="/"><i>R</i>un</a></h1>
            </Center>

            <Center h={HEADER_HEIGHT} className={classes.user_menu}>
                {/* Only try displaying menu if user has a token saved to browser */}
                {localStorage.getItem("token") !== null && <UserMenu/>}

                {/* If user has no token, display login button */}
                {localStorage.getItem("token") === null &&
                    <Button className={classes.button} onClick={() => window.location.href = "/login"}>Login</Button>
                }
            </Center>
        </div>
    )
}