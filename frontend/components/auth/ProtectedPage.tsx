'use server'
import {getServerSession} from "next-auth/next";
import {authOptions} from "~/app/api/auth/[...nextauth]/route";
import {PropsWithChildren} from "react";
import {redirect} from 'next/navigation'

export async function ProtectedPage({children}: PropsWithChildren) {
    const session = await getServerSession(authOptions);
    return !!session ? children : redirect('/signin');
}
