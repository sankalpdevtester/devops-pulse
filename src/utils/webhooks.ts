import axios from 'axios';
import { toast } from 'react-toastify';

const triggerWebhook = async (webhookUrl: string, webhookEvent: string, webhookSecret: string) => {
  try {
    const response = await axios.post(webhookUrl, {
      event: webhookEvent,
      secret: webhookSecret,
    });
    if (response.status === 200) {
      return true;
    } else {
      throw new Error(`Webhook failed with status code ${response.status}`);
    }
  } catch (error) {
    throw new Error(`Error triggering webhook: ${error.message}`);
  }
};

const testWebhook = async (webhookUrl: string, webhookEvent: string, webhookSecret: string) => {
  try {
    const response = await axios.post(webhookUrl, {
      event: webhookEvent,
      secret: webhookSecret,
    });
    if (response.status === 200) {
      return true;
    } else {
      throw new Error(`Webhook failed with status code ${response.status}`);
    }
  } catch (error) {
    throw new Error(`Error testing webhook: ${error.message}`);
  }
};

const getWebhooks = async () => {
  try {
    const response = await axios.get('/api/webhooks');
    return response.data;
  } catch (error) {
    throw new Error(`Error getting webhooks: ${error.message}`);
  }
};

export { triggerWebhook, testWebhook, getWebhooks };