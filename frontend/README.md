# Rep Mate Frontend

A mobile-first workout tracking application built with Vue.js and Tailwind CSS.

## Features

- 🏋️ Track exercises, sets, reps, and weight
- 📊 Real-time progress visualization with ring charts
- 📚 Exercise library with search functionality
- 🌙 Dark theme optimized for mobile devices
- 🔐 Authentication and user management

## Tech Stack

- **Vue 3** - Progressive JavaScript framework
- **Vite** - Next generation frontend tooling
- **Tailwind CSS** - Utility-first CSS framework
- **Vue Router** - Official router for Vue.js
- **Axios** - Promise-based HTTP client

## Getting Started

### Prerequisites

- Node.js 16+ and npm
- Backend API running (see `/backend` directory)

### Installation

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build
```

### Environment Variables

Create a `.env` file in the root directory:

```env
VITE_API_URL=http://localhost:8000
```

## Project Structure

```
src/
├── components/        # Reusable Vue components
│   └── BottomNav.vue # Bottom navigation bar
├── views/            # Page components
│   ├── HomeView.vue     # Main workout tracking page
│   ├── ProgressView.vue # Progress and analytics
│   ├── LibraryView.vue  # Exercise library
│   ├── ProfileView.vue  # User profile
│   └── LoginView.vue    # Authentication
├── router/           # Vue Router configuration
├── services/         # API services
│   └── api.js       # Backend API calls
├── App.vue          # Root component
└── main.js          # Application entry point
```

## Demo Mode

For testing without a backend, click "Continue with Demo Mode" on the login page. This will use mock data to demonstrate the UI.

## API Integration

The app connects to the Rep Mate backend API. Make sure the backend is running and the `VITE_API_URL` environment variable is set correctly.

## Development

The app is designed with a mobile-first approach and is optimized for a 414px viewport (iPhone dimensions). For the best development experience, use Chrome DevTools in mobile view.

## License

MIT
