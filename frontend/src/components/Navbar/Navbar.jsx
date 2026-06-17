import { useAuth } from '../../context/AuthContext.jsx'
import { MdNotificationsNone } from 'react-icons/md'

export default function Navbar() {
  const { user } = useAuth()
  const hour = new Date().getHours()
  const greeting = hour < 12 ? 'Good morning' : hour < 18 ? 'Good afternoon' : 'Good evening'

  return (
    <header className="h-16 bg-white border-b border-gray-100 flex items-center justify-between px-6 flex-shrink-0">
      <div>
        <p className="text-xs text-gray-400">{greeting},</p>
        <p className="text-sm font-semibold text-gray-800">{user?.full_name || 'User'}</p>
      </div>
      <div className="flex items-center gap-3">
        <button className="relative p-2 rounded-lg text-gray-500 hover:bg-gray-100 transition-colors">
          <MdNotificationsNone size={20} />
        </button>
        <div className="w-8 h-8 rounded-full bg-primary-100 flex items-center justify-center">
          <span className="text-primary-700 font-semibold text-sm">
            {user?.full_name?.[0]?.toUpperCase() || 'U'}
          </span>
        </div>
      </div>
    </header>
  )
}
