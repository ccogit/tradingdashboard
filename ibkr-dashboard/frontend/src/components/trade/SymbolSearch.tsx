import { useState, useCallback } from 'react'
import { useAuthFetch } from '../../hooks/useAuthFetch'
import type { Contract } from '../../types/api'

interface Props {
  onSelect: (contract: Contract) => void
}

export function SymbolSearch({ onSelect }: Props) {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState<Contract[]>([])
  const [isOpen, setIsOpen] = useState(false)
  const fetch = useAuthFetch()
  let debounceTimer: ReturnType<typeof setTimeout>

  async function handleInput(value: string) {
    setQuery(value)
    clearTimeout(debounceTimer)
    if (value.length < 1) { setResults([]); setIsOpen(false); return }
    debounceTimer = setTimeout(async () => {
      const data = await fetch<Contract[]>(`/contracts/search?q=${encodeURIComponent(value)}`)
      setResults(data)
      setIsOpen(true)
    }, 300)
  }

  function select(c: Contract) {
    setQuery(c.symbol)
    setResults([])
    setIsOpen(false)
    onSelect(c)
  }

  return (
    <div className="relative">
      <input
        type="text"
        value={query}
        onChange={(e) => handleInput(e.target.value)}
        placeholder="Search symbol (e.g. AAPL)..."
        className="w-full bg-secondary border border-border rounded-md px-3 py-2 text-sm"
      />
      {isOpen && results.length > 0 && (
        <div className="absolute z-10 w-full mt-1 bg-card border border-border rounded-md shadow-lg max-h-48 overflow-y-auto">
          {results.map((c) => (
            <button
              key={c.conid}
              type="button"
              onClick={() => select(c)}
              className="w-full text-left px-3 py-2 text-sm hover:bg-secondary flex justify-between"
            >
              <span className="font-medium">{c.symbol}</span>
              <span className="text-muted-foreground">{c.description || c.sec_type}</span>
            </button>
          ))}
        </div>
      )}
    </div>
  )
}
