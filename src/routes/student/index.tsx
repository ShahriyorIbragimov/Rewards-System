import { createFileRoute } from '@tanstack/react-router'
import { useAuth } from '@/context/AuthContext'
import { motion } from "framer-motion"
import { Card, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Separator } from "@/components/ui/separator"
import { Coins, Trophy, Users, Gift, Bell, BellOff, ArrowRight, Sparkles, User } from "lucide-react"
import { useState } from 'react'

export const Route = createFileRoute('/student/')({
  component: RouteComponent,
})

function RouteComponent() {
  const { loading, user, studentProfile } = useAuth()
  const [notify, setNotify] = useState<boolean>(true)

  const recentRewards = [
    { id: "r1", title: "Perfect Attendance", coins: 100, group: "Math Olympiad" },
    { id: "r2", title: "Quiz Champion", coins: 50, group: "Physics Lab" },
  ]

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-center">
          <p className="text-lg font-semibold">Loading...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-background">
      <motion.div
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3 }}
        className="max-w mx-auto space-y-3"
      >
        <Card className="rounded-2xl shadow-sm">
          <CardContent className="p-4 flex items-center gap-3">
            <Avatar className="h-12 w-12">
              <AvatarImage src={studentProfile?.avatar_url} />
              <AvatarFallback>
                <User className="h-5 w-5" />
              </AvatarFallback>
            </Avatar>
            <div className="flex-1">
              <p className="text-sm text-muted-foreground">Welcome back,</p>
              <p className="font-semibold text-lg leading-none">{user?.first_name} 👋</p>
            </div>
            <Button
              size="icon"
              variant="ghost"
              className="rounded-full"
              onClick={() => setNotify(!notify)}
            >
              {notify
                ? <Bell className="h-5 w-5" />
                : <BellOff className="h-5 w-5" />
              }
            </Button>
          </CardContent>
        </Card>

        <Card className="rounded-2xl shadow-sm bg-primary/5">
          <CardContent className="p-4 space-y-2">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Coins className="h-5 w-5 text-primary" />
                <p className="font-medium">Your Coin Balance</p>
              </div>
              <Badge className="gap-1">
                <Sparkles className="h-3 w-3" />
                Rewards
              </Badge>
            </div>
            <p className="text-3xl font-bold">{studentProfile?.coin_balance}</p>
            <p className="text-sm text-muted-foreground">
              Total earned: {studentProfile?.total_coins_earned}
            </p>
          </CardContent>
        </Card>

        {/* Quick Stats */}
        <div className="grid grid-cols-2 gap-3">
          <Card className="rounded-2xl shadow-sm">
            <CardContent className="p-4 space-y-1">
              <div className="flex items-center gap-2">
                <Users className="h-4 w-4 text-muted-foreground" />
                <p className="text-sm">Groups</p>
              </div>
              <p className="text-xl font-semibold">0</p>
            </CardContent>
          </Card>
          <Card className="rounded-2xl shadow-sm">
            <CardContent className="p-4 space-y-1">
              <div className="flex items-center gap-2">
                <Trophy className="h-4 w-4 text-muted-foreground" />
                <p className="text-sm">Achievements</p>
              </div>
              <p className="text-xl font-semibold">{recentRewards.length}</p>
            </CardContent>
          </Card>
        </div>

        {/* Quick Actions */}
        <Card className="rounded-2xl shadow-sm">
          <CardContent className="p-4 space-y-3">
            <p className="font-medium">Quick Actions</p>
            <div className="grid grid-cols-2 gap-3">
              <Button variant="secondary" className="rounded-xl gap-2">
                <Gift className="h-4 w-4" />
                Rewards
              </Button>
              <Button variant="secondary" className="rounded-xl gap-2">
                <Users className="h-4 w-4" />
                Groups
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Recent Rewards */}
        <Card className="rounded-2xl shadow-sm">
          <CardContent className="p-4 space-y-3">
            <div className="flex items-center justify-between">
              <p className="font-medium">Recent Rewards</p>
              <Button size="sm" variant="ghost" className="gap-1">
                See all <ArrowRight className="h-3 w-3" />
              </Button>
            </div>
            <Separator />
            <div className="space-y-3">
              {recentRewards.map((r) => (
                <div key={r.id} className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium leading-none">{r.title}</p>
                    <p className="text-xs text-muted-foreground">{r.group}</p>
                  </div>
                  <div className="flex items-center gap-1 font-semibold">
                    +{r.coins}
                    <Coins className="h-4 w-4 text-primary" />
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </motion.div>
    </div>
  )
}
