"use client";
import {createElement, memo, useState} from "react";
import {CheckIcon, ChevronsUpDownIcon, icons, type LucideIcon} from 'lucide-react';
import {cn} from "@/lib/utils"
import {Button} from "@/components/ui/button"
import {Command, CommandEmpty, CommandGroup, CommandInput, CommandItem, CommandList,} from "@/components/ui/command"
import {Popover, PopoverContent, PopoverTrigger,} from "@/components/ui/popover"
import _ from "lodash";

const iconsList = Object.keys(icons);


function SelectIcon() {

    const [open, setOpen] = useState(false)
    const [value, setValue] = useState("");


    return (
        <Popover open={open} onOpenChange={setOpen}>
            <PopoverTrigger asChild>
                <Button
                    variant="outline"
                    role="combobox"
                    aria-expanded={open}
                    className="w-[250px] justify-between cursor-pointer"
                >
                    {value
                        ? iconsList.find((icon) => icon === value)
                        : "Select Icon"}
                    <ChevronsUpDownIcon className="ml-2 h-4 w-4 shrink-0 opacity-50"/>
                </Button>
            </PopoverTrigger>
            <PopoverContent className="w-[250px] p-0">
                <Command>
                    <CommandInput placeholder="Search Icon"/>
                    <CommandList>
                        <CommandEmpty>No icons found.</CommandEmpty>
                        <CommandGroup>
                            {iconsList.map((icon, idx) => (
                                <CommandItem
                                    key={idx}
                                    value={icon}
                                    onSelect={(currentValue) => {
                                        setValue(currentValue === value ? "" : currentValue)
                                        setOpen(false)
                                    }}
                                >
                                    <CheckIcon
                                        className={cn(
                                            "mr-2 h-4 w-4",
                                            value === icon ? "opacity-100" : "opacity-0"
                                        )}
                                    />
                                    {
                                        <>

                                            {createElement(icons[icon] as LucideIcon)}
                                            <span>{_.startCase(icon)}</span>
                                        </>
                                    }

                                </CommandItem>
                            ))}
                        </CommandGroup>
                    </CommandList>
                </Command>
            </PopoverContent>
        </Popover>
    )
}

export default memo(SelectIcon);