import { env } from './env'

type WSHandler = (event: unknown) => void

export class WSClient {
  private ws: WebSocket | null = null
  private handlers: Map<string, WSHandler[]> = new Map()
  private reconnectTimer: ReturnType<typeof setTimeout> | null = null
  private url: string

  constructor(path: string, token: string) {
    this.url = `${env.wsUrl}${path}?token=${encodeURIComponent(token)}`
  }

  connect() {
    this.ws = new WebSocket(this.url)
    this.ws.onmessage = (e) => {
      try {
        const msg = JSON.parse(e.data)
        const handlers = this.handlers.get(msg.type) || []
        handlers.forEach((h) => h(msg.payload ?? msg))
      } catch {}
    }
    this.ws.onclose = () => {
      this.reconnectTimer = setTimeout(() => this.connect(), 3000)
    }
  }

  on(type: string, handler: WSHandler) {
    if (!this.handlers.has(type)) this.handlers.set(type, [])
    this.handlers.get(type)!.push(handler)
  }

  send(data: unknown) {
    if (this.ws?.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(data))
    }
  }

  disconnect() {
    if (this.reconnectTimer) clearTimeout(this.reconnectTimer)
    this.ws?.close()
  }
}
