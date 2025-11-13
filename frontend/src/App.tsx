
/**
 * Main App component
 */
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { CssBaseline } from '@mui/material';
import { AuthProvider } from './contexts/AuthContext';
import Layout from './components/Layout';
import ProtectedRoute from './components/ProtectedRoute';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Devices from './pages/Devices';
import DeviceHealth from './pages/DeviceHealth';
import Rules from './pages/Rules';
import Incidents from './pages/Incidents';
import OperationalModels from './pages/OperationalModels';

// Create theme
const theme = createTheme({
  palette: {
    primary: {
      main: '#1976D2',
    },
    secondary: {
      main: '#FF6B35',
    },
    success: {
      main: '#4CAF50',
    },
    warning: {
      main: '#FFC107',
    },
    error: {
      main: '#F44336',
    },
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
  },
});

const App: React.FC = () => {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <AuthProvider>
        <Router>
          <Routes>
            {/* Public routes */}
            <Route path="/login" element={<Login />} />

            {/* Protected routes */}
            <Route
              path="/"
              element={
                <ProtectedRoute>
                  <Layout>
                    <Dashboard />
                  </Layout>
                </ProtectedRoute>
              }
            />
            <Route
              path="/devices"
              element={
                <ProtectedRoute>
                  <Layout>
                    <Devices />
                  </Layout>
                </ProtectedRoute>
              }
            />
            <Route
              path="/device-health"
              element={
                <ProtectedRoute>
                  <Layout>
                    <DeviceHealth />
                  </Layout>
                </ProtectedRoute>
              }
            />
            <Route
              path="/rules"
              element={
                <ProtectedRoute>
                  <Layout>
                    <Rules />
                  </Layout>
                </ProtectedRoute>
              }
            />
            <Route
              path="/incidents"
              element={
                <ProtectedRoute>
                  <Layout>
                    <Incidents />
                  </Layout>
                </ProtectedRoute>
              }
            />
            <Route
              path="/operational-models"
              element={
                <ProtectedRoute>
                  <Layout>
                    <OperationalModels />
                  </Layout>
                </ProtectedRoute>
              }
            />

            {/* Catch-all redirect */}
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </Router>
      </AuthProvider>
    </ThemeProvider>
  );
};

export default App;
