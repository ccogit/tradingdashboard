import { CopilotChat } from '../components/copilot/CopilotChat'

export function CopilotPage() {
  return (
    <div className="p-6 h-full flex flex-col">
      <h1 className="text-2xl font-semibold mb-4">AI Copilot</h1>
      <div className="flex-1 min-h-0">
        <CopilotChat />
      </div>
    </div>
  )
}
