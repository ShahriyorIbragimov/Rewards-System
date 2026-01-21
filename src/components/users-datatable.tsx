import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table"

type User = {
    id: string
    telegram_id: number
    first_name: string
    last_name?: string | null
    username?: string | null
    role: 'admin' | 'teacher' | 'student'
    photo_url?: string | null
}

interface DataTableProps {
    users: User[]
}

export default function UsersDataTable({ users }: DataTableProps) {
    return (
        <Table>
            <TableHeader>
                <TableRow>
                    <TableHead>ID</TableHead>
                    <TableHead>Telegram ID</TableHead>
                    <TableHead>Name</TableHead>
                    <TableHead>Username</TableHead>
                    <TableHead>Role</TableHead>
                </TableRow>
            </TableHeader>
            <TableBody>
                {users.map((u) => (
                    <TableRow key={u.id}>
                        <TableCell className="font-medium">{u.id}</TableCell>
                        <TableCell>{u.telegram_id}</TableCell>
                        <TableCell>{`${u.first_name || ''} ${u.last_name || ''}`.trim()}</TableCell>
                        <TableCell>{u.username || '-'}</TableCell>
                        <TableCell>{u.role}</TableCell>
                    </TableRow>
                ))}
            </TableBody>
        </Table>
    )
}