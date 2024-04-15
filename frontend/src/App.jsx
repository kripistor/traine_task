import {useState} from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import {BrowserRouter, Route, Routes} from "react-router-dom"
import Login from "./assets/pages/Login.jsx";
import Clients from "./assets/pages/Clients.jsx";

function App() {

    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<Login/>}/>
                <Route path="/clients" element={<Clients/>}/>
            </Routes>
        </BrowserRouter>
    )
}

export default App
