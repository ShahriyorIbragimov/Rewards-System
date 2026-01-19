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
  const [error, setError] = useState<string | null>(null)
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
    console.log('🚀 Initializing Telegram Mini App...');
    console.log('Current URL:', window.location.href);
    
    // @ts-ignore
    if (!window.Telegram) {
      const script = document.createElement('script');
      script.src = 'https://telegram.org/js/telegram-web-app.js';
      script.onload = () => {
        console.log('✅ Telegram WebApp script loaded');
        initializeTelegramApp();
      };
      script.onerror = () => {
        console.error('❌ Failed to load Telegram WebApp script');
        setError('Failed to load Telegram WebApp');
      };
      document.head.appendChild(script);
    } else {
      initializeTelegramApp();
    }

    function initializeTelegramApp() {
      try {
        // @ts-ignore
        if (window.Telegram?.WebApp) {
          console.log('✅ Telegram.WebApp found');
          // @ts-ignore
          const webApp = window.Telegram.WebApp;

          // Call ready to inform Telegram we're ready
          webApp.ready();
          console.log('Called webApp.ready()');

          // Get user data from initDataUnsafe
          const user = webApp.initDataUnsafe?.user;
          
          console.log('User from initDataUnsafe:', user);
          console.log('Full initDataUnsafe:', webApp.initDataUnsafe);

          if (user && user.id) {
            console.log('✅ User data found:', user);
            setTelegramUser(user);
          } else {
            console.warn('⚠️ No user data found in initDataUnsafe');
            setError('No user data received from Telegram. Make sure you opened this app via the inline button.');
          }
        } else {
          console.error('❌ Telegram.WebApp not found');
          // @ts-ignore
          console.log('window.Telegram:', window.Telegram);
          setError('Telegram WebApp SDK not available. Please open this app through the Telegram bot.');
        }
      } catch (err) {
        console.error('Error initializing Telegram app:', err);
        setError(`Initialization error: ${String(err)}`);
      }
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
          {showDebug ? 'Hide' : 'Show'} Debug
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

      {error && (
        <div className="border border-red-500 rounded-lg p-4 bg-red-50">
          <p className="text-red-700 text-sm font-semibold">⚠️ Error</p>
          <p className="text-red-600 text-sm mt-2">{error}</p>
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
