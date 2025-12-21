"use client"

import * as React from "react"
import {ComponentProps, useMemo} from "react"
import * as Icons from "lucide-react";
import {BadgeQuestionMark, type LucideIcon, SearchCode} from "lucide-react";
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
import {Skeleton} from "@/components/ui/skeleton"


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
            url: `/validations/${validation.event_type}`.toLowerCase(),
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
                {isLoading ?
                    (
                        <Skeleton className="h-4 w-[250px]"/>
                    )
                    :
                    (
                        <NavMain items={items}/>
                    )}

            </SidebarContent>
            <SidebarFooter>
                <NavUser user={session.user}/>
            </SidebarFooter>
        </Sidebar>
    )
}
