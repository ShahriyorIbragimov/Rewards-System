import { createRootRoute, Outlet } from '@tanstack/react-router'
import { AppSidebar } from "@/components/app-sidebar"
import {
  SidebarInset,
  SidebarProvider
} from "@/components/ui/sidebar"
import { Header } from '@/components/header'
import Navigation from '@/components/navigation'
import { ShoppingBag, Home, Store, Users, User } from "lucide-react"
import { ThemeProvider } from "@/components/theme-provider"

const navItems = {
  navMain: [
    {
      title: "Home",
      icon: Home,
      url: "/main"
    },
    {
      title: "Marketplace",
      icon: Store,
      url: "/marketplace"
    },
    {
      title: "Items",
      icon: ShoppingBag,
      url: "/items"
    },
    {
      title: "Groups",
      icon: Users,
      url: "/groups"
    },
    {
      title: "Profile",
      icon: User,
      url: "/profile"
    }
  ],
}

const RootLayout = () => (
  <ThemeProvider>
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
  </ThemeProvider>
)

export const Route = createRootRoute({ component: RootLayout })