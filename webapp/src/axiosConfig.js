// axiosConfig.js
import axios from 'axios';

// Create an instance of axios with default properties
const axiosInstance = axios.create({
    baseURL: 'https://edh-reshuffle-api.azurewebsites.net/', // Set your API base URL here
});

// Request interceptor
axiosInstance.interceptors.request.use(
    config => {
        // Perform actions before the request is sent
        // For example, attaching an auth token to the header
        // config.headers.Authorization = 'Bearer your-auth-token';
        return config;
    },
    error => {
        // Handle request errors
        return Promise.reject(error);
    }
);

// Response interceptor
axiosInstance.interceptors.response.use(
    response => {
        // Perform actions with response data
        return response;
    },
    error => {
        // Handle response errors
        // For example, redirecting on a 401 unauthorized error
        if (error.response && error.response.status === 401) {
            // Redirect to login or perform any action
        }
        return Promise.reject(error);
    }
);

export default axiosInstance;
