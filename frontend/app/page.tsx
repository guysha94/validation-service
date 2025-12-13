import {Card, CardContent, CardDescription, CardHeader, CardTitle,} from "~/components/ui/card";
import {RulesForm} from "~/components/forms";
import {ProtectedPage} from "~/components/auth";

export default async function Home() {


    return (
        <ProtectedPage>
            <div className="flex min-h-screen items-center justify-center bg-background py-12 px-4">
                <div className="w-full max-w-4xl">
                    <Card>
                        <CardHeader>
                            <CardTitle>Create Validation Rules</CardTitle>
                            <CardDescription>
                                Add rules for event validation. Each rule requires a name, error message, and query.
                            </CardDescription>
                        </CardHeader>
                        <CardContent>
                            <RulesForm/>
                        </CardContent>
                    </Card>
                </div>
            </div>
        </ProtectedPage>
    );
}
