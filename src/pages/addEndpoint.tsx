```typescript
import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import * as yup from 'yup';
import axios from 'axios';
import { useRouter } from 'next/router';
import Header from '../components/Header';

const schema = yup.object().shape({
  name: yup.string().required('Name is required'),
  url: yup.string().required('URL is required').url('Invalid URL'),
  method: yup.string().required('Method is required'),
});

interface Endpoint {
  name: string;
  url: string;
  method: string;
}

const AddEndpoint = () => {
  const [endpoints, setEndpoints] = useState<Endpoint[]>([]);
  const { register, handleSubmit, errors } = useForm({
    resolver: yupResolver(schema),
  });
  const router = useRouter();

  const onSubmit = async (data: Endpoint) => {
    try {
      const response = await axios.post('/api/endpoints', data);
      setEndpoints([...endpoints, response.data]);
    } catch (error) {
      console.error(error);
    }
  };

  const fetchEndpoints = async () => {
    try {
      const response = await axios.get('/api/endpoints');
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
      <form onSubmit={handleSubmit(onSubmit)} className="max-w-md mx-auto p-4 border border-gray-300 rounded">
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
          {errors.name && <p className="text-red-500 text-xs italic">{errors.name.message}</p>}
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
          {errors.url && <p className="text-red-500 text-xs italic">{errors.url.message}</p>}
        </div>
        <div className="mb-4">
          <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="method">
            Method
          </label>
          <select
            className="block appearance-none w-full bg-gray-200 border border-gray-200 text-gray-700 py-3 px-4 pr-8 rounded leading-tight focus:outline-none focus:bg-white focus:border-gray-500"
            id="method"
            {...register('method')}
          >
            <option value="">Select a method</option>
            <option value="GET">GET</option>
            <option value="POST">POST</option>
            <option value="PUT">PUT</option>
            <option value="DELETE">DELETE</option>
          </select>
          {errors.method && <p className="text-red-500 text-xs italic">{errors.method.message}</p>}
        </div>
        <button
          className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
          type="submit"
        >
          Add Endpoint
        </button>
      </form>
      <h2 className="text-2xl font-bold mt-4">Added Endpoints</h2>
      <ul>
        {endpoints.map((endpoint) => (
          <li key={endpoint.name} className="py-2 border-b border-gray-300">
            <span className="text-gray-700">{endpoint.name}</span>
            <span className="text-gray-500 ml-2">{endpoint.url}</span>
            <span className="text-gray-500 ml-2">{endpoint.method}</span>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default AddEndpoint;
```