import ReactMarkdown from 'react-markdown'
import type { ChatMessage } from '../../types/copilot'

export function MessageBubble({ message }: { message: ChatMessage }) {
  const isUser = message.role === 'user'

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div className={`max-w-[80%] rounded-lg px-4 py-3 text-sm ${
        isUser
          ? 'bg-primary text-primary-foreground'
          : 'bg-secondary text-foreground'
      }`}>
        {isUser ? (
          <p>{message.content}</p>
        ) : (
          <ReactMarkdown className="prose prose-sm prose-invert max-w-none">
            {message.content || '...'}
          </ReactMarkdown>
        )}
      </div>
    </div>
  )
}
