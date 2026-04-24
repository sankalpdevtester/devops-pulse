```typescript
import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import * as yup from 'yup';
import axios from 'axios';
import { API_URL } from '../utils/helpers';
import Header from '../components/Header';

interface Endpoint {
  id: number;
  name: string;
  url: string;
}

const schema = yup.object().shape({
  name: yup.string().required('Name is required'),
  url: yup.string().required('URL is required').url('Invalid URL'),
});

const AddEndpoint = () => {
  const [endpoints, setEndpoints] = useState<Endpoint[]>([]);
  const { register, handleSubmit, errors } = useForm({
    resolver: yupResolver(schema),
  });

  const onSubmit = async (data: any) => {
    try {
      const response = await axios.post(`${API_URL}/endpoints`, data);
      setEndpoints([...endpoints, response.data]);
    } catch (error) {
      console.error(error);
    }
  };

  const fetchEndpoints = async () => {
    try {
      const response = await axios.get(`${API_URL}/endpoints`);
      setEndpoints(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  React.useEffect(() => {
    fetchEndpoints();
  }, []);

  return (
    <div>
      <Header />
      <h1 className="text-3xl font-bold mb-4">Add API Endpoint</h1>
      <form onSubmit={handleSubmit(onSubmit)}>
        <div className="mb-4">
          <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="name">
            Name
          </label>
          <input
            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            id="name"
            type="text"
            {...register('name')}
          />
          {errors.name && <div className="text-red-500 text-xs">{errors.name.message}</div>}
        </div>
        <div className="mb-4">
          <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="url">
            URL
          </label>
          <input
            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            id="url"
            type="text"
            {...register('url')}
          />
          {errors.url && <div className="text-red-500 text-xs">{errors.url.message}</div>}
        </div>
        <button
          className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
          type="submit"
        >
          Add Endpoint
        </button>
      </form>
      <h2 className="text-2xl font-bold mt-4">Added Endpoints</h2>
      <ul>
        {endpoints.map((endpoint) => (
          <li key={endpoint.id}>
            <span className="text-gray-700">{endpoint.name}</span>
            <span className="text-gray-500"> - {endpoint.url}</span>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default AddEndpoint;
```