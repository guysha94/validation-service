"use client"
import {SessionProvider} from "next-auth/react"
import {PropsWithChildren} from "react";

import {type Session} from "next-auth";

type AuthProviderProps = {
    session?: Session | null | undefined
}

export default function AuthProvider({session, children}: PropsWithChildren<AuthProviderProps>) {

    return (
        <SessionProvider
            session={session}
            refetchInterval={3 * 60}
            refetchOnWindowFocus
        >
            {children}
        </SessionProvider>
    )
}
