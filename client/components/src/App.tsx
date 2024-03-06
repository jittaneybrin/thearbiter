import React, { useEffect, useState } from "react";
import logo from "./logo.svg";
import "./App.css";
import axios from "axios";

function App() {
  const [message, setMessage] = useState("");

  useEffect(() => {
    // Make a GET request to the Flask backend
    axios
      .get("http://127.0.0.1:5000/")
      .then((response) => {
        setMessage(response.data.message);
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
      });
  }, []);

  return (
    // <ThemeProvider theme={theme}>
    //   <CssBaseline />
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>Flask says {message}</p>
      </header>
    </div>
    // </ThemeProvider>
  );
}

export default App;
