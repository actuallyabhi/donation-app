import React from "react";
import { Box } from "@mui/system";
import { TextField, Button } from "@mui/material";



const Login = () => {
    const [email, setEmail] = React.useState("");
    const [password, setPassword] = React.useState("");
    const [name, setName] = React.useState("");

    const handleSubmit = () => {
        if (email && password && name) {
            console.log("Email: ", email);
        }
    }
    return (
        <Box display="flex" justifyContent="center" alignItems="center" height="100vh">
            <TextField label="Name" value={name} onChange={(e) => setName(e.target.value)} />
            <TextField label="Email" value={email} onChange={(e) => setEmail(e.target.value)} />
            <TextField label="Password" value={password} onChange={(e) => setPassword(e.target.value)} />

            <Button variant="contained" color="primary">Login</Button>

        </Box>

    );
    }

export default Login;