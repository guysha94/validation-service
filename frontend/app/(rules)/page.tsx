import {ProtectedPage} from "~/components/auth";
import RulesCard from "~/components/RulesCard";

export default async function Home() {


    return (
        <ProtectedPage>
            <div className="flex min-h-screen items-center justify-center bg-background py-12 px-4">
                <div className="w-full max-w-4xl">
                    <RulesCard/>
                </div>
            </div>
        </ProtectedPage>
    );
}
