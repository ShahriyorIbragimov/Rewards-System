import { createFileRoute } from '@tanstack/react-router'
import { motion } from "framer-motion"
import { Card, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Separator } from "@/components/ui/separator"
import { Coins, Edit3, Trophy, ShoppingBag, User } from "lucide-react"
import { useAuth } from "@/context/AuthContext"

export const Route = createFileRoute('/student/profile/')({
    component: RouteComponent,
})

function RouteComponent() {
    const { user, studentProfile } = useAuth()

    return (
        <div className="min-h-screen bg-background p-1">
            <motion.div
                initial={{ opacity: 0, y: 12 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3 }}
                className="max-w mx-auto space-y-3"
            >
                <Card className="rounded-2xl shadow-sm">
                    <CardContent className="p-4 flex items-center gap-3">
                        <Avatar className="h-14 w-14">
                            <AvatarImage src={studentProfile?.avatar_url} />
                            <AvatarFallback>
                                <User className="h-6 w-6" />
                            </AvatarFallback>
                        </Avatar>
                        <div className="flex-1">
                            <div className="flex items-center justify-between">
                                <div>
                                    <p className="font-semibold leading-none">
                                        {user?.first_name} {user?.last_name}
                                    </p>
                                    <p className="text-sm text-muted-foreground">@{user?.username}</p>
                                </div>
                                <Badge variant={studentProfile?.is_active ? "default" : "secondary"}>
                                    {studentProfile?.is_active ? "Active" : "Inactive"}
                                </Badge>
                            </div>
                            <p className="text-sm mt-2 text-muted-foreground line-clamp-2">
                                {studentProfile?.bio}
                            </p>
                        </div>
                    </CardContent>
                </Card>

                <Card className="rounded-2xl shadow-sm">
                    <CardContent className="p-4 space-y-3">
                        <div className="flex items-center justify-between">
                            <div className="flex items-center gap-2">
                                <Coins className="h-5 w-5 text-primary" />
                                <p className="font-medium">Coin Balance</p>
                            </div>
                            <p className="text-xl font-bold">{studentProfile?.coin_balance}</p>
                        </div>
                        <Separator />
                        <div className="text-sm flex justify-between">
                            <div className="flex items-center gap-2">
                                <Trophy className="h-4 w-4 text-muted-foreground" />
                                <span>Earned: {studentProfile?.total_coins_earned}</span>
                            </div>
                            <div className="flex items-center gap-2">
                                <ShoppingBag className="h-4 w-4 text-muted-foreground" />
                                <span>Spent: {studentProfile?.total_coins_spent}</span>
                            </div>
                        </div>
                    </CardContent>
                </Card>

                <Card className="rounded-2xl shadow-sm">
                    <CardContent className="p-4 space-y-3">
                        <Button variant="secondary" className="w-full rounded-xl gap-2">
                            <Edit3 className="h-4 w-4" />
                            Edit Profile
                        </Button>
                        <Button variant="outline" className="w-full rounded-xl">
                            View Transactions
                        </Button>
                    </CardContent>
                </Card>
            </motion.div>
        </div>
    )
}