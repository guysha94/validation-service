import {PropsWithChildren} from "react";
import AuthProvider from "./AuthProvider";
import {getServerSession} from "next-auth/next"
import {authOptions} from "~/app/api/auth/[...nextauth]/route";
import QueryProvider from './QueryProvider';
import {dehydrate, HydrationBoundary, QueryClient,} from '@tanstack/react-query'
import AppSidebarProvider from "./AppSidebarProvider";

export default async function AppProviders({children}: PropsWithChildren) {
    const session = await getServerSession(authOptions);
    const queryClient = new QueryClient();
    return (
        <QueryProvider>
            <AuthProvider session={session}>
                <HydrationBoundary state={dehydrate(queryClient)}>
                    <AppSidebarProvider session={session}>
                        {children}

                    </AppSidebarProvider>
                </HydrationBoundary>
            </AuthProvider>
        </QueryProvider>
    );
}
