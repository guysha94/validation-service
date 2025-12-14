"use client"
import {useCallback} from "react";
import {
    SidebarGroup,
    SidebarGroupContent,
    SidebarMenu,
    SidebarMenuButton,
    SidebarMenuItem,
} from "@/components/ui/sidebar"
import {SideBarItem} from "~/domain";
import {useValidationsStore} from "~/store";
import {useShallow} from 'zustand/react/shallow'
import {Plus} from "lucide-react";
import {Button} from "~/components/ui/button";

export default function NavMain({
                                    items,
                                }: {
    items: SideBarItem[]
}) {

    const {addFormOpen, toggleAddFormOpen, setCurrentEvent} = useValidationsStore(useShallow((state) => state));

    const onSelectedEvent = useCallback((eventType: { id: string, type: string, label: string } | null | undefined) => {
        setCurrentEvent(eventType);
    }, [setCurrentEvent]);


    return (
        <SidebarGroup>
            <SidebarGroupContent className="flex flex-col gap-2">

                <SidebarMenu>
                    <SidebarMenuItem className="cursor-pointer" onClick={toggleAddFormOpen}>
                        <Button
                            variant="outline"
                            className="w-full justify-start cursor-pointer"
                        >

                            <Plus/>
                            <span>New Event</span>
                        </Button>
                    </SidebarMenuItem>
                    {items.map((item) => (
                        <SidebarMenuItem key={item.title} className="cursor-pointer">
                            <SidebarMenuButton className="cursor-pointer" tooltip={item.title} onClick={()=>onSelectedEvent({id: item.id, type: item.type, label: item.title})} >
                                {item.icon && <item.icon/>}
                                <span>{item.title}</span>
                            </SidebarMenuButton>
                        </SidebarMenuItem>
                    ))}
                </SidebarMenu>
            </SidebarGroupContent>
        </SidebarGroup>
    )
}
