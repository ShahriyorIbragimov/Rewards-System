import { createFileRoute } from '@tanstack/react-router'
import UsersDataTable from '@/components/users-datatable'
import { Input } from '@/components/ui/input'
import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { useAuth } from '@/context/AuthContext'
import { useEffect, useState } from 'react'

export const Route = createFileRoute('/admin/users/')({
  component: RouteComponent,
})

type User = {
  id: string
  telegram_id: number
  first_name: string
  last_name?: string | null
  username?: string | null
  role: 'admin' | 'teacher' | 'student'
  photo_url?: string | null
}

function RouteComponent() {
  const { token } = useAuth()
  const [users, setUsers] = useState<User[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchUsers = async () => {
      setLoading(true)
      setError(null)
      try {
        const headers: Record<string, string> = { 'Content-Type': 'application/json' }
        if (token) headers.Authorization = `Bearer ${token}`

        const res = await fetch('/api/users/list-all', { headers })
        if (!res.ok) {
          const text = await res.text()
          throw new Error(`${res.status} ${res.statusText} - ${text}`)
        }

        const data = await res.json()
        setUsers(data || [])
      } catch (e) {
        setError(e instanceof Error ? e.message : String(e))
      } finally {
        setLoading(false)
      }
    }

    fetchUsers()
  }, [token])

  return (
    <>
      <div className='w-full flex flex-col gap-2 mb-4'>
        <div>
          <Input className='w-full'></Input>
        </div>
        <div className='w-full flex gap-2'>
          <Select>
            <SelectTrigger className='w-full'>
              <SelectValue placeholder="Select a role" />
            </SelectTrigger>
            <SelectContent>
              <SelectGroup>
                <SelectItem value="teacher">Teacher</SelectItem>
                <SelectItem value="student">Student</SelectItem>
              </SelectGroup>
            </SelectContent>
          </Select>
          <Select>
            <SelectTrigger className='w-full'>
              <SelectValue placeholder="Sort by" />
            </SelectTrigger>
            <SelectContent>
              <SelectGroup>
                {}
              </SelectGroup>
            </SelectContent>
          </Select>
        </div>
      </div>
      {loading && (
        <span>Loading...</span>
      )}

      {error && !loading && (
        <span className="text-red-600">
          {error}
        </span>
      )}

      {!loading && !error && users.length === 0 && (
        <span>No users found.</span>
      )}

      {!loading && !error && (
        <UsersDataTable users={users} />
      )}
    </>
  )
}
