"use client"

import * as React from "react"
import {ComponentProps, useMemo} from "react"
import * as Icons from "lucide-react";
import {
    BadgeQuestionMark,
    Camera,
    ChartColumn,
    Database,
    FileSpreadsheet,
    FileText,
    Folder,
    LayoutDashboard,
    LayoutList,
    type LucideIcon,
    Search,
    SearchCode,
    Settings,
    Users
} from "lucide-react";
import NavMain from "./NavMain"
import NavUser from "./NavUser"
import {
    Sidebar,
    SidebarContent,
    SidebarFooter,
    SidebarHeader,
    SidebarMenu,
    SidebarMenuButton,
    SidebarMenuItem,
} from "@/components/ui/sidebar"
import {type Session} from "next-auth";
import Link from 'next/link'
import {useLiveQuery} from "@tanstack/react-db";
import {validationsCollection} from "~/db/collections";
import {SideBarItem} from "~/domain";

const data = {
    user: {
        name: "shadcn",
        email: "m@example.com",
        avatar: "/avatars/shadcn.jpg",
    },
    navMain: [
        {
            title: "Dashboard",
            url: "#",
            icon: LayoutDashboard,
        },
        {
            title: "Lifecycle",
            url: "#",
            icon: LayoutList,
        },
        {
            title: "Analytics",
            url: "#",
            icon: ChartColumn,
        },
        {
            title: "Projects",
            url: "#",
            icon: Folder,
        },
        {
            title: "Team",
            url: "#",
            icon: Users,
        },
    ],
    navClouds: [
        {
            title: "Capture",
            icon: Camera,
            isActive: true,
            url: "#",
            items: [
                {
                    title: "Active Proposals",
                    url: "#",
                },
                {
                    title: "Archived",
                    url: "#",
                },
            ],
        },
        {
            title: "Proposal",
            icon: FileText,
            url: "#",
            items: [
                {
                    title: "Active Proposals",
                    url: "#",
                },
                {
                    title: "Archived",
                    url: "#",
                },
            ],
        },
    ],
    navSecondary: [
        {
            title: "Settings",
            url: "#",
            icon: Settings,
        },
        {
            title: "Get Help",
            url: "#",
            icon: BadgeQuestionMark,
        },
        {
            title: "Search",
            url: "#",
            icon: Search,
        },
    ],
    documents: [
        {
            name: "Data Library",
            url: "#",
            icon: Database,
        },
        {
            name: "Reports",
            url: "#",
            icon: FileSpreadsheet,
        },

    ],
}

type AppSidebarProps = ComponentProps<typeof Sidebar> & { session: Session };

export function AppSidebar({session, ...props}: AppSidebarProps) {

    const {data: validations = [], isLoading} = useLiveQuery(
        (q) => q.from({validation: validationsCollection})
            .select(({validation}) => ({
                id: validation.id,
                event_type: validation.event_type,
                icon: validation.icon,
                label: validation.label
            }))
            .orderBy(({validation}) => validation.event_type, 'asc'),
    );

    const items = useMemo(() => {

        return validations.map((validation) => ({
            id: validation.id,
            type: validation.event_type,
            title: validation.label,
            url: `/validations/${validation.id}`,
            icon: (Icons[validation.icon as keyof typeof Icons] || BadgeQuestionMark) as LucideIcon,
        })) as SideBarItem[];

    }, [validations]);

    return (
        <Sidebar collapsible="offcanvas" {...props}>
            <SidebarHeader>
                <SidebarMenu>
                    <SidebarMenuItem>
                        <SidebarMenuButton
                            asChild
                            className="data-[slot=sidebar-menu-button]:!p-1.5"
                        >
                            <Link href="/">
                                <SearchCode/>
                                <span className="text-base font-semibold">Validations</span>
                            </Link>
                        </SidebarMenuButton>
                    </SidebarMenuItem>
                </SidebarMenu>
            </SidebarHeader>
            <SidebarContent>
                <NavMain items={items}/>
                {/*<NavDocuments items={data.documents}/>*/}
                {/*<NavSecondary items={data.navSecondary} className="mt-auto"/>*/}
            </SidebarContent>
            <SidebarFooter>
                <NavUser user={session.user}/>
            </SidebarFooter>
        </Sidebar>
    )
}
