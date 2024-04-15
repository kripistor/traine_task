import axios from "axios";
import Cookies from 'js-cookie';

let serverPath = "http://localhost:8000/api/v1";
axios.interceptors.response.use(undefined, async error => {
    if (error.config && error.response && error.response.status === 401) {
        const refreshToken = Cookies.get('refresh_token');
        console.log(refreshToken)
        const response = await axios.post(serverPath + `/users/refresh?refresh_token=${refreshToken}`, {});
        console.log(response)
        Cookies.set('access_token', response.data.access_token);
        error.config.headers['Authorization'] = `Bearer ${response.data.access_token}`;
        return axios(error.config);
    }
    return Promise.reject(error);
});
export default class UserService {
    static async login(login, password) {
        const response = await axios.post(serverPath + "/users/login", {
            login: login, password: password
        });

        Cookies.set('access_token', response.data.access_token);
        Cookies.set('refresh_token', response.data.refresh_token);

        return response;
    }


    static async get_user_clients() {
        const accessToken = Cookies.get('access_token');

        const response = await axios.get(serverPath + "/users/clients", {
            headers: {
                'Authorization': `Bearer ${accessToken}`
            }
        });

        return response;
    }

    static async update_client_status(client_id, status) {
        const accessToken = Cookies.get('access_token');

        const response = await axios.put(serverPath + `/users/update_client?client_id=${client_id}&status=${status}`, {}, {
            headers: {
                'Authorization': `Bearer ${accessToken}`
            }
        });

        return response;
    }

    static async delete_clients(client_ids) {
        const accessToken = Cookies.get('access_token');

        const response = await axios.delete(serverPath + "/users/delete_clients", {
            data: client_ids, // Изменено с {client_ids: client_ids}
            headers: {
                'Authorization': `Bearer ${accessToken}`
            }
        });

        return response;
    }
}