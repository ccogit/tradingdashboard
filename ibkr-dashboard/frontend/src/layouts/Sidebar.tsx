import { NavLink } from 'react-router-dom'
import { LayoutDashboard, BarChart2, TrendingUp, ClipboardList, History, Bot, Settings } from 'lucide-react'
import { cn } from '../lib/utils'

const navItems = [
  { to: '/dashboard', icon: LayoutDashboard, label: 'Dashboard' },
  { to: '/positions', icon: BarChart2, label: 'Positions' },
  { to: '/trade', icon: TrendingUp, label: 'Trade' },
  { to: '/orders', icon: ClipboardList, label: 'Orders' },
  { to: '/history', icon: History, label: 'History' },
  { to: '/copilot', icon: Bot, label: 'Copilot' },
  { to: '/settings', icon: Settings, label: 'Settings' },
]

export function Sidebar() {
  return (
    <aside className="w-56 border-r border-border bg-card flex flex-col">
      <div className="p-4 border-b border-border">
        <span className="text-lg font-bold text-primary">IBKR Dashboard</span>
      </div>
      <nav className="flex-1 p-2 space-y-1">
        {navItems.map(({ to, icon: Icon, label }) => (
          <NavLink
            key={to}
            to={to}
            className={({ isActive }) =>
              cn(
                'flex items-center gap-3 px-3 py-2 rounded-md text-sm transition-colors',
                isActive
                  ? 'bg-primary/10 text-primary font-medium'
                  : 'text-muted-foreground hover:text-foreground hover:bg-secondary'
              )
            }
          >
            <Icon size={16} />
            {label}
          </NavLink>
        ))}
      </nav>
    </aside>
  )
}
