import { Routes, Route, Navigate } from 'react-router-dom'
import DashboardLayout from './components/Sidebar/DashboardLayout.jsx'
import Login     from './pages/Auth/Login.jsx'
import Register  from './pages/Auth/Register.jsx'
import Dashboard from './pages/Dashboard/Dashboard.jsx'
import Profile   from './pages/Profile/Profile.jsx'
import FoodLog   from './pages/FoodLog/FoodLog.jsx'
import Summary   from './pages/Summary/Summary.jsx'
import Recommendations from './pages/Recommendations/Recommendations.jsx'
import ProtectedRoute  from './routes/ProtectedRoute.jsx'

export default function App() {
  return (
    <Routes>
      <Route path="/login"    element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route element={<ProtectedRoute />}>
        <Route element={<DashboardLayout />}>
          <Route path="/"                element={<Navigate to="/dashboard" replace />} />
          <Route path="/dashboard"       element={<Dashboard />} />
          <Route path="/profile"         element={<Profile />} />
          <Route path="/food-log"        element={<FoodLog />} />
          <Route path="/summary"         element={<Summary />} />
          <Route path="/recommendations" element={<Recommendations />} />
        </Route>
      </Route>
      <Route path="*" element={<Navigate to="/dashboard" replace />} />
    </Routes>
  )
}
