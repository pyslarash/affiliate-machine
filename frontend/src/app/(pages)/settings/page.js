'use client'

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import AccountForm from './AccountForm';
import JanCredentialsForm from './JanCredentialsForm';
import ApiKeysFormOneLine from './ApiKeysFormOneLine';
import ApiKeysFormTwoLine from './ApiKeysFormTwoLine';
import axios from 'axios';

export default function Settings() {
  const router = useRouter();
  const [apiMessage, setApiMessage] = useState('');
  const [apiErrorMessage, setApiErrorMessage] = useState('');
  const [userData, setUserData] = useState(null);
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    first_name: '',
    last_name: '',
    password: ''
  });

  useEffect(() => {
    const token = localStorage.getItem('token');
    const expirationTime = localStorage.getItem('expiration_time');
    const userID = localStorage.getItem('user_id');

    if (!token || !expirationTime || Date.now() > parseInt(expirationTime)) {
      redirectToLogin();
    } else {
      // Fetch user account information
      axios.get(`${process.env.NEXT_PUBLIC_BACKEND}/get_user/${userID}`, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      })
        .then(response => {
          setUserData(response.data);
          setFormData({
            username: response.data.username,
            email: response.data.email,
            first_name: response.data.first_name,
            last_name: response.data.last_name,
            password: ''
          });
        })
        .catch(error => {
          console.error('Error fetching user data:', error);
        });
    }
  }, []);

  const redirectToLogin = () => {
    window.location.href = '/login';
  };

  return (
    <div className="container mx-auto px-4">
      <h1 className='my-4'>Settings</h1>
      <div className="flex justify-between">
        {/* Left Column: Account Information */}
        <div className="flex flex-col space-y-4 w-full">
          <AccountForm
            formData={formData}
            userData={userData}
            setFormData={setFormData}
          />
        </div>
        {/* Right Column */}
        <div className="flex flex-col space-y-2 w-full">
          <h2>Jan.ai Credentials</h2>
          {/* JAN Credentials */}
          <JanCredentialsForm
            userData={userData}
          />
          {/* API Keys */}
          <h2>API Keys</h2>
          {/* OpenAI */}
          <ApiKeysFormOneLine
            userData={userData}
            getCall={'get_open_ai_api_key'}
            postCall={'save_open_ai_api_key'}
            putCall={'update_open_ai_api_key'}
            deleteCall={'delete_open_ai_api_key'}
            apiName={'OpenAI'}
            colName={'open_ai_api_key'}
            apiMsg={setApiMessage}
            apiEMsg={setApiErrorMessage}
          />
          <ApiKeysFormTwoLine 
            userData={userData}
            getCall={'get_google_api_keys'}
            postCall={'save_google_api_keys'}
            putCall={'update_google_api_keys'}
            deleteCall={'delete_google_api_keys'}
            apiName={'Google'}
            apiNameOne={'Google Search'}
            apiNameTwo={'Google CX'}
            colOneName={'google_search_api_key'}
            colTwoName={'google_cx'}
            apiMsg={setApiMessage}
            apiEMsg={setApiErrorMessage}
          />
          <ApiKeysFormOneLine
            userData={userData}
            getCall={'get_myaddr_api_key'}
            postCall={'save_myaddr_api_key'}
            putCall={'update_myaddr_api_key'}
            deleteCall={'delete_myaddr_api_key'}
            apiName={'MyAddr'}
            colName={'myaddr_api_key'}
            apiMsg={setApiMessage}
            apiEMsg={setApiErrorMessage}
          />
          <ApiKeysFormTwoLine 
            userData={userData}
            getCall={'get_porkbun_api_keys'}
            postCall={'save_porkbun_api_keys'}
            putCall={'update_porkbun_api_keys'}
            deleteCall={'delete_porkbun_api_keys'}
            apiName={'Porkbun'}
            apiNameOne={'Porkbun'}
            apiNameTwo={'Porkbun Secret'}
            colOneName={'porkbun_api_key'}
            colTwoName={'porkbun_secret'}
            apiMsg={setApiMessage}
            apiEMsg={setApiErrorMessage}
          />
          <ApiKeysFormTwoLine 
            userData={userData}
            getCall={'get_czds_credentials'}
            postCall={'save_czds_credentials'}
            putCall={'update_czds_credentials'}
            deleteCall={'delete_czds_credentials'}
            apiName={'CZDS ICANN'}
            apiNameOne={'CZDS Login'}
            apiNameTwo={'CZDS Password'}
            colOneName={'czds_login'}
            colTwoName={'czds_password'}
            apiMsg={setApiMessage}
            apiEMsg={setApiErrorMessage}
          />
          {/* Display error and success messages */}
          {(apiErrorMessage && (
            <p className="text-center text-sm text-red-600">{apiErrorMessage}</p>
          )) ||
          (apiMessage && (
            <p className="text-center text-sm text-green-600">{apiMessage}</p>
          ))}
        </div>
      </div>
    </div>
  );
}
