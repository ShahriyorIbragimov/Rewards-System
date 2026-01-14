import * as React from "react"

import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbList,
  BreadcrumbSeparator,
} from "@/components/ui/breadcrumb"
import { Separator } from "@/components/ui/separator"
import {
  SidebarTrigger,
  useSidebar,
} from "@/components/ui/sidebar"
import { useLocation, Link } from '@tanstack/react-router'
import { ModeToggle } from "./mode-toggle"
import { Button } from "./ui/button"
import { SettingsIcon } from "lucide-react"

export function Header() {
  const { pathname } = useLocation()
  const { isMobile } = useSidebar()

  type PathItem = {
    path: string;
    title: string;
  };

  const createPathData = (path: string): PathItem[] => {
    const parts = path.split("/").filter(Boolean);

    return parts.map((part, index) => {
      const fullPath = "/" + parts.slice(0, index + 1).join("/");

      return {
        path: fullPath,
        title: part.charAt(0).toUpperCase() + part.slice(1),
      };
    });
  };

  const formatTitle = (s: string) =>
    s
      .replace(/[-_]/g, " ")
      .replace(/\b\w/g, (c) => c.toUpperCase());

  const createdPathData = createPathData(String(pathname));
  const indexesToRemove: number[] = [];
  const filteredPathData = createdPathData.filter((_, index) => !indexesToRemove.includes(index));

  return (
    <header className="flex h-16 shrink-0 items-center gap-2 border-b justify-between px-3">
      <div className="flex items-center gap-2">
        {!isMobile && <SidebarTrigger />}
        {!isMobile && (
          <Separator
            orientation="vertical"
            className="mr-2 h-4"
          />
        )}
        <Breadcrumb>
          <BreadcrumbList>
            {createdPathData.length === 0 ? null : filteredPathData.map((_, index) => {
              return (
                <React.Fragment key={index}>
                  {index !== 0 && <BreadcrumbSeparator />}
                  <BreadcrumbItem>
                    <BreadcrumbLink href={_.path}>
                      {formatTitle(_.title)}
                    </BreadcrumbLink>
                  </BreadcrumbItem>
                </React.Fragment>
              )
            })}
          </BreadcrumbList>
        </Breadcrumb>
      </div>
      <div className="flex gap-2">
        <Link to={createdPathData.length === 0 ? "/settings" : createdPathData[0].path + "/settings"}>
          <Button variant="outline" size="icon">
            <SettingsIcon />
          </Button>
        </Link>
        <ModeToggle className="" />
      </div>
    </header>
  )
}