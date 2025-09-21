// API client for communicating with the FastAPI backend
import { useAuth } from '@clerk/nextjs';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

class APIClient {
  constructor() {
    this.baseURL = API_BASE_URL;
  }

  async makeRequest(endpoint, options = {}) {
    // For client-side requests, we need to get the token differently
    let token = null;
    
    // Try to get token from Clerk auth context if available
    if (typeof window !== 'undefined') {
      // We'll need to pass the token as a parameter for client-side calls
      token = options.token;
    }

    const headers = {
      'Content-Type': 'application/json',
      ...options.headers,
    };

    if (token) {
      headers.Authorization = `Bearer ${token}`;
    }

    // Remove token from options to avoid passing it to fetch
    const { token: _, ...fetchOptions } = options;

    const config = {
      method: 'GET',
      ...fetchOptions,
      headers,
    };

    console.log(`Making request to: ${this.baseURL}${endpoint}`, { config });

    const response = await fetch(`${this.baseURL}${endpoint}`, config);

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
      throw new Error(error.detail || `HTTP ${response.status}`);
    }

    return response.json();
  }

  // Analytics endpoints
  async getAnalytics(token) {
    return this.makeRequest('/analytics/', { token });
  }

  async getMoodAnalytics(token) {
    return this.makeRequest('/analytics/mood', { token });
  }

  // Collection endpoints
  async getCollections(token) {
    return this.makeRequest('/collections/', { token });
  }

  async createCollection(data, token) {
    return this.makeRequest('/collections/', {
      method: 'POST',
      body: JSON.stringify(data),
      token,
    });
  }

  async getCollection(collectionId, token) {
    return this.makeRequest(`/collections/${collectionId}`, { token });
  }

  async updateCollection(collectionId, data, token) {
    return this.makeRequest(`/collections/${collectionId}`, {
      method: 'PUT',
      body: JSON.stringify(data),
      token,
    });
  }

  async deleteCollection(collectionId, token) {
    return this.makeRequest(`/collections/${collectionId}`, {
      method: 'DELETE',
      token,
    });
  }

  // Journal endpoints
  async getEntry(entryId, token) {
    return this.makeRequest(`/journal/entries/${entryId}`, { token });
  }

  async getCollectionEntries(collectionId, filters = {}, token) {
    const params = new URLSearchParams(filters);
    return this.makeRequest(`/journal/entries/collection/${collectionId}?${params}`, { token });
  }

  async createEntry(data, token) {
    return this.makeRequest('/journal/entries', {
      method: 'POST',
      body: JSON.stringify(data),
      token,
    });
  }

  async updateEntry(entryId, data, token) {
    return this.makeRequest(`/journal/entries/${entryId}`, {
      method: 'PUT',
      body: JSON.stringify(data),
      token,
    });
  }

  async deleteEntry(entryId, token) {
    return this.makeRequest(`/journal/entries/${entryId}`, {
      method: 'DELETE',
      token,
    });
  }

  // Draft endpoints
  async getDraft(token) {
    return this.makeRequest('/journal/draft', { token });
  }

  async saveDraft(data, token) {
    return this.makeRequest('/journal/draft', {
      method: 'POST',
      body: JSON.stringify(data),
      token,
    });
  }

  async deleteDraft(token) {
    return this.makeRequest('/journal/draft', {
      method: 'DELETE',
      token,
    });
  }

  // Public endpoints (no auth required)
  async getDailyPrompt() {
    return this.makeRequest('/public/daily-prompt');
  }

  // getMoodImage removed (Pixabay removed)
}

// Create a hook to use the API client with auth
export const useApiClient = () => {
  const { getToken, isLoaded } = useAuth();
  
  const client = new APIClient();
  
  // Don't try to get token during SSR
  const getTokenSafely = async () => {
    if (typeof window === 'undefined' || !isLoaded) {
      return null;
    }
    return await getToken();
  };
  
  // Wrap all methods to automatically include token
  const wrappedClient = {
    async getAnalytics() {
      const token = await getTokenSafely();
      return client.getAnalytics(token);
    },
    
    async getMoodAnalytics() {
      const token = await getTokenSafely();
      return client.getMoodAnalytics(token);
    },
    
    async getCollections() {
      const token = await getTokenSafely();
      return client.getCollections(token);
    },
    
    async createCollection(data) {
      const token = await getTokenSafely();
      return client.createCollection(data, token);
    },
    
    async getCollection(collectionId) {
      const token = await getTokenSafely();
      return client.getCollection(collectionId, token);
    },
    
    async updateCollection(collectionId, data) {
      const token = await getTokenSafely();
      return client.updateCollection(collectionId, data, token);
    },
    
    async deleteCollection(collectionId) {
      const token = await getTokenSafely();
      return client.deleteCollection(collectionId, token);
    },
    
    async getEntry(entryId) {
      const token = await getTokenSafely();
      return client.getEntry(entryId, token);
    },
    
    async getCollectionEntries(collectionId, filters = {}) {
      const token = await getTokenSafely();
      return client.getCollectionEntries(collectionId, filters, token);
    },
    
    async createEntry(data) {
      const token = await getTokenSafely();
      return client.createEntry(data, token);
    },
    
    async updateEntry(entryId, data) {
      const token = await getTokenSafely();
      return client.updateEntry(entryId, data, token);
    },
    
    async deleteEntry(entryId) {
      const token = await getTokenSafely();
      return client.deleteEntry(entryId, token);
    },
    
    async getDraft() {
      const token = await getTokenSafely();
      return client.getDraft(token);
    },
    
    async saveDraft(data) {
      const token = await getTokenSafely();
      return client.saveDraft(data, token);
    },
    
    async deleteDraft() {
      const token = await getTokenSafely();
      return client.deleteDraft(token);
    },
    
    // Public endpoints
    getDailyPrompt: () => client.getDailyPrompt(),
  };
  
  return wrappedClient;
};

export const apiClient = new APIClient();
