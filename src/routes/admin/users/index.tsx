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
import { useIsMobile } from '@/hooks/use-mobile'
import { useEffect, useState, useMemo } from 'react'
import { Plus } from 'lucide-react'
import { Button } from "@/components/ui/button"
import {
  Dialog,
  DialogClose,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import { Field, FieldGroup } from "@/components/ui/field"
import { Label } from "@/components/ui/label"

export const Route = createFileRoute('/admin/users/')({
  component: RouteComponent,
})

type User = {
  id: string
  telegram_id: number
  first_name: string
  last_name: string | null
  username: string | null
  language_code: string
  allows_write_to_pm: boolean
  photo_url: string | null
  role: 'admin' | 'teacher' | 'student'
  created_at: string
  updated_at: string
}

function RouteComponent() {
  const { token } = useAuth()
  const [users, setUsers] = useState<User[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const isMobile = useIsMobile()

  const [formData, setFormData] = useState({
    telegram_id: "",
    first_name: "",
    last_name: "",
    username: "",
    language_code: "",
    allows_write_to_pm: "",
    photo_url: "",
    role: "student"
  })

  const [query, setQuery] = useState('')
  const [roleFilter, setRoleFilter] = useState<'all' | 'teacher' | 'student'>('all')
  const [searchKey, setSearchKey] = useState<'id' | 'telegram_id' | 'name' | 'username'>('name')

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

  const filteredUsers = useMemo(() => {
    const q = query.trim().toLowerCase()

    const matchesQuery = (u: User) => {
      if (!q) return true
      if (searchKey === 'name') {
        const fullName = `${u.first_name || ''} ${u.last_name || ''}`.trim().toLowerCase()
        return fullName.includes(q)
      }
      if (searchKey === 'username') {
        return (u.username || '').toLowerCase().includes(q)
      }
      if (searchKey === 'telegram_id') {
        return String(u.telegram_id ?? '').toLowerCase().includes(q)
      }
      return (u.id || '').toLowerCase().includes(q)
    }

    const matchesRole = (u: User) => {
      if (roleFilter === 'all') return true
      return u.role === roleFilter
    }

    const result = users.filter((u) => matchesRole(u) && matchesQuery(u))

    const sorted = [...result].sort((a, b) => {
      if (searchKey === 'telegram_id') return a.telegram_id - b.telegram_id
      if (searchKey === 'name') {
        const an = `${a.first_name || ''} ${a.last_name || ''}`.trim()
        const bn = `${b.first_name || ''} ${b.last_name || ''}`.trim()
        return an.localeCompare(bn)
      }
      if (searchKey === 'username') return (a.username || '').localeCompare(b.username || '')
      return (a.id || '').localeCompare(b.id || '')
    })

    return sorted
  }, [users, query, roleFilter, searchKey])

  const handleInputChange = (
    e: React.ChangeEvent<HTMLInputElement>
  ) => {
    const { id, value } = e.currentTarget
    setFormData((prev) => ({
      ...prev,
      [id]: value,
    }))
  }

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    setError("")

    if (formData.username.length < 4 && formData.username.length > 0) {
      setError("Username must be at least 5 characters long")
      return
    }

    setLoading(true)

    try {
      const loginResponse = await fetch("/api/users/create", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({
          telegram_id: formData.telegram_id,
          first_name: formData.first_name,
          last_name: formData.last_name,
          username: formData.username,
          language_code: formData.language_code,
          allows_write_to_pm: formData.allows_write_to_pm,
          photo_url: formData.photo_url,
          role: formData.role
        }),
      })

      if (!loginResponse.ok) {
        const errorData = await loginResponse.json().catch(() => ({}))
        throw new Error(errorData.detail || "Failed to login. Please sign in manually.")
      }


    } catch (err) {
      const message = err instanceof Error ? err.message : "An error occurred"
      setError(message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <>
      <div className='w-full flex flex-col gap-2 mb-4'>
        <div className="w-full">
          <Input
            className='w-full'
            placeholder={
              searchKey === 'name'
                ? 'Search by name...'
                : searchKey === 'username'
                  ? 'Search by username...'
                  : searchKey === 'telegram_id'
                    ? 'Search by telegram id...'
                    : 'Search by id...'
            }
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
        </div>
        <div className={!isMobile ? "w-full flex gap-2" : "w-full flex flex-col gap-2"}>
          <Select
            value={roleFilter}
            onValueChange={(v) => setRoleFilter(v as typeof roleFilter)}>
            <SelectTrigger className="w-full">
              <SelectValue placeholder="Select a role" />
            </SelectTrigger>
            <SelectContent>
              <SelectGroup>
                <SelectItem value="all">All</SelectItem>
                <SelectItem value="teacher">Teacher</SelectItem>
                <SelectItem value="student">Student</SelectItem>
              </SelectGroup>
            </SelectContent>
          </Select>
          <Select value={searchKey} onValueChange={(v) => setSearchKey(v as typeof searchKey)}>
            <SelectTrigger className="w-full">
              <SelectValue placeholder="Search/Sort by" />
            </SelectTrigger>
            <SelectContent>
              <SelectGroup>
                <SelectItem value="name">Name</SelectItem>
                <SelectItem value="username">Username</SelectItem>
                <SelectItem value="telegram_id">Telegram ID</SelectItem>
                <SelectItem value="id">ID</SelectItem>
              </SelectGroup>
            </SelectContent>
          </Select>
          <Dialog>
            <form onSubmit={handleSubmit}>
              <DialogTrigger className={isMobile ? "w-full" : ""}>
                <Button className='w-full'>
                  <Plus /> Create a new user
                </Button>
              </DialogTrigger>
              <DialogContent className="sm:max-w-sm">
                <DialogHeader>
                  <DialogTitle>Create user</DialogTitle>
                  <DialogDescription>
                    Create a new user here. Click create when you&apos;re
                    done.
                  </DialogDescription>
                </DialogHeader>
                <FieldGroup>
                  <Field>
                    <Label htmlFor="telegram_id">Telegram ID</Label>
                    <Input id="telegram_id" name="telegram_id" placeholder='optional' />
                  </Field>
                  <div className='flex gap-2'>
                    <Field>
                      <Label htmlFor="first_name">First Name</Label>
                      <Input id="first_name" name="first_name" placeholder='Pedro' />
                    </Field>
                    <Field>
                      <Label htmlFor="last_name">Last Name</Label>
                      <Input id="last_name" name="last_name" defaultValue="Duarte" />
                    </Field>
                  </div>
                  <Field>
                    <Label htmlFor="username">Username</Label>
                    <Input id="username" name="username" placeholder="@peduarte" />
                  </Field>
                  <div className='flex gap-2'>
                    <Field>
                      <Label htmlFor="language_code">Language</Label>
                      <Input id="language_code" name="language_code" />
                    </Field>
                    <Field>
                      <Label htmlFor="allows_write_to_pm">Allows PM</Label>
                      <Input id="allows_write_to_pm" name="allows_write_to_pm" />
                    </Field>
                  </div>
                  <div className='flex gap-2'>
                    <Field>
                      <Label htmlFor="photo_url">Photo URL</Label>
                      <Input id="photo_url" name="photo_url" />
                    </Field>
                    <Field>
                      <Label htmlFor="role">Role</Label>
                      <Input id="role" name="role" />
                    </Field>
                  </div>
                </FieldGroup>
                <DialogFooter>
                  <DialogClose>
                    <Button variant="outline">Cancel</Button>
                  </DialogClose>
                  <Button type="submit">Create</Button>
                </DialogFooter>
              </DialogContent>
            </form>
          </Dialog>
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
        <UsersDataTable users={filteredUsers} />
      )}
    </>
  )
}
