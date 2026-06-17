import { NavLink, useNavigate } from 'react-router-dom'
import {
  MdDashboard, MdPerson, MdRestaurantMenu, MdBarChart,
  MdRecommend, MdLogout, MdMenuOpen, MdMenu,
} from 'react-icons/md'
import { useAuth } from '../../context/AuthContext.jsx'
import toast from 'react-hot-toast'

const NAV_ITEMS = [
  { to: '/dashboard',       icon: MdDashboard,      label: 'Dashboard' },
  { to: '/profile',         icon: MdPerson,         label: 'Profile' },
  { to: '/food-log',        icon: MdRestaurantMenu, label: 'Food Log' },
  { to: '/summary',         icon: MdBarChart,       label: 'Summary' },
  { to: '/recommendations', icon: MdRecommend,      label: 'Recommendations' },
]

export default function Sidebar({ collapsed, onToggle }) {
  const { logout } = useAuth()
  const navigate   = useNavigate()

  const handleLogout = async () => {
    await logout()
    toast.success('Logged out successfully')
    navigate('/login')
  }

  return (
    <aside
      className={`
        ${collapsed ? 'w-[68px]' : 'w-[240px]'}
        flex flex-col bg-white border-r border-gray-100 shadow-sm
        transition-all duration-300 ease-in-out flex-shrink-0 z-20
      `}
    >
      {/* Logo + Toggle */}
      <div className={`flex items-center h-16 px-4 border-b border-gray-100 ${collapsed ? 'justify-center' : 'justify-between'}`}>
        {!collapsed && (
          <div className="flex items-center gap-2">
            <span className="text-2xl">🥗</span>
            <span className="font-bold text-primary-700 text-sm leading-tight">
              Nutri<br />Nepal
            </span>
          </div>
        )}
        <button
          onClick={onToggle}
          className="p-1.5 rounded-lg text-gray-500 hover:bg-gray-100 transition-colors"
          aria-label="Toggle sidebar"
        >
          {collapsed ? <MdMenu size={20} /> : <MdMenuOpen size={20} />}
        </button>
      </div>

      {/* Navigation */}
      <nav className="flex-1 p-3 space-y-1 overflow-y-auto">
        {NAV_ITEMS.map(({ to, icon: Icon, label }) => (
          <NavLink
            key={to}
            to={to}
            className={({ isActive }) =>
              `sidebar-link ${isActive ? 'active' : ''} ${collapsed ? 'justify-center' : ''}`
            }
            title={collapsed ? label : undefined}
          >
            <Icon size={20} className="flex-shrink-0" />
            {!collapsed && <span className="text-sm truncate">{label}</span>}
          </NavLink>
        ))}
      </nav>

      {/* Logout */}
      <div className="p-3 border-t border-gray-100">
        <button
          onClick={handleLogout}
          className={`sidebar-link w-full text-red-500 hover:bg-red-50 hover:text-red-600 ${collapsed ? 'justify-center' : ''}`}
          title={collapsed ? 'Logout' : undefined}
        >
          <MdLogout size={20} className="flex-shrink-0" />
          {!collapsed && <span className="text-sm">Logout</span>}
        </button>
      </div>
    </aside>
  )
}
