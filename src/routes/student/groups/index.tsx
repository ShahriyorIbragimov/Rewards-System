import { createFileRoute } from '@tanstack/react-router'
import { Card, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { useState, useEffect } from 'react'
import { useAuth } from '@/context/AuthContext'
import { motion } from "framer-motion"
import { Badge } from "@/components/ui/badge"
import { Input } from "@/components/ui/input"
import { Separator } from "@/components/ui/separator"
import { Users, Search, BookOpen } from "lucide-react"

export const Route = createFileRoute('/student/groups/')({
    component: RouteComponent,
})

function RouteComponent() {
    type group = {
        id: string,
        title: string,
        description: string,
        is_active: boolean
    }

    const [groups, setGroups] = useState<group[]>([])
    const { token } = useAuth();

    useEffect(
        () => {
            async function get() {
                const meResponse = await fetch('/api/groups/list-user', {
                    headers: { Authorization: `Bearer ${token}` },
                })

                if (!meResponse.ok) {
                    const errorData = await meResponse.json().catch(() => ({}))
                    throw new Error(errorData.detail || 'Failed to fetch user data')
                }

                const responseData = await meResponse.json()
                setGroups(responseData)
            }

            get()
        },
        []
    )

    return (
        <div className="min-h-screen bg-background">
            <motion.div
                initial={{ opacity: 0, y: 12 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3 }}
                className="max-w mx-auto space-y-3"
            >
                <Card className="rounded-2xl shadow-sm">
                    <CardContent className="p-4 space-y-3">
                        <div className="flex items-center gap-2">
                            <Users className="h-5 w-5 text-primary" />
                            <p className="font-semibold text-lg">My Groups</p>
                        </div>
                        <div className="relative">
                            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                            <Input
                                placeholder="Search groups..."
                                className="pl-9 rounded-xl"
                            />
                        </div>
                    </CardContent>
                </Card>

                <div className="space-y-3">
                    {groups.length !== 0 && groups.map((group) => (
                        <motion.div
                            key={group.id}
                            whileHover={{ scale: 1.01 }}
                            whileTap={{ scale: 0.98 }}
                        >
                            <Card className="rounded-2xl shadow-sm">
                                <CardContent className="p-4 space-y-2">
                                    <div className="flex items-start justify-between gap-2">
                                        <div className="space-y-1">
                                            <div className="flex items-center gap-2">
                                                <BookOpen className="h-4 w-4 text-muted-foreground" />
                                                <p className="font-medium leading-none">{group.title}</p>
                                            </div>
                                            <p className="text-sm text-muted-foreground line-clamp-2">
                                                {group.description}
                                            </p>
                                        </div>
                                        <div className="flex flex-col items-end gap-1">
                                            <Badge variant="default">
                                                Active
                                            </Badge>
                                        </div>
                                    </div>
                                    <Separator />
                                    <div className="flex items-center justify-between text-sm">
                                        <Button
                                            size="sm"
                                            variant="secondary"
                                            className="rounded-xl"
                                        >
                                            Open
                                        </Button>
                                    </div>
                                </CardContent>
                            </Card>
                        </motion.div>
                    ))}
                </div>
            </motion.div>
        </div>
    )
}