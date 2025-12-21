"use client";
import {Card, CardContent, CardDescription, CardHeader, CardTitle,} from "~/components/ui/card";
import RulesForm from "~/components/forms/RulesForm";
import {ilike, useLiveQuery} from "@tanstack/react-db";
import {validationsCollection} from "~/db/collections";
import SkeletonCard from "~/components/CardSkeleton";
import {useMemo} from "react";

type RulesCardProps = {
    slug?: string | null | undefined;
};

export function RulesCard({slug}: RulesCardProps) {

    const {data: validations = [], isLoading} = useLiveQuery(
        (q) => q.from({validation: validationsCollection})
            .where(({validation}) => ilike(validation.event_type, slug))
            .select(({validation}) => ({
                label: validation.label,
                event_type: validation.event_type,
                id: validation.id,
            }))
            .orderBy(({validation}) => validation.id, 'asc')
            .limit(1)
    );

    const event = useMemo(() => validations?.[0] || {
        label: `Event Of Type "${slug} Not Found"`,
        event_type: slug || 'unknown',
        id: '',
    }, [validations, slug]);

    if (isLoading) return <SkeletonCard/>


    return (

        <Card>
            <CardHeader>
                <CardTitle className="flex flex-row">

                    Create Validation Rules For <pre><code>{event.label}</code></pre></CardTitle>
                <CardDescription>
                    Add rules for event validation. Each rule requires a name, error message, and query.
                </CardDescription>
            </CardHeader>
            <CardContent>
                <RulesForm eventType={event.event_type} eventId={event.id}/>
            </CardContent>
        </Card>

    );
}

export default RulesCard;
