"use client";

import {useFieldArray, useForm} from "react-hook-form";
import {useEffect, useState} from "react";
import {Plus, Trash2} from "lucide-react";
import {Button} from "~/components/ui/button";
import {Input} from "~/components/ui/input";
import {Label} from "~/components/ui/label";
import {Card, CardContent, CardHeader, CardTitle,} from "~/components/ui/card";
import {Form, FormControl, FormField, FormItem, FormLabel, FormMessage,} from "~/components/ui/form";
import {SqlQuerySchema} from "~/domain";
import {rulesCollection} from "~/db/collections";
import {Spinner} from "~/components/ui/spinner";
import {eq, useLiveQuery} from "@tanstack/react-db";
import SQLEditor from "~/components/SQLEditor";
import * as z from "zod";
import {zodResolver} from "@hookform/resolvers/zod";
import dynamic from "next/dynamic";
import {rulesSchema} from "~/db/schemas";
import _ from 'lodash';

type RulesFormProps = {
    eventType: string;
    eventId: string;
};

const ruleSchema = z.object({
    id: z.string().nullable().optional().default(""),
    name: z.string().min(1, {message: "Rule name is required"}),
    error_message: z.string().min(1, {message: "Error message is required"}),
    query: SqlQuerySchema,
});

const formSchema = z.object({
    rules: z.array(ruleSchema).min(1, {message: "At least one rule is required"}),
});

type FormData = z.infer<typeof formSchema>;

