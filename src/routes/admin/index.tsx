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
    console.log('Window object keys:', Object.keys(window).filter(k => k.includes('Telegram') || k.includes('telegram')));
    // @ts-ignore
    console.log('Window.Telegram exists:', !!window.Telegram);
    // @ts-ignore
    console.log('Window.TelegramWebviewProxy exists:', !!window.TelegramWebviewProxy);
    
    const timer = setTimeout(() => {
      // @ts-ignore
      if (window.Telegram?.WebApp) {
        console.log('✅ Telegram WebApp found (iOS/Desktop)');
        // @ts-ignore
        const tg = window.Telegram.WebApp;

        tg.ready();

        const user = tg.initDataUnsafe?.user;
        
        console.log('User data:', user);
        console.log('Full initDataUnsafe:', tg.initDataUnsafe);

        setTelegramUser(user);
      } 
      // @ts-ignore
      else if (window.TelegramWebviewProxy) {
        console.log('✅ Telegram WebviewProxy found (Android)');
        // @ts-ignore
        const proxy = window.TelegramWebviewProxy;
        
        // On Android, we need to use postEvent to get data
        // @ts-ignore
        proxy.postEvent('web_app_ready', {});
        
        // Log all URL parameters
        const params = new URLSearchParams(window.location.hash.substring(1));
        console.log('All URL params:');
        params.forEach((value, key) => {
          console.log(`  ${key}: ${value}`);
        });
        
        // Try different ways to get user data on Android
        // Method 1: Check if data is passed via postEvent callback
        // @ts-ignore
        if (window.TelegramWebviewProxy.receiveEvent) {
          // @ts-ignore
          window.TelegramWebviewProxy.receiveEvent('web_app_data_received', (data: any) => {
            console.log('Received web_app_data:', data);
            if (data && data.user) {
              setTelegramUser(data.user);
            }
          });
        }
        
        // Method 2: Try to parse from URL query string (some Android versions use query instead of hash)
        const queryParams = new URLSearchParams(window.location.search);
        const urlInitData = queryParams.get('tgWebAppData') || params.get('tgWebAppData');
        console.log('Init data from URL:', urlInitData);
        
        if (urlInitData) {
          const decoded = decodeURIComponent(urlInitData);
          console.log('Decoded init data:', decoded);
          
          // Parse user data from initData
          const match = decoded.match(/user=({[^}]+})/);
          if (match) {
            try {
              const userData = JSON.parse(decodeURIComponent(match[1]));
              console.log('Extracted user data:', userData);
              setTelegramUser(userData);
            } catch (e) {
              console.error('Failed to parse user data:', e);
            }
          }
        }
        
        // For Android, also try accessing user data if available in window object
        // @ts-ignore
        if (window.TelegramUser) {
          // @ts-ignore
          console.log('TelegramUser found in window:', window.TelegramUser);
          // @ts-ignore
          setTelegramUser(window.TelegramUser);
        }
      } else {
        console.log('❌ Telegram WebApp NOT found');
        // @ts-ignore
        console.log('Window.Telegram:', window.Telegram);
        // @ts-ignore
        console.log('Window.TelegramWebviewProxy:', window.TelegramWebviewProxy);
        console.log('⚠️ ERROR: Telegram SDK not loaded.');
        console.log('Current URL:', window.location.href);
      }
    }, 1000);

    return () => clearTimeout(timer);
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
