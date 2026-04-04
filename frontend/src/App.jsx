import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Suspense, lazy } from 'react';
import Navbar from './components/common/Navbar';
import Footer from './components/common/Footer';
import LoadingSpinner from './components/common/LoadingSpinner';

// Lazy load pages for code splitting
const HomePage = lazy(() => import('./pages/HomePage'));
const LoginPage = lazy(() => import('./pages/LoginPage'));
const RegisterPage = lazy(() => import('./pages/RegisterPage'));
const ProfilePage = lazy(() => import('./pages/ProfilePage'));
const LinkDetailPage = lazy(() => import('./pages/LinkDetailPage'));
const SubmitLinkPage = lazy(() => import('./pages/SubmitLinkPage'));
const ExplorePage = lazy(() => import('./pages/ExplorePage'));
const GraphPage = lazy(() => import('./pages/GraphPage'));
const RoomsPage = lazy(() => import('./pages/RoomsPage'));
const ChatRoomPage = lazy(() => import('./pages/ChatRoomPage'));
const ToolsPage = lazy(() => import('./pages/ToolsPage'));
const LeaderboardPage = lazy(() => import('./pages/LeaderboardPage'));
const RandomLinkPage = lazy(() => import('./pages/RandomLinkPage'));

function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <main className="container">
        <Suspense fallback={<LoadingSpinner />}>
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route path="/profile/:username" element={<ProfilePage />} />
            <Route path="/link/:id" element={<LinkDetailPage />} />
            <Route path="/submit" element={<SubmitLinkPage />} />
            <Route path="/explore" element={<ExplorePage />} />
            <Route path="/graph/:tag" element={<GraphPage />} />
            <Route path="/rooms" element={<RoomsPage />} />
            <Route path="/room/:id" element={<ChatRoomPage />} />
            <Route path="/tools" element={<ToolsPage />} />
            <Route path="/leaderboard" element={<LeaderboardPage />} />
            <Route path="/random" element={<RandomLinkPage />} />
          </Routes>
        </Suspense>
      </main>
      <Footer />
    </BrowserRouter>
  );
}

export default App;