import { createRootRoute, Outlet } from '@tanstack/react-router'
import { AppSidebar } from "@/components/app-sidebar"
import {
  SidebarInset,
  SidebarProvider
} from "@/components/ui/sidebar"
import { Header } from '@/components/header'
import Navigation from '@/components/navigation'
import { Bell, Home, Store, Users } from "lucide-react"

const navItems = {
  navMain: [
    {
      title: "Home",
      icon: Home,
      url: "/main"
    },
    {
      title: "Groups",
      icon: Users,
      url: "/groups"
    },
    {
      title: "Marketplace",
      icon: Store,
      url: "/marketplace"
    },
    {
      title: "",
      icon: Bell,
      url: "/notifications"
    },
  ],
}

const RootLayout = () => (
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
      <Navigation navItems={navItems} />
    </SidebarInset>
  </SidebarProvider>
)

export const Route = createRootRoute({ component: RootLayout })