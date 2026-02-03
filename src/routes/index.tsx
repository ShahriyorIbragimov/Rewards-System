import { createFileRoute } from '@tanstack/react-router'
import { useNavigate } from '@tanstack/react-router'
import { useEffect, useState } from 'react'
import { useAuth, type StudentProfile, type AdminProfile } from '@/context/AuthContext'

export const Route = createFileRoute('/')({
  component: RouteComponent,
})

type TelegramUser = {
  id: number
  first_name: string
  last_name?: string
  username?: string
  language_code?: string
  allows_write_to_pm?: boolean
  photo_url?: string
}

function RouteComponent() {
  const navigate = useNavigate()
  const { user, token, login } = useAuth()
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (user && token) {
      const roleRoutes = {
        admin: '/admin',
        teacher: '/teacher',
        student: '/student',
      }
      navigate({ to: roleRoutes[user.role] || '/student' })
    }
  }, [user, token])

  useEffect(() => {
    let isMounted = true

    const initializeApp = async () => {
      try {
        // @ts-ignore
        if (!window.Telegram?.WebApp) {
          if (isMounted) setError('Please open this app through the Telegram bot')
          return
        }

        // @ts-ignore
        const webApp = window.Telegram.WebApp
        webApp.ready()
        const telegramUser = webApp.initDataUnsafe?.user as TelegramUser | undefined

        if (!telegramUser?.id) {
          if (isMounted) setError('Could not retrieve your Telegram information')
          return
        }

        // If user is already logged in, navigate to their role page
        if (user && token) {
          const roleRoutes = {
            admin: '/admin',
            teacher: '/teacher',
            student: '/student',
          }
          navigate({ to: roleRoutes[user.role] || '/student' })
          return
        }

        const initDataString = webApp.initData
        
        const loginResponse = await fetch('/api/auth/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ init_data: initDataString }),
        })

        if (!loginResponse.ok) {
          const errorData = await loginResponse.json().catch(() => ({}))
          throw new Error(errorData.detail || 'Login failed')
        }

        const { access_token } = await loginResponse.json()

        const meResponse = await fetch('/api/auth/me', {
          headers: { Authorization: `Bearer ${access_token}` },
        })

        if (!meResponse.ok) {
          const errorData = await meResponse.json().catch(() => ({}))
          throw new Error(errorData.detail || 'Failed to fetch user data')
        }

        const responseData = await meResponse.json()
        let adminData: any = null;
        let studentData: any = null;

        if (responseData.role == "admin") {
          const profileResponse = await fetch('/api/admin/validate', {
            headers: { Authorization: `Bearer ${access_token}` },
          })
  
          if (!profileResponse.ok) {
            const errorData = await profileResponse.json().catch(() => ({}))
            throw new Error(errorData.detail || 'Failed to fetch profile data')
          }
  
          adminData = await profileResponse.json()
        }

        const adminProfile: AdminProfile | undefined = adminData ? {
          id: adminData.id as string,
          user_id: responseData.id as string,
          avatar_url: adminData.avatar_url as string,
          bio: adminData.bio as string,
          is_active: adminData.is_active as boolean,
        } : undefined

        if (responseData.role == "student") {
          const profileResponse = await fetch('/api/students/validate', {
            headers: { Authorization: `Bearer ${access_token}` },
          })
  
          if (!profileResponse.ok) {
            const errorData = await profileResponse.json().catch(() => ({}))
            throw new Error(errorData.detail || 'Failed to fetch profile data')
          }
  
          studentData = await profileResponse.json()
        }

        const studentProfile: StudentProfile | undefined = studentData ? {
          id: studentData.id as string,
          user_id: responseData.id as string,
          coin_balance: studentData.coin_balance as number,
          total_coins_earned: studentData.total_coins_earned as number,
          total_coins_spent: studentData.total_coins_spent as number,
          avatar_url: studentData.avatar_url as string,
          bio: studentData.bio as string,
          is_active: studentData.is_active as boolean,
        } : undefined

        if (isMounted) {
          login(access_token, responseData, adminProfile, studentProfile)

          const roleRoutes = {
            admin: '/admin',
            teacher: '/teacher',
            student: '/student',
          }
          const userRole = (responseData.role || 'student') as keyof typeof roleRoutes
          navigate({ to: roleRoutes[userRole] })
        }
      } catch (err) {
        if (isMounted) {
          setError(err instanceof Error ? err.message : 'An error occurred')
        }
      } finally {
        if (isMounted) {
          setLoading(false)
        }
      }
    }

    if (!user || !token) {
      initializeApp()
    } else {
      setLoading(false)
    }

    return () => {
      isMounted = false
    }
  }, [])

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

