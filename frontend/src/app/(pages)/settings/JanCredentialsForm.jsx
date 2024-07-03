import { useState, useEffect } from 'react';
import { Input } from "@nextui-org/input";
import { Button } from "@nextui-org/button";
import axios from 'axios';

export default function JanCredentialsForm({ userData }) {
    const [janMessage, setJanMessage] = useState('');
    const [janErrorMessage, setJanErrorMessage] = useState('');
    const [janCred, setJanCred] = useState(false);
    const [janData, setJanData] = useState({
        jan_ip: '',
        jan_port: '',
        jan_prefix: ''
    });

    // useEffect to set JAN data if available in userData
    useEffect(() => {
        fetchJanCredentials();
    }, []);

    const fetchJanCredentials = () => {
        const token = localStorage.getItem('token');
        axios.get(`${process.env.NEXT_PUBLIC_BACKEND}/get_credentials`, {
            headers: {
                Authorization: `Bearer ${token}`
            }
        })
            .then(response => {
                if (response.status === 200) {
                    const { jan_ip, jan_port, jan_prefix } = response.data;
                    setJanData({
                        jan_ip,
                        jan_port,
                        jan_prefix
                    });
                    setJanCred(true);
                } else if (response.status === 404) {
                    // Handle case where no Jan credentials are found
                    setJanCred(false);
                } else {
                    console.error('Error fetching Jan.ai credentials:', response);
                    setJanCred(false);
                }
            })
            .catch(error => {
                console.error('Error fetching Jan.ai credentials:', error);
                setJanCred(false);
            });
    };

    const handleChange = (name, value) => {
        setJanData(prevJanData => ({
            ...prevJanData,
            [name]: value
        }));
    };

    const handleSubmitJan = (e) => {
        e.preventDefault();
        const token = localStorage.getItem('token');
        const { jan_ip, jan_port, jan_prefix } = janData;

        if (!jan_ip || !jan_port || !jan_prefix) {
            setJanErrorMessage('All Jan.ai fields are required.');
            return;
        }

        const updatedJanData = { jan_ip, jan_port, jan_prefix };

        if (!janCred) {
            axios.post(`${process.env.NEXT_PUBLIC_BACKEND}/set_credentials`, updatedJanData, {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            })
                .then(response => {
                    setJanMessage(response.data.message);
                    setJanErrorMessage('');
                    setJanCred(true);
                })
                .catch(error => {
                    setJanErrorMessage(error.response && error.response.data.message
                        ? error.response.data.message
                        : 'Update failed. Please check your input and try again.');
                });
        } else {
            axios.put(`${process.env.NEXT_PUBLIC_BACKEND}/update_credentials`, updatedJanData, {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            })
                .then(response => {
                    setJanMessage(response.data.message);
                    setJanErrorMessage('');
                })
                .catch(error => {
                    setJanErrorMessage(error.response && error.response.data.message
                        ? error.response.data.message
                        : 'Update failed. Please check your input and try again.');
                });
        }
    };

    return (
        <div className="w-full max-w">
            <form onSubmit={handleSubmitJan}>                
                <div className="grid grid-cols-1">
                    <div>
                        <div className="group relative mb-2">
                            <Input
                                size="md"
                                type="text"
                                label="Jan.ai IP"
                                placeholder="Enter Jan.ai IP"
                                value={janData.jan_ip}
                                onChange={(e) => handleChange('jan_ip', e.target.value)}
                            />
                        </div>
                        <div className="group relative mb-2">
                            <Input
                                size="md"
                                type="text"
                                label="Jan.ai Port"
                                placeholder="Enter Jan.ai Port"
                                value={janData.jan_port}
                                onChange={(e) => handleChange('jan_port', e.target.value)}
                            />
                        </div>
                        <div className="group relative mb-2">
                            <Input
                                size="md"
                                type="text"
                                label="Jan.ai Prefix"
                                placeholder="Enter Jan.ai Prefix"
                                value={janData.jan_prefix}
                                onChange={(e) => handleChange('jan_prefix', e.target.value)}
                            />
                        </div>
                        <Button className="button-text w-full" type="submit" color="primary" auto>
                            Update Jan
                        </Button>
                        {(janErrorMessage && (
                            <p className="text-center text-sm text-red-600 mt-1">{janErrorMessage}</p>
                        )) ||
                            (janMessage && (
                                <p className="text-center text-sm text-green-600 mt-1">{janMessage}</p>
                            ))}
                    </div>
                </div>
            </form>
        </div>
    );
}
