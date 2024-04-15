import React, {useState} from 'react'
import {UserOutlined} from '@ant-design/icons';
import {Button, Input, Space} from 'antd';
import UserService from "../api/UserService.js";
import {useNavigate} from "react-router-dom";

export default function Login() {
    const [login, setLogin] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();

    const handleLogin = async () => {
        try {
            await UserService.login(login, password);
            navigate('/clients');
        } catch (error) {
            console.error(error);
        }
    }
    return (
        <div className="flex items-center justify-center h-screen space-y-2">
            <Space direction="vertical">
                <Input
                    size="large"
                    placeholder="default size"
                    prefix={<UserOutlined />}
                    className="h-12 w-72"
                    onChange={(e) => setLogin(e.target.value)}
                />
                <Input.Password
                    size="large"
                    placeholder="input password"
                    className="h-12 w-72"
                    onChange={(e) => setPassword(e.target.value)}
                />
                <Button className="h-12 w-72" type="primary" onClick={handleLogin}>Primary Button</Button>
            </Space>
        </div>
    )
}