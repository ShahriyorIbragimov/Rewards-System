import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Button } from "@/components/ui/button"
import { Pen } from "lucide-react"

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

interface DataTableProps {
    users: User[]
}

function formatDate(iso: string) {
    try {
        const d = new Date(iso)
        return d.toLocaleString()
    } catch {
        return iso || '-'
    }
}

function getInitials(firstName: string, lastName: string | null): string {
    const first = (firstName ?? '').trim().charAt(0).toUpperCase()
    const last = (lastName ?? '').trim().charAt(0).toUpperCase()
    if (first && last) return `${first}${last}`
    if (first) return first
    return '?'
}

function openUserLink(url: string) {
    if (typeof window !== 'undefined' && window.Telegram?.WebApp?.openLink) {
        window.Telegram.WebApp.openLink(url)
    } else {
        window.open(url, '_blank', 'noopener,noreferrer')
    }
}

export default function UsersDataTable({ users }: DataTableProps) {
    return (
        <div className="w-full overflow-x-scroll overflow-y-visible pb-2 [scrollbar-gutter:stable] [&::-webkit-scrollbar]:h-2 [&::-webkit-scrollbar-track]:bg-muted/30 [&::-webkit-scrollbar-thumb]:rounded-full [&::-webkit-scrollbar-thumb]:bg-muted-foreground/30">
            <Table>
                <TableHeader>
                    <TableRow>
                        <TableHead>Photo</TableHead>
                        <TableHead>ID</TableHead>
                        <TableHead>Telegram ID</TableHead>
                        <TableHead>First name</TableHead>
                        <TableHead>Last name</TableHead>
                        <TableHead>Username</TableHead>
                        <TableHead>Language</TableHead>
                        <TableHead>Allows PM</TableHead>
                        <TableHead>Role</TableHead>
                        <TableHead>Created at</TableHead>
                        <TableHead>Updated at</TableHead>
                        <TableHead></TableHead>
                    </TableRow>
                </TableHeader>
                <TableBody>
                    {users.map((u) => (
                        <TableRow key={u.id}>
                            <TableCell>
                                <button
                                    type="button"
                                    onClick={() => u.username && openUserLink(`https://t.me/${u.username}`)}
                                    disabled={!u.username}
                                    className="rounded-full focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
                                    title={u.username ? `Open @${u.username}` : 'No username'}
                                >
                                    <Avatar className="size-8 cursor-pointer">
                                        {u.photo_url ? (
                                            <AvatarImage src={u.photo_url} alt="" />
                                        ) : null}
                                        <AvatarFallback className="text-xs font-medium">
                                            {getInitials(u.first_name, u.last_name)}
                                        </AvatarFallback>
                                    </Avatar>
                                </button>
                            </TableCell>
                            <TableCell className="font-medium font-mono text-xs" title={u.id}>{u.id}</TableCell>
                            <TableCell>{u.telegram_id}</TableCell>
                            <TableCell>{u.first_name ?? '-'}</TableCell>
                            <TableCell>{u.last_name ?? '-'}</TableCell>
                            <TableCell>{u.username || '-'}</TableCell>
                            <TableCell>{u.language_code ?? '-'}</TableCell>
                            <TableCell>{u.allows_write_to_pm ? 'Yes' : 'No'}</TableCell>
                            <TableCell>{u.role}</TableCell>
                            <TableCell className="whitespace-nowrap text-muted-foreground text-xs">{formatDate(u.created_at)}</TableCell>
                            <TableCell className="whitespace-nowrap text-muted-foreground text-xs">{formatDate(u.updated_at)}</TableCell>
                            <TableCell className="flex justify-end items-center">
                                <Button variant="ghost" size="icon" className="size-8">
                                    <Pen className="size-4" />
                                </Button>
                            </TableCell>
                        </TableRow>
                    ))}
                </TableBody>
            </Table>
        </div>
    )
}