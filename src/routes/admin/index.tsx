import { createFileRoute } from '@tanstack/react-router'
import { useEffect, useState } from 'react';

export const Route = createFileRoute('/admin/')({
  component: RouteComponent,
})

type TelegramUser = {
  id: number,
  is_bot: string,
  first_name: string,
  last_name: string,
  username: string,
  language_code: string
}

function RouteComponent() {
  const [telegramUser, setTelegramUser] = useState<TelegramUser>()
  const [showDebug, setShowDebug] = useState(false)
  const [logs, setLogs] = useState<string[]>([])

  useEffect(() => {
    // Capture console logs
    const originalLog = console.log;
    console.log = (...args: any[]) => {
      originalLog(...args);
      setLogs(prev => [...prev, args.map(arg => 
        typeof arg === 'object' ? JSON.stringify(arg, null, 2) : String(arg)
      ).join(' ')]);
    };
    return () => {
      console.log = originalLog;
    };
  }, []);

  useEffect(() => {
    console.log('Checking for Telegram...');
    // @ts-ignore
    if (window.Telegram?.WebApp) {
      console.log('Telegram WebApp found');
      // @ts-ignore
      const tg = window.Telegram.WebApp;

      tg.ready();

      const user = tg.initDataUnsafe?.user;
      
      console.log('User data:', user);
      console.log('Full initDataUnsafe:', tg.initDataUnsafe);

      setTelegramUser(user);
    } else {
      // @ts-ignore
      console.log('Telegram WebApp not found. Window.Telegram:', window.Telegram);
      console.log('Make sure you are opening this app from a Telegram bot, not directly in a browser.');
    }
  }, []);

  return (
    <div className="p-6 space-y-4">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold">Admin Dashboard</h1>
        <button 
          onClick={() => setShowDebug(!showDebug)}
          className="px-3 py-1 text-sm bg-slate-600 text-white rounded hover:bg-slate-700"
        >
          {showDebug ? 'Hide' : 'Show'} Debug Console
        </button>
      </div>

      {showDebug && (
        <div className="bg-black text-green-400 p-4 rounded font-mono text-xs max-h-60 overflow-y-auto border border-green-400">
          <div className="space-y-1">
            {logs.length === 0 ? (
              <p>No logs yet...</p>
            ) : (
              logs.map((log, i) => <div key={i}>{log}</div>)
            )}
          </div>
        </div>
      )}
      
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
            <div>
              <span className="font-medium text-sm">Is Bot:</span>
              <p className="text-sm text-muted-foreground">{telegramUser.is_bot}</p>
            </div>
          </div>
        </div>
      ) : (
        <div className="border rounded-lg p-4 bg-card">
          <p className="text-muted-foreground">Loading Telegram user information...</p>
        </div>
      )}
    </div>
  )
}
