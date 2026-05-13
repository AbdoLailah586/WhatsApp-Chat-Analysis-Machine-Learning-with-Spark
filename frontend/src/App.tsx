import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ThemeProvider } from './components/ThemeProvider';
import { Layout } from './components/Layout/Layout';
import Home from './pages/Home';
import Dashboard from './pages/Dashboard';
import Messages from './pages/Messages';
import { Toaster } from 'sonner';

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider>
        <BrowserRouter>
          <Layout>
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/dashboard/:uploadId" element={<Dashboard />} />
              <Route path="/messages/:uploadId" element={<Messages />} />
            </Routes>
          </Layout>
          <Toaster position="top-center" />
        </BrowserRouter>
      </ThemeProvider>
    </QueryClientProvider>
  );
}

export default App;
