import { createFileRoute } from '@tanstack/react-router'
import { useEffect, useState } from 'react';

export const Route = createFileRoute('/admin/')({
  component: RouteComponent,
})

type TelegramUser = {
  id: number,
  is_bot?: boolean,
  first_name: string,
  last_name?: string,
  username?: string,
  language_code?: string,
  photo_url?: string,
  is_premium?: boolean
}

function RouteComponent() {
  const [telegramUser, setTelegramUser] = useState<TelegramUser | null>(null)

  useEffect(() => {
    // @ts-ignore
    if (window.Telegram?.WebApp) {
      // @ts-ignore
      const webApp = window.Telegram.WebAppInitData;
      webApp.ready();
      setTelegramUser(webApp.user || null);
    }
  }, []);

  return (
    <div className="p-6 space-y-4">
      <h1 className="text-2xl font-bold">Admin Dashboard</h1>

      {telegramUser ? (
        <div className="border rounded-lg p-4 bg-card">
          <h2 className="text-lg font-semibold mb-4">Telegram User Information</h2>
          <div className="grid gap-3">
            <div>
              <span className="font-medium text-sm">ID:</span>
              <p className="text-sm text-muted-foreground">{telegramUser.id}</p>
            </div>
            <div>
              <span className="font-medium text-sm">First Name:</span>
              <p className="text-sm text-muted-foreground">{telegramUser.first_name}</p>
            </div>
            <div>
              <span className="font-medium text-sm">Last Name:</span>
              <p className="text-sm text-muted-foreground">{telegramUser.last_name || 'N/A'}</p>
            </div>
            <div>
              <span className="font-medium text-sm">Username:</span>
              <p className="text-sm text-muted-foreground">@{telegramUser.username || 'N/A'}</p>
            </div>
            <div>
              <span className="font-medium text-sm">Language:</span>
              <p className="text-sm text-muted-foreground">{telegramUser.language_code || 'N/A'}</p>
            </div>
          </div>
        </div>
      ) : (
        <div className="border rounded-lg p-4 bg-card">
          <p className="text-muted-foreground">Loading user information...</p>
        </div>
      )}
    </div>
  )
}
