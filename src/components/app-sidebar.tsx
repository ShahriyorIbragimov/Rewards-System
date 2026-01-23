import * as React from "react"
import { Coins } from "lucide-react"
import { Link } from "@tanstack/react-router"

import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/components/ui/sidebar"

type NavItem = {
  title: string
  icon: React.ComponentType<any>
  url: string
}

type NavItems = {
  main_url: string,
  navMain: NavItem[]
}

export function AppSidebar({ navItems, ...props }: { navItems?: NavItems } & React.ComponentProps<typeof Sidebar>) {
  const navList = navItems?.navMain ?? []

  return (
    <Sidebar variant="floating" {...props}>
      <SidebarHeader>
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton size="lg" asChild>
              <Link to={navItems?.main_url}>
                <div className="bg-sidebar-primary text-sidebar-primary-foreground flex aspect-square size-8 items-center justify-center rounded-lg">
                  <Coins className="size-4" />
                </div>
                <div className="flex flex-col gap-0.5 leading-none">
                  <span className="font-medium">EduCoins</span>
                </div>
              </Link>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarHeader>
      <SidebarContent>
        <SidebarGroup>
          <SidebarMenu className="gap-2">
            {navList.map((item) => (
              <SidebarMenuItem key={item.title} className="flex gap-2">
                <SidebarMenuButton asChild>
                  <Link to={item.url} className="font-medium">
                    <item.icon />
                    {item.title}
                  </Link>
                </SidebarMenuButton>
              </SidebarMenuItem>
            ))}
          </SidebarMenu>
        </SidebarGroup>
      </SidebarContent>
    </Sidebar>
  )
}
