import { createFileRoute } from '@tanstack/react-router'
import { useNavigate } from '@tanstack/react-router'
import { useEffect, useState } from 'react'
import { useAuth } from '@/context/AuthContext'

export const Route = createFileRoute('/')({
  component: RouteComponent,
})

type TelegramUser = {
  id: number
  first_name: string
  last_name?: string
  username?: string
  language_code?: string
  photo_url?: string
}

function RouteComponent() {
  const navigate = useNavigate()
  const { user, token } = useAuth()
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const initializeApp = async () => {
      try {
        // @ts-ignore
        if (!window.Telegram?.WebApp) {
          setError('Please open this app through the Telegram bot')
          return
        }

        // @ts-ignore
        const webApp = window.Telegram.WebApp
        webApp.ready()
        const telegramUser = webApp.initDataUnsafe?.user as TelegramUser | undefined

        if (!telegramUser?.id) {
          setError('Could not retrieve your Telegram information')
          return
        }

        if (user && token) {
          const roleRoutes = {
            admin: '/admin',
            teacher: '/teacher',
            student: '/student',
          }
          navigate({ to: roleRoutes[user.role] || '/student' })
          return
        }

        // Login with Telegram data
        const loginResponse = await fetch('http://localhost:8000/api/auth/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            telegram_id: telegramUser.id,
            first_name: telegramUser.first_name,
            last_name: telegramUser.last_name || '',
            username: telegramUser.username || '',
            language_code: telegramUser.language_code || 'en',
            photo_url: telegramUser.photo_url || '',
            role: 'student',
          }),
        })

        if (!loginResponse.ok) {
          throw new Error('Login failed')
        }

        const { access_token } = await loginResponse.json()
        localStorage.setItem('authToken', access_token)

        // Get user data
        const meResponse = await fetch('http://localhost:8000/api/auth/me', {
          headers: { Authorization: `Bearer ${access_token}` },
        })

        if (!meResponse.ok) {
          throw new Error('Failed to fetch user data')
        }

        const userData = await meResponse.json()
        localStorage.setItem('user', JSON.stringify(userData))

        // Redirect based on role
        const roleRoutes = {
          admin: '/admin',
          teacher: '/teacher',
          student: '/student',
        }
        const userRole = (userData.role || 'student') as keyof typeof roleRoutes
        navigate({ to: roleRoutes[userRole] })
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An error occurred')
      } finally {
        setLoading(false)
      }
    }

    initializeApp()
  }, [navigate, user, token])

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-center">
          <p className="text-lg font-semibold">Loading...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-center">
          <p className="text-red-600 font-semibold">Error</p>
          <p className="text-red-500 mt-2">{error}</p>
        </div>
      </div>
    )
  }

  return null
}

