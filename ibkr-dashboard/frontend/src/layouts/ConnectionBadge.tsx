import { useConnectionStore } from '../stores/connectionStore'
import { useConnectionStatus } from '../hooks/useConnectionStatus'

export function ConnectionBadge() {
  useConnectionStatus()
  const ibState = useConnectionStore((s) => s.ibState)

  const config = {
    connected: { color: 'bg-green-500', label: 'IB Connected' },
    connecting: { color: 'bg-yellow-500 animate-pulse', label: 'Connecting...' },
    disconnected: { color: 'bg-red-500', label: 'IB Disconnected' },
    error: { color: 'bg-red-500', label: 'IB Error' },
  }[ibState]

  return (
    <div className="flex items-center gap-2 text-xs text-muted-foreground">
      <div className={`w-2 h-2 rounded-full ${config.color}`} />
      {config.label}
    </div>
  )
}
