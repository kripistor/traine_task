import React, {useState} from 'react';
import {Form, Input, Button, DatePicker, Select} from 'antd';
import {jwtDecode} from "jwt-decode";
import UserService from "../api/UserService.js";
import Cookies from "js-cookie";
const { Option } = Select;
export default function CreateClientForm(props) {
    const [form] = Form.useForm();
    const onFinish = async (values) => {
        const accessToken = Cookies.get('access_token');
        const decodedToken = jwtDecode(accessToken);
        const responsible_user_id = parseInt(decodedToken.sub);
        values.responsible_user_id = responsible_user_id;
        values.birth_date = values.birth_date.format('YYYY-MM-DD');
        try {
            console.log(values);
            await UserService.create_clients(values);
            form.resetFields();
            await props.refreshClients();
        } catch (error) {
            console.error(error);
        }
    };

    return (
        <Form form={form} name="create_client" onFinish={onFinish} layout="vertical">
            <Form.Item name="account_number" label="Номер счета" rules={[{required: true}]}>
                <Input/>
            </Form.Item>
            <Form.Item name="surname" label="Фамилия" rules={[{required: true}]}>
                <Input/>
            </Form.Item>
            <Form.Item name="name" label="Имя" rules={[{required: true}]}>
                <Input/>
            </Form.Item>
            <Form.Item name="middle_name" label="Отчество" rules={[{required: true}]}>
                <Input/>
            </Form.Item>
            <Form.Item name="birth_date" label="Дата рождения" rules={[{required: true}]}>
                <DatePicker/>
            </Form.Item>
            <Form.Item name="itn" label="ИНН" rules={[{required: true}]}>
                <Input/>
            </Form.Item>
            <Form.Item name="status" label="Статус" rules={[{required: true}]}>
                <Select defaultValue="not_at_work" placeholder="Выберите статус">
                    <Option value="not_at_work">Не в работе</Option>
                    <Option value="work">В работе</Option>
                    <Option value="rejection">Отказ</Option>
                    <Option value="deal _closed">Сделка закрыта</Option>
                </Select>
            </Form.Item>
            <Form.Item>
                <Button type="primary" htmlType="submit">
                    Создать клиента
                </Button>
            </Form.Item>
        </Form>
    );
}