export function formatCurrency(value: number, currency = 'USD'): string {
  return new Intl.NumberFormat('en-US', { style: 'currency', currency, minimumFractionDigits: 2 }).format(value)
}

export function formatPercent(value: number): string {
  return new Intl.NumberFormat('en-US', { style: 'percent', minimumFractionDigits: 2, signDisplay: 'always' }).format(value / 100)
}

export function formatNumber(value: number, decimals = 2): string {
  return new Intl.NumberFormat('en-US', { minimumFractionDigits: decimals, maximumFractionDigits: decimals }).format(value)
}
