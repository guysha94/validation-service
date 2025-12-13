import {PropsWithChildren} from "react";
import AuthProvider from "./AuthProvider";
import {getServerSession} from "next-auth/next"
import {authOptions} from "~/app/api/auth/[...nextauth]/route";

export default async function AppProviders({ children }: PropsWithChildren) {
    const session = await getServerSession(authOptions)
    return (
        <AuthProvider session={session}>
            {children}
        </AuthProvider>
    );
}
