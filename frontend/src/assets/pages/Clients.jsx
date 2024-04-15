import React, {useEffect, useState} from 'react';
import {Button, Divider, Radio, Select, Space, Table} from 'antd';
import UserService from "../api/UserService.js";
import Cookies from "js-cookie";
import {useNavigate} from 'react-router-dom';
import {DeleteOutlined} from "@ant-design/icons";
const { Option } = Select;
const columns = [
    {
        title: 'id',
        dataIndex: 'id',
        render: (text) => <a>{text}</a>,
    },
    {
        title: 'Номер счета',
        dataIndex: 'account_number',
    },
    {
        title: 'Фамилия',
        dataIndex: 'surname',
    },
    {
        title: 'Имя',
        dataIndex: 'name',
    },
    {
        title: 'Отчество',
        dataIndex: 'middle_name',
    },
    {
        title: 'Дата рождения',
        dataIndex: 'birth_date',
    },
    {
        title: 'ИНН',
        dataIndex: 'itn',
    },
    {
        title: 'Статус',
        dataIndex: 'status',
        render: (text, record) => (
            <Space size="middle">
                <Select defaultValue={text} style={{width: 120}} onChange={(value) => handleChange(value, record)}>
                    <Option value="not_at_work">Не в работе</Option>
                    <Option value="work">В работе</Option>
                </Select>
                <Button type="primary" onClick={() => handleSave(record)}>Save</Button>
            </Space>
        ),
    }

];


const handleChange = (value, record) => {
    // Update the status in the local state
    record.status = value;
};

const handleSave = async (record) => {
    try {
        await UserService.update_client_status(record.id, record.status);
    } catch (error) {
        console.error(error);
    }
};

export default function Clients() {
    const [selectionType, setSelectionType] = useState('checkbox');
    const [data, setData] = useState([]);
    const [selectedRowKeys, setSelectedRowKeys] = useState([]);
    const navigate = useNavigate();

    const rowSelection = {
        onChange: (selectedRowKeys, selectedRows) => {
            setSelectedRowKeys(selectedRowKeys);
        },
    };
    const handleDelete = async (selectedRowKeys, data, setData) => {
        // Delete the selected rows from the server
        console.log("Selected rows: ", selectedRowKeys);
        try {
            await UserService.delete_clients(selectedRowKeys);
            // Remove the selected rows from the local state
            setData(data.filter(row => !selectedRowKeys.includes(row.id)));
            setSelectedRowKeys([]);
        } catch (error) {
            console.error(error);
        }
    };
    useEffect(() => {
        const fetchData = async () => {
            const accessToken = Cookies.get('access_token');
            if (!accessToken) {
                navigate('/');
                return;
            }
            try {
                const response = await UserService.get_user_clients();
                setData(response.data);
            } catch (error) {
                console.error(error);
            }
        };

        fetchData();
    }, []);

    return (
        <div>

            <Table
                rowKey={record => record.id} // Add this line
                rowSelection={{
                    type: selectionType,
                    ...rowSelection,
                }}
                columns={columns}
                dataSource={data}
            />
            <Button className="ml-2" type="primary" icon={<DeleteOutlined/>}
                    onClick={() => handleDelete(selectedRowKeys, data, setData)}
                    disabled={selectedRowKeys.length === 0}>
                Delete
            </Button>
        </div>

    );
}