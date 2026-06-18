import React, { useState } from 'react';
import { useRouter } from 'next/router';
import { useSession } from '../utils/auth';
import axios from 'axios';
import { toast } from 'react-toastify';

const AddWebhook = () => {
  const [webhookUrl, setWebhookUrl] = useState('');
  const [webhookEvent, setWebhookEvent] = useState('');
  const [webhookSecret, setWebhookSecret] = useState('');
  const [isTesting, setIsTesting] = useState(false);
  const router = useRouter();
  const { session } = useSession();

  const handleAddWebhook = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    try {
      const response = await axios.post('/api/webhooks', {
        webhookUrl,
        webhookEvent,
        webhookSecret,
      }, {
        headers: {
          Authorization: `Bearer ${session.token}`,
        },
      });
      toast.success('Webhook added successfully');
      router.push('/webhooks');
    } catch (error) {
      toast.error('Error adding webhook');
    }
  };

  const handleTestWebhook = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setIsTesting(true);
    try {
      const response = await axios.post('/api/webhooks/test', {
        webhookUrl,
        webhookEvent,
        webhookSecret,
      }, {
        headers: {
          Authorization: `Bearer ${session.token}`,
        },
      });
      toast.success('Webhook tested successfully');
    } catch (error) {
      toast.error('Error testing webhook');
    } finally {
      setIsTesting(false);
    }
  };

  return (
    <div className="max-w-md mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Add Webhook</h1>
      <form onSubmit={handleAddWebhook}>
        <div className="mb-4">
          <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="webhookUrl">
            Webhook URL
          </label>
          <input
            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            id="webhookUrl"
            type="text"
            value={webhookUrl}
            onChange={(e) => setWebhookUrl(e.target.value)}
          />
        </div>
        <div className="mb-4">
          <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="webhookEvent">
            Webhook Event
          </label>
          <select
            className="block appearance-none w-full bg-gray-200 border border-gray-200 text-gray-700 py-3 px-4 pr-8 rounded leading-tight focus:outline-none focus:bg-white focus:border-gray-500"
            id="webhookEvent"
            value={webhookEvent}
            onChange={(e) => setWebhookEvent(e.target.value)}
          >
            <option value="">Select an event</option>
            <option value="api_down">API Down</option>
            <option value="api_up">API Up</option>
          </select>
        </div>
        <div className="mb-4">
          <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="webhookSecret">
            Webhook Secret
          </label>
          <input
            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            id="webhookSecret"
            type="text"
            value={webhookSecret}
            onChange={(e) => setWebhookSecret(e.target.value)}
          />
        </div>
        <button
          className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
          type="submit"
        >
          Add Webhook
        </button>
      </form>
      <form onSubmit={handleTestWebhook}>
        <button
          className="bg-orange-500 hover:bg-orange-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
          type="submit"
          disabled={isTesting}
        >
          {isTesting ? 'Testing...' : 'Test Webhook'}
        </button>
      </form>
    </div>
  );
};

export default AddWebhook;