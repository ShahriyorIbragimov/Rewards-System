import { createFileRoute } from '@tanstack/react-router'
import { Card, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { useState, useEffect } from 'react'

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

    useEffect(
        () => {
            async function get() {
                const response = await fetch("/api/auth/groups/list-active")
                const data = await response.json()
                setGroups(data)
            }

            get()
        },
        []
    )

    return (
        <div className="space-y-4">
            <div>
                <h1 className="text-xl font-semibold">My Groups</h1>
                <p className="text-sm text-muted-foreground">
                    Classes you are currently enrolled in
                </p>
            </div>

            <div className="grid gap-4 md:grid-cols-2">
                {groups.map((item, index) => (
                    <GroupCard key={index}
                        title={item.title}
                        description={item.description.length === 0 ? "No description" : item.description}
                        teacher="Shahriyor"
                        isActive={item.is_active}
                    />
                ))}
            </div>
        </div>
    )
}

const GroupCard = ({
    title,
    description,
    teacher,
    isActive,
}: {
    title: string
    description?: string
    teacher: string
    isActive: boolean
}) => (
    <Card className="hover:shadow-md transition">
        <CardContent className="p-4 space-y-3">
            <div className="flex items-start justify-between">
                <div>
                    <h2 className="font-semibold text-lg">{title}</h2>
                    {description && (
                        <p className="text-sm text-muted-foreground line-clamp-2">
                            {description}
                        </p>
                    )}
                </div>
                <span
                    className={`text-xs px-2 py-1 rounded-full ${isActive
                        ? "bg-green-100 text-green-700"
                        : "bg-gray-100 text-gray-500"
                        }`}
                >
                    {isActive ? "Active" : "Inactive"}
                </span>
            </div>

            <div className="text-sm text-muted-foreground">
                Teacher: <span className="text-foreground">{teacher}</span>
            </div>

            <div className="flex gap-2">
                <Button size="sm" variant="secondary" className="flex-1">
                    View Group
                </Button>
                <Button size="sm" variant="outline" className="flex-1">
                    Rewards
                </Button>
            </div>
        </CardContent>
    </Card>
)
