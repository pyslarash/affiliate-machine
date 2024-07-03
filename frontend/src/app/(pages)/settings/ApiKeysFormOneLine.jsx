import { useState, useEffect } from 'react';
import { Input } from "@nextui-org/input";
import { Button } from "@nextui-org/button";
import { PlusIcon, TrashIcon } from '@heroicons/react/24/outline';
import axios from 'axios';
import { EyeIcon, EyeSlashIcon } from '@heroicons/react/24/outline';

export default function ApiKeysFormOneLine({ userData, getCall, postCall, putCall, deleteCall, apiName, colName, apiMsg, apiEMsg }) {
  const [apiKey, setApiKey] = useState('');
  const [cred, setCred] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [isVisible, setIsVisible] = useState(false);
  const toggleVisibility = () => setIsVisible(!isVisible);

  const handleApiKeyChange = (value) => {
    setApiKey(value);
  };

  // useEffect to fetch API keys on component mount
  useEffect(() => {
    fetchCredentials();
  }, []);

  const fetchCredentials = () => {
    const token = localStorage.getItem('token');
    axios.get(`${process.env.NEXT_PUBLIC_BACKEND}/${getCall}`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
      .then(response => {
        if (response.status === 200) {
          setApiKey(response.data[colName]); // Update apiKey state with fetched data
          setCred(true);
        } else if (response.status === 404) {
          // Handle case where no API credentials are found
          setCred(false);
        } else {
          console.error('Error fetching API credentials:', response);
          setCred(false);
        }
      })
      .catch(error => {
        console.error('Error fetching API credentials:', error);
        setCred(false);
      });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const token = localStorage.getItem('token');

    if (!apiKey) {
      apiEMsg(`${apiName} API Key is required.`);
      return;
    }

    const requestData = { [colName]: apiKey }; // Use colName for the key in the request payload

    if (!cred) {
      axios.post(`${process.env.NEXT_PUBLIC_BACKEND}/${postCall}`, requestData, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      })
        .then(response => {
          apiMsg(response.data.message);
          apiEMsg('');
          setCred(true);
        })
        .catch(error => {
          apiEMsg(error.response && error.response.data.message
            ? error.response.data.message
            : 'Setting failed. Please check your input and try again.');
        });
    } else {
      axios.put(`${process.env.NEXT_PUBLIC_BACKEND}/${putCall}`, requestData, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      })
        .then(response => {
          apiMsg(response.data.message);
          apiEMsg('');
        })
        .catch(error => {
          apiEMsg(error.response && error.response.data.message
            ? error.response.data.message
            : 'Update failed. Please check your input and try again.');
        });
    }
  };

  const deleteApiKey = async () => {
    setIsLoading(true);
    try {
      const token = localStorage.getItem('token');
      const response = await axios.delete(`${process.env.NEXT_PUBLIC_BACKEND}/${deleteCall}`, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      apiMsg(response.data.message);
      apiEMsg('');
      setApiKey('');
      setCred(false);
    } catch (error) {
      apiEMsg(error.response && error.response.data.message
        ? error.response.data.message
        : `Failed to delete ${apiName} API key. Please try again.`);
      console.error(`Error deleting ${apiName} API key:`, error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="w-full max-w">
      <form onSubmit={handleSubmit}>
        <div className="grid grid-cols-1 gap-y-2">
          {userData && (
            <div>
              <div className="flex items-center space-x-2 mb-2">
                <Input
                  size="md"
                  label={`${apiName} API Key`}
                  placeholder={`Enter ${apiName} API Key`}
                  value={apiKey}
                  onChange={(e) => handleApiKeyChange(e.target.value)}
                  endContent={
                    <Button className="focus:outline-none" type="button" onClick={toggleVisibility}>
                      {isVisible ? (
                        <EyeSlashIcon className="w-6 h-6 text-default-400 pointer-events-none" />
                      ) : (
                        <EyeIcon className="w-6 h-6 text-default-400 pointer-events-none" />
                      )}
                    </Button>
                  }
                  type={isVisible ? "text" : "password"}
                />
                <Button
                  isIconOnly
                  color="success"
                  aria-label={`Save or Update ${apiName} API Key`}
                  type="submit"
                  disabled={isLoading}
                >
                  <PlusIcon className="h-5 w-5" />
                </Button>
                <Button
                  isIconOnly
                  color="danger"
                  aria-label={`Delete ${apiName} API Key`}
                  onClick={deleteApiKey}
                  disabled={isLoading}
                >
                  <TrashIcon className="h-5 w-5" />
                </Button>
              </div>
            </div>
          )}
        </div>
      </form>
    </div>
  );
}