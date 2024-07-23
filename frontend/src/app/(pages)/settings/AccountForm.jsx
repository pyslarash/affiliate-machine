import { useState } from 'react';
import { Input } from "@nextui-org/input";
import { Button } from "@nextui-org/button";
import axios from 'axios';
import { EyeIcon, EyeSlashIcon } from '@heroicons/react/24/outline';

export default function AccountForm({ formData, userData, setFormData }) {
  const [accountMessage, setAccountMessage] = useState('');
  const [accountErrorMessage, setAccountErrorMessage] = useState('');
  const [isVisible, setIsVisible] = useState(false);
  const toggleVisibility = () => setIsVisible(!isVisible);

  // Dealing with account
  const handleSubmitAccount = (e) => {
    e.preventDefault();
    const token = localStorage.getItem('token');
    const userID = localStorage.getItem('user_id');

    axios.put(`${process.env.NEXT_PUBLIC_BACKEND}/edit_user/${userID}`, formData, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
      .then(response => {
        setAccountMessage(response.data.message);
        // Clear the error message on success
        setAccountErrorMessage('');
      })
      .catch(error => {
        setAccountErrorMessage(error.response && error.response.data.message
          ? error.response.data.message
          : 'Update failed. Please check your input and try again.');
      });
  };

  const formatLabel = (key) => {
    return key.replace(/_/g, ' ')
      .split(' ')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ');
  };

  const handleInputChange = (key, value) => {
    setFormData(prevFormData => ({
      ...prevFormData,
      [key]: value
    }));
  };

  return (
    <div className="w-full max-w px-4">
      <form onSubmit={handleSubmitAccount}>
        <h2 className='mb-2'>Account</h2>
        <div className="grid grid-cols-1 gap-y-2">
        {userData && (
            <div>
              {Object.keys(formData).map((key, index) => (
                <div className="group relative mb-2" key={index}>
                  <Input
                    size="md"
                    type={key === 'password' ? (isVisible ? 'text' : 'password') : 'text'}
                    label={formatLabel(key)}
                    placeholder={`Change ${formatLabel(key)}`}
                    value={formData[key]}
                    onChange={(e) => handleInputChange(key, e.target.value)}
                    endContent={
                      key === 'password' && (
                        <Button className="focus:outline-none" type="button" onClick={toggleVisibility}>
                          {isVisible ? (
                            <EyeSlashIcon className="w-6 h-6 text-default-400 pointer-events-none" />
                          ) : (
                            <EyeIcon className="w-6 h-6 text-default-400 pointer-events-none" />
                          )}
                        </Button>
                      )
                    }
                  />
                </div>
              ))}
            </div>
          )}
          <Button className="button-text w-full" type="submit" color="primary" auto>
            Update Account
          </Button>
          {(accountErrorMessage && (
            <p className="text-center text-sm text-red-600 mt-1">{accountErrorMessage}</p>
          )) ||
            (accountMessage && (
              <p className="text-center text-sm text-green-600 mt-1">{accountMessage}</p>
            ))}
        </div>
      </form>
    </div>
  );
}