import { createFileRoute } from '@tanstack/react-router'
import { useAuth } from '@/context/AuthContext'

export const Route = createFileRoute('/student/')({
  component: RouteComponent,
})

function RouteComponent() {
  const { user, loading } = useAuth()

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-center">
          <p className="text-lg font-semibold">Loading...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="p-6 space-y-4">
      <h1 className="text-2xl font-bold">Student Dashboard</h1>

      {user ? (
        <>
          <div className="border rounded-lg p-4 bg-card">
            <h2 className="text-lg font-semibold mb-4">User Information</h2>
            <div className="grid gap-3">
              <div>
                <span className="font-medium text-sm">ID:</span>
                <p className="text-sm text-muted-foreground">{user.id}</p>
              </div>
              <div>
                <span className="font-medium text-sm">Telegram ID:</span>
                <p className="text-sm text-muted-foreground">{user.telegram_id}</p>
              </div>
              <div>
                <span className="font-medium text-sm">First Name:</span>
                <p className="text-sm text-muted-foreground">{user.first_name}</p>
              </div>
              <div>
                <span className="font-medium text-sm">Last Name:</span>
                <p className="text-sm text-muted-foreground">{user.last_name || 'N/A'}</p>
              </div>
              <div>
                <span className="font-medium text-sm">Username:</span>
                <p className="text-sm text-muted-foreground">@{user.username || 'N/A'}</p>
              </div>
              <div>
                <span className="font-medium text-sm">Language:</span>
                <p className="text-sm text-muted-foreground">{user.language_code || 'N/A'}</p>
              </div>
              <div>
                <span className="font-medium text-sm">Photo URL:</span>
                <p className="text-sm text-muted-foreground">{user.photo_url || 'N/A'}</p>
              </div>
              <div>
                <span className="font-medium text-sm">Role:</span>
                <p className="text-sm text-muted-foreground font-semibold uppercase">{user.role}</p>
              </div>
            </div>
          </div>

          <div className="border rounded-lg p-4 bg-card">
            <h2 className="text-lg font-semibold mb-4">User Data (JSON)</h2>
            <pre className="text-xs bg-muted p-3 rounded overflow-auto max-h-60">
              {JSON.stringify(user, null, 2)}
            </pre>
          </div>
        </>
      ) : (
        <div className="border rounded-lg p-4 bg-card">
          <p className="text-muted-foreground">No user data available. Please log in.</p>
        </div>
      )}
    </div>
  )
}
