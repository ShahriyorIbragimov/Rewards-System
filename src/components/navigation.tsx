import { Link } from "@tanstack/react-router";
import { useSidebar } from "./ui/sidebar";

type NavItem = {
  title: string
  icon: React.ComponentType<any>
  url: string
}

type NavItems = {
  navMain: NavItem[]
}

export default function Navigation({ navItems }: { navItems?: NavItems }) {
    const { isMobile } = useSidebar()

    if (!isMobile) {
        return null
    }

    const navList = navItems?.navMain ?? []

    return (
        <nav className="fixed bottom-0 left-0 right-0 bg-background border-t flex justify-around h-12">
            {navList.map((item) => (
              <BottomNavItem key={item.title} to={item.url} icon={<item.icon />} />
            ))}
        </nav>
    )
}

const BottomNavItem = ({ to, icon }: { to: string; icon: React.ReactNode }) => (
  <Link
    to={to}
    className="flex flex-col items-center justify-center text-muted-foreground"
  >
    {icon}
  </Link>
)