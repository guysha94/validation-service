import NextAuth, {type AuthOptions} from "next-auth"
import CredentialsProvider from "next-auth/providers/credentials"
import {env} from "~/env/server";

export const authOptions: AuthOptions = {
    secret: env.NEXTAUTH_SECRET,
    session: {
        strategy: 'jwt',
    },
    providers: [

        CredentialsProvider({
            name: 'credentials',
            credentials: {
                email: {label: "Email", type: "email", placeholder: "john.doe@superplay.co"},
                password: {label: "Password", type: "password"}
            },
            async authorize(credentials, req) {

                const url = `${env.API_BASE_URL}/auth/login`;
                const res = await fetch(url, {
                    method: 'POST',
                    body: JSON.stringify(credentials),
                    headers: {"Content-Type": "application/json"}
                })
                const data = await res.json()
                if (res.ok && data?.user) return data.user
                return null
            }
        })
    ],
    callbacks: {
        async jwt({token, user}) {

            if (user) {
                token.user = user
            } else if (Object.hasOwn(token, 'email')) {
                token.user = {email: token.email, name: token.name, id: token.sub}
            }
            return token
        },
        async session({session, token}) {

            if (token.user) {
                session.user = token.user
            }
            return session
        },
    }


}


const handler = NextAuth(authOptions)

export {handler as GET, handler as POST}
