import { createFileRoute, Outlet } from '@tanstack/react-router'
import { AppSidebar } from "@/components/app-sidebar"
import {
    SidebarInset,
    SidebarProvider
} from "@/components/ui/sidebar"
import { Header } from '@/components/student-header'
import Navigation from '@/components/navigation'
import { ShoppingBag, Home, Store, Users, User } from "lucide-react"

export const Route = createFileRoute('/student')({
    component: Layout,
})

const navItems = {
    main_url: "/student",
    navMain: [
        {
            title: "Home",
            icon: Home,
            url: "/student"
        },
        {
            title: "Marketplace",
            icon: Store,
            url: "/student/marketplace"
        },
        {
            title: "Items",
            icon: ShoppingBag,
            url: "/student/items"
        },
        {
            title: "Groups",
            icon: Users,
            url: "/student/groups"
        },
        {
            title: "Profile",
            icon: User,
            url: "/student/profile"
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
                <div className='p-4 pl-2 mb-12'>
                    <Outlet />
                </div>
                <Navigation navItems={navItems} />
            </SidebarInset>
        </SidebarProvider>
    )
}
