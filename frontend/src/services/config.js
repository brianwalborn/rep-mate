/**
 * Runtime Configuration Service
 *
 * Provides access to environment variables that can be configured at runtime
 * (after the application is built). This allows the same Docker image to work
 * across different environments with different configurations.
 *
 * Configuration values are loaded from window.__ENV__ which is populated by
 * /config.js at runtime via envsubst in the Docker entrypoint script.
 */

class ConfigService {
  constructor() {
    this.env = window.__ENV__ || {};
  }

  /**
   * Get a configuration value with fallback chain
   * @param {string} key - The configuration key to retrieve
   * @param {string} fallback - Fallback value if key is not found
   * @returns {string} The configuration value
   */
  get(key, fallback = '') {
    // Check runtime config first (from window.__ENV__)
    if (this.env[key]) {
      return this.env[key];
    }

    // Fall back to build-time environment variables (for development)
    if (import.meta.env[`VITE_${key}`]) {
      return import.meta.env[`VITE_${key}`];
    }

    // Return fallback
    return fallback;
  }

  /**
   * Get the API base URL
   * @returns {string} The API base URL
   */
  getApiUrl() {
    return this.get('API_URL', 'http://localhost:8000');
  }

  /**
   * Check if running in production mode
   * @returns {boolean} True if in production
   */
  isProduction() {
    return import.meta.env.PROD;
  }

  /**
   * Check if running in development mode
   * @returns {boolean} True if in development
   */
  isDevelopment() {
    return import.meta.env.DEV;
  }

  /**
   * Get all runtime configuration values
   * @returns {object} All configuration values
   */
  getAll() {
    return { ...this.env };
  }
}

// Export a singleton instance
export default new ConfigService();
