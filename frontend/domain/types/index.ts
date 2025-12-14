import {type LucideIcon} from "lucide-react";


export type  Rule = {
    name: string;
    error_message: string;
    query: string;
};

export type FormData = {
    event_type: string;
    rules: Rule[];
};

export type SideBarItem = {
    id: string;
    title: string;
    type: string;
    url: string;
    icon?: LucideIcon | null | undefined;
};
