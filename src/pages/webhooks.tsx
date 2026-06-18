import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import { useSession } from '../utils/auth';
import axios from 'axios';
import { Webhook } from '../models/webhook';
import { toast } from 'react-toastify';

const WebhooksPage = () => {
  const [webhooks, setWebhooks] = useState<Webhook[]>([]);
  const [newWebhook, setNewWebhook] = useState<Webhook>({ url: '', method: 'POST' });
  const [loading, setLoading] = useState(false);
  const router = useRouter();
  const session = useSession();

  useEffect(() => {
    if (!session) {
      router.push('/login');
    } else {
      axios.get('/api/webhooks')
        .then(response => {
          setWebhooks(response.data);
        })
        .catch(error => {
          toast.error('Error fetching webhooks');
        });
    }
  }, [session, router]);

  const handleAddWebhook = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setLoading(true);
    axios.post('/api/webhooks', newWebhook)
      .then(response => {
        setWebhooks([...webhooks, response.data]);
        setNewWebhook({ url: '', method: 'POST' });
        setLoading(false);
      })
      .catch(error => {
        toast.error('Error adding webhook');
        setLoading(false);
      });
  };

  const handleTestWebhook = (webhook: Webhook) => {
    axios.post('/api/webhooks/test', webhook)
      .then(response => {
        toast.success('Webhook test successful');
      })
      .catch(error => {
        toast.error('Error testing webhook');
      });
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-4">Webhooks</h1>
      <form onSubmit={handleAddWebhook}>
        <div className="flex flex-col mb-4">
          <label className="text-lg font-bold mb-2">URL:</label>
          <input
            type="text"
            value={newWebhook.url}
            onChange={(event) => setNewWebhook({ ...newWebhook, url: event.target.value })}
            className="p-2 border border-gray-400 rounded"
          />
        </div>
        <div className="flex flex-col mb-4">
          <label className="text-lg font-bold mb-2">Method:</label>
          <select
            value={newWebhook.method}
            onChange={(event) => setNewWebhook({ ...newWebhook, method: event.target.value })}
            className="p-2 border border-gray-400 rounded"
          >
            <option value="POST">POST</option>
            <option value="GET">GET</option>
          </select>
        </div>
        <button
          type="submit"
          disabled={loading}
          className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
        >
          {loading ? 'Adding...' : 'Add Webhook'}
        </button>
      </form>
      <ul>
        {webhooks.map((webhook) => (
          <li key={webhook.id} className="mb-4">
            <div className="flex justify-between">
              <span>{webhook.url}</span>
              <button
                onClick={() => handleTestWebhook(webhook)}
                className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded"
              >
                Test
              </button>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default WebhooksPage;