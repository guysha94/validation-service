import {ProtectedPage} from "~/components/auth";
import RulesCard from "~/components/rules-card";
import NewEventDialog from "~/components/NewEventDialog";

type PageProps = {
    params: Promise<{ slug: string }>;
};

export default async function EventPage({params}: PageProps) {

    const {slug} = await params;
    return (
        <ProtectedPage>
            <div className="flex min-h-screen items-center justify-center bg-background py-12 px-4">
                <div className="w-full max-w-4xl">
                    <RulesCard slug={slug}/>
                </div>
            </div>
            <NewEventDialog/>
        </ProtectedPage>
    );
}
