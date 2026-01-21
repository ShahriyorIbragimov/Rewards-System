import { createFileRoute, Outlet } from '@tanstack/react-router'
import { AppSidebar } from "@/components/app-sidebar"
import {
  SidebarInset,
  SidebarProvider
} from "@/components/ui/sidebar"
import { Header } from '@/components/admin-header'
import {
  ShoppingBag,
  Home,
  Glasses,
  Users,
  GraduationCap,
  Sprout,
  HandCoins,
  Wallet,
  ClockArrowDown,
  BellRing
} from "lucide-react"

export const Route = createFileRoute('/admin')({
  component: Layout,
})

const navItems = {
  navMain: [
    {
      title: "Home",
      icon: Home,
      url: "/admin/main"
    },
    {
      title: "Users",
      icon: Users,
      url: "/admin/users"
    },
    {
      title: "Groups",
      icon: Sprout,
      url: "/admin/groups"
    },
    {
      title: "Teachers",
      icon: Glasses,
      url: "/admin/teachers"
    },
    {
      title: "Students",
      icon: GraduationCap,
      url: "/admin/students"
    },
    {
      title: "Products",
      icon: ShoppingBag,
      url: "/admin/products"
    },
    {
      title: "Rewards",
      icon: HandCoins,
      url: "/admin/rewards"
    },
    {
      title: "Transactions",
      icon: Wallet,
      url: "/admin/transactions"
    },
    {
      title: "Orders",
      icon: ClockArrowDown,
      url: "/admin/orders"
    },
    {
      title: "Notifications",
      icon: BellRing,
      url: "/admin/notifications"
    }
  ],
}

function Layout() {
  return (
    <SidebarProvider
      style={
        {
          "--sidebar-width": "19rem",
        } as React.CSSProperties
      }
    >
      <AppSidebar navItems={navItems} />
      <SidebarInset>
        <Header />
        <div className='p-4 pl-2'>
          <Outlet />
        </div>
      </SidebarInset>
    </SidebarProvider>
  )
}