export function RulesFormComponent({eventType, eventId}: RulesFormProps) {
    const {data: rules = [], isLoading} = useLiveQuery(
        (q) => q.from({rules: rulesCollection})
            .where(({rules}) => eq(rules.validation_id, eventId)),
    )

    const [isSubmitting, setIsSubmitting] = useState(false);
    const [submitMessage, setSubmitMessage] = useState<{
        type: "success" | "error";
        message: string;
    } | null>(null);

    const form = useForm({
        resolver: zodResolver(formSchema),
        mode: "onChange",
        defaultValues: {
            rules: [{name: "", error_message: "", query: ""}],
        },

    });

    const {fields, append, remove} = useFieldArray({
        control: form.control,
        name: "rules",
    });

    const onSubmit = async (data: FormData) => {
        setIsSubmitting(true);
        setSubmitMessage(null);

        try {
            const existingQueries = rules.map(r => r.query);
            const toInsert = data.rules.filter(r => !r.id && !existingQueries.includes(r.query));
            const toUpdate = data.rules.filter(r => r.id && !existingQueries.includes(r.query));
            const tasks: Promise<any>[] = [];
            if (toInsert.length) {
                const insertTx = rulesCollection.insert(toInsert.map(r => rulesSchema.parse(r)));
                tasks.push(insertTx.isPersisted.promise)

            }


            if (toUpdate.length) {
                const updatedIds: string[] = _.intersection([
                    rules.map(r => r.id),
                    toUpdate.map(r => r.id)]
                ).flat().filter(Boolean) as string[];

                const updateTx = rulesCollection.update(updatedIds, (drafts) => {
                    drafts.forEach((draft) => {
                        const updated = toUpdate.find(r => r.id === draft.id);
                        if (updated) {
                            draft.name = updated.name;
                            draft.error_message = updated.error_message;
                            draft.query = updated.query;
                        }
                    })
                });
                tasks.push(updateTx.isPersisted.promise);
            }

            if (tasks.length > 0) {
                await Promise.all(tasks);
            }

            setSubmitMessage({
                type: "success",
                message: "Rules saved successfully",
            });


        } catch (error) {
            setSubmitMessage({
                type: "error",
                message: error instanceof Error ? error.message : "An error occurred",
            });
        } finally {
            setIsSubmitting(false);
        }
    };


    const onRemove = async (index: number, id: string) => {
        remove(index);
        if (id) {
            const tx = rulesCollection.delete(id);
            await tx.isPersisted.promise;
        }
    };

    useEffect(() => {

        if (isLoading) return;
        if (rules.length > 0) {
            form.reset({
                rules: rules.map((rule) => ({
                    name: rule.name,
                    error_message: rule.error_message,
                    query: rule.query,
                })),
            });
        }


    }, [isLoading, rules, form]);

    if (isLoading) {
        return <div>Loading...</div>;
    }

    return (<Form {...form}>
        <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">

            <div className="space-y-4">
                <div className="flex items-center justify-between">
                    <Label>
                        Rules <span className="text-destructive">*</span>
                    </Label>
                    <Button
                        type="button"
                        variant="outline"
                        size="sm"
                        onClick={() => append({id: "", name: "", error_message: "", query: ""})}
                    >
                        <Plus className="h-4 w-4"/>
                        Add Rule
                    </Button>
                </div>

                <div className="space-y-4">
                    {fields.map((field, index) => (
                        <Card key={field.id}>
                            <CardHeader className="pb-4">
                                <div className="flex items-center justify-between">
                                    <CardTitle className="text-lg">Rule {index + 1}</CardTitle>
                                    {fields.length > 1 && (
                                        <Button
                                            type="button"
                                            variant="ghost"
                                            size="sm"
                                            onClick={() => onRemove(index, field.id)}
                                            className="text-destructive hover:text-destructive"
                                        >
                                            <Trash2 className="h-4 w-4"/>
                                        </Button>
                                    )}
                                </div>
                            </CardHeader>
                            <CardContent className="space-y-4">
                                {/* Rule Name */}
                                <FormField
                                    control={form.control}
                                    name={`rules.${index}.name`}
                                    rules={{required: "Rule name is required"}}
                                    render={({field}) => (
                                        <FormItem>
                                            <FormLabel>
                                                Name <span className="text-destructive">*</span>
                                            </FormLabel>
                                            <FormControl>
                                                <Input
                                                    placeholder="e.g., email_format_check"
                                                    {...field}
                                                />
                                            </FormControl>
                                            <FormMessage/>
                                        </FormItem>
                                    )}
                                />

                                {/* Error Message */}
                                <FormField
                                    control={form.control}
                                    name={`rules.${index}.error_message`}
                                    rules={{required: "Error message is required"}}
                                    render={({field}) => (
                                        <FormItem>
                                            <FormLabel>
                                                Error Message <span className="text-destructive">*</span>
                                            </FormLabel>
                                            <FormControl>
                                                <Input
                                                    placeholder="e.g., Invalid email format"
                                                    {...field}
                                                />
                                            </FormControl>
                                            <FormMessage/>
                                        </FormItem>
                                    )}
                                />

                                {/* Query */}
                                <FormField
                                    control={form.control}
                                    name={`rules.${index}.query`}
                                    rules={{required: "Query is required"}}
                                    render={({field}) => (
                                        <FormItem>
                                            <FormLabel>
                                                Query <span className="text-destructive">*</span>
                                            </FormLabel>
                                            <FormControl>
                                                <SQLEditor
                                                    value={field.value}
                                                    onChange={field.onChange}
                                                    placeholder="e.g., email LIKE '%@%.%'"
                                                />
                                            </FormControl>
                                            <FormMessage/>
                                        </FormItem>
                                    )}
                                />
                            </CardContent>
                        </Card>
                    ))}
                </div>
            </div>


            <div className="flex items-center justify-end pt-4">
                <Button type="submit" disabled={isSubmitting} className="cursor-pointer">
                    {isSubmitting && <Spinner/>}
                    {isSubmitting ? "Saving..." : "Save"}
                </Button>
            </div>

            {submitMessage && (
                <div
                    className={`p-4 rounded-md border ${
                        submitMessage.type === "success"
                            ? "bg-green-50 dark:bg-green-900/20 text-green-800 dark:text-green-200 border-green-200 dark:border-green-800"
                            : "bg-destructive/10 text-destructive border-destructive/20"
                    }`}
                >
                    {submitMessage.message}
                </div>
            )}
        </form>
    </Form>);
}

export const RulesForm = dynamic(() => Promise.resolve(RulesFormComponent), {
    ssr: false,
    loading: () => <div>Loading...</div>,
});

export default RulesForm;
