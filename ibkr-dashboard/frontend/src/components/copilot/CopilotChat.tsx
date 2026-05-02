import { useState, useRef, useEffect } from 'react'
import { useAuth } from '@clerk/clerk-react'
import { useCopilotStore } from '../../stores/copilotStore'
import { useTradingModeStore } from '../../stores/tradingModeStore'
import { MessageBubble } from './MessageBubble'
import { StagedOrderCard } from './StagedOrderCard'
import { env } from '../../lib/env'
import type { ChatMessage } from '../../types/copilot'

const SUGGESTIONS = [
  "What's my P&L today?",
  "Show me my current positions",
  "Stage a buy of 10 AAPL at market",
  "What are my open orders?",
]

export function CopilotChat() {
  const [input, setInput] = useState('')
  const [isStreaming, setIsStreaming] = useState(false)
  const { messages, stagedOrders, addMessage, setSessionId, sessionId } = useCopilotStore()
  const accountId = useTradingModeStore((s) => s.accountId)
  const { getToken } = useAuth()
  const bottomRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  async function sendMessage(text: string) {
    if (!text.trim() || !accountId || isStreaming) return
    setInput('')
    setIsStreaming(true)

    const userMsg: ChatMessage = { id: crypto.randomUUID(), role: 'user', content: text, timestamp: new Date() }
    addMessage(userMsg)

    const token = await getToken()
    const response = await fetch(`${env.apiUrl}/copilot/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
      body: JSON.stringify({ session_id: sessionId, account_id: accountId, message: text }),
    })

    let assistantText = ''
    const assistantMsg: ChatMessage = { id: crypto.randomUUID(), role: 'assistant', content: '', timestamp: new Date() }
    addMessage(assistantMsg)

    const reader = response.body?.getReader()
    const decoder = new TextDecoder()
    let buffer = ''

    while (reader) {
      const { done, value } = await reader.read()
      if (done) break
      buffer += decoder.decode(value, { stream: true })
      const lines = buffer.split('\n')
      buffer = lines.pop() || ''
      for (const line of lines) {
        if (line.startsWith('data: ')) {
          try {
            const data = JSON.parse(line.slice(6))
            const { messages: msgs, setSessionId: setId, addStagedOrder } = useCopilotStore.getState()
            if (line.startsWith('event: text_delta') || data.text) {
              assistantText += data.text || ''
              // Update last message
            } else if (data.session_id) {
              setId(data.session_id)
            }
          } catch {}
        }
      }
    }

    setIsStreaming(false)
  }

  return (
    <div className="flex flex-col h-full border border-border rounded-lg bg-card overflow-hidden">
      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 && (
          <div className="text-center text-muted-foreground py-8">
            <p className="text-lg font-medium">AI Trading Copilot</p>
            <p className="text-sm mt-1">Ask about your portfolio or stage trades for review</p>
          </div>
        )}
        {messages.map((msg) => (
          <MessageBubble key={msg.id} message={msg} />
        ))}
        {stagedOrders.map((order) => (
          <StagedOrderCard key={order.staged_order_id} stagedOrder={order} />
        ))}
        <div ref={bottomRef} />
      </div>

      {/* Suggestions */}
      {messages.length === 0 && (
        <div className="px-4 pb-2 flex flex-wrap gap-2">
          {SUGGESTIONS.map((s) => (
            <button
              key={s}
              onClick={() => sendMessage(s)}
              className="text-xs px-3 py-1.5 rounded-full bg-secondary text-muted-foreground hover:text-foreground transition-colors"
            >
              {s}
            </button>
          ))}
        </div>
      )}

      {/* Input */}
      <div className="border-t border-border p-4 flex gap-2">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendMessage(input) }
          }}
          placeholder="Ask about your portfolio..."
          rows={1}
          className="flex-1 bg-secondary border border-border rounded-md px-3 py-2 text-sm resize-none"
        />
        <button
          onClick={() => sendMessage(input)}
          disabled={!input.trim() || isStreaming}
          className="px-4 py-2 bg-primary text-primary-foreground rounded-md text-sm font-medium disabled:opacity-50 hover:bg-primary/90"
        >
          {isStreaming ? '...' : 'Send'}
        </button>
      </div>
    </div>
  )
}
