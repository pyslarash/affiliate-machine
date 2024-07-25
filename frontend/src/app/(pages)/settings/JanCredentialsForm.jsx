import { useState, useEffect } from 'react';
import { Input } from "@nextui-org/input";
import { Button } from "@nextui-org/react";
import axios from 'axios';

export default function OllamaCredentialsForm({ userData }) {
    const [ollamaMessage, setOllamaMessage] = useState('');
    const [ollamaErrorMessage, setOllamaErrorMessage] = useState('');
    const [ollamaIpData, setOllamaIpData] = useState({
        ollama_ip: '',
        ollama_port: ''
    });
    const [ollamaWebData, setOllamaWebData] = useState({
        ollama_web_address: ''
    });

    useEffect(() => {
        const fetchData = async () => {
            const token = localStorage.getItem('token');
            
            try {
                // Fetch credentials data
                const credentialsResponse = await axios.get(`${process.env.NEXT_PUBLIC_BACKEND}/get_ollama_credentials`, {
                    headers: { Authorization: `Bearer ${token}` }
                });

                const { ollama_ip, ollama_port } = credentialsResponse.data;

                if (ollama_ip && ollama_port) {
                    // Set IP + Port data
                    setOllamaIpData({
                        ollama_ip,
                        ollama_port
                    });
                } else {
                    // Fetch web address data
                    const webResponse = await axios.get(`${process.env.NEXT_PUBLIC_BACKEND}/get_ollama_web`, {
                        headers: { Authorization: `Bearer ${token}` }
                    });

                    const { ollama_web_address } = webResponse.data;
                            
                    // Set web address data
                    setOllamaWebData({
                        ollama_web_address
                    });
                }
            } catch (error) {
                console.error('Error fetching Ollama data:', error);
            }
        };

        fetchData();
    }, []); // Empty dependency array ensures this runs once on component mount

    const handleChange = (name, value) => {
        if (name.startsWith('ollama_web')) {
            setOllamaWebData(prev => ({ ...prev, [name]: value }));
        } else {
            setOllamaIpData(prev => ({ ...prev, [name]: value }));
        }
    };

    const handleSubmitOllama = (e) => {
        e.preventDefault();
        const token = localStorage.getItem('token');

        const { ollama_ip, ollama_port } = ollamaIpData;
        const { ollama_web_address } = ollamaWebData;

        if ((ollama_ip && ollama_port) || ollama_web_address) {
            if (ollama_ip && ollama_port) {
                // Update IP + Port
                axios.put(`${process.env.NEXT_PUBLIC_BACKEND}/update_ollama_credentials`, { ollama_ip, ollama_port }, {
                    headers: { Authorization: `Bearer ${token}` }
                })
                    .then(response => {
                        setOllamaMessage(response.data.message);
                        setOllamaErrorMessage('');
                    })
                    .catch(error => {
                        setOllamaErrorMessage(error.response && error.response.data.message
                            ? error.response.data.message
                            : 'Update failed. Please check your input and try again.');
                    });
            } else {
                // Update Web Address
                axios.put(`${process.env.NEXT_PUBLIC_BACKEND}/update_ollama_web`, { ollama_web_address }, {
                    headers: { Authorization: `Bearer ${token}` }
                })
                    .then(response => {
                        setOllamaMessage(response.data.message);
                        setOllamaErrorMessage('');
                    })
                    .catch(error => {
                        setOllamaErrorMessage(error.response && error.response.data.message
                            ? error.response.data.message
                            : 'Update failed. Please check your input and try again.');
                    });
            }
        } else {
            setOllamaErrorMessage('Either IP and Port or Web Address is required.');
        }
    };

    return (
        <div className="w-full max-w">
            <form onSubmit={handleSubmitOllama}>
                <div className="grid grid-cols-1">
                    <div>
                        <div className="group relative mb-2">
                            <Input
                                size="md"
                                type="text"
                                label="Ollama IP"
                                placeholder="Enter Ollama IP"
                                value={ollamaIpData.ollama_ip}
                                onChange={(e) => handleChange('ollama_ip', e.target.value)}
                            />
                        </div>
                        <div className="group relative mb-2">
                            <Input
                                size="md"
                                type="text"
                                label="Ollama Port"
                                placeholder="Enter Ollama Port"
                                value={ollamaIpData.ollama_port}
                                onChange={(e) => handleChange('ollama_port', e.target.value)}
                            />
                        </div>
                        <div className="group relative mb-2">
                            <Input
                                size="md"
                                type="text"
                                label="Ollama Web Address"
                                placeholder="Enter Ollama Web Address"
                                value={ollamaWebData.ollama_web_address}
                                onChange={(e) => handleChange('ollama_web_address', e.target.value)}
                            />
                        </div>
                        <div className="flex gap-4 mb-4">
                            <Button className="button-text button-width" type="submit" color="primary" auto css={{ width: '100%' }}>
                                Update Ollama
                            </Button>
                        </div>
                        {(ollamaErrorMessage && (
                            <p className="text-center text-sm text-red-600 mt-1">{ollamaErrorMessage}</p>
                        )) ||
                            (ollamaMessage && (
                                <p className="text-center text-sm text-green-600 mt-1">{ollamaMessage}</p>
                            ))}
                    </div>
                </div>
            </form>
        </div>
    );
}
