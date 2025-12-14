"use client";
import {Card, CardContent, CardDescription, CardHeader, CardTitle,} from "~/components/ui/card";
import dynamic from "next/dynamic";

const RulesForm = dynamic(
    () =>
        import("~/components/forms/RulesForm").then((mod) => ({
            default: mod.RulesForm,
        })),
    {
        ssr: false,
        loading: () => <div>Loading...</div>,
    }
);

export default function RulesCard() {

    return (

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

    );
}
