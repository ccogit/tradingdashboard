import { Routes, Route, Navigate } from 'react-router-dom'
import { SignedIn, SignedOut, RedirectToSignIn } from '@clerk/clerk-react'
import { AppShell } from './layouts/AppShell'
import { SignInPage } from './pages/SignInPage'
import { SignUpPage } from './pages/SignUpPage'
import { DashboardPage } from './pages/DashboardPage'
import { PositionsPage } from './pages/PositionsPage'
import { TradePage } from './pages/TradePage'
import { OrdersPage } from './pages/OrdersPage'
import { HistoryPage } from './pages/HistoryPage'
import { CopilotPage } from './pages/CopilotPage'
import { SettingsPage } from './pages/SettingsPage'

export default function App() {
  return (
    <Routes>
      <Route path="/sign-in" element={<SignInPage />} />
      <Route path="/sign-up" element={<SignUpPage />} />
      <Route
        path="/"
        element={
          <>
            <SignedIn>
              <AppShell />
            </SignedIn>
            <SignedOut>
              <RedirectToSignIn />
            </SignedOut>
          </>
        }
      >
        <Route index element={<Navigate to="/dashboard" replace />} />
        <Route path="dashboard" element={<DashboardPage />} />
        <Route path="positions" element={<PositionsPage />} />
        <Route path="trade" element={<TradePage />} />
        <Route path="orders" element={<OrdersPage />} />
        <Route path="history" element={<HistoryPage />} />
        <Route path="copilot" element={<CopilotPage />} />
        <Route path="settings" element={<SettingsPage />} />
      </Route>
    </Routes>
  )
}
