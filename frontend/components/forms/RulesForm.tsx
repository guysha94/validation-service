"use client";

import {useFieldArray, useForm} from "react-hook-form";
import {useState} from "react";
import {Plus, Trash2} from "lucide-react";
import {Button} from "~/components/ui/button";
import {Input} from "~/components/ui/input";
import {Textarea} from "~/components/ui/textarea";
import {Label} from "~/components/ui/label";
import {Card, CardContent, CardHeader, CardTitle,} from "~/components/ui/card";
import {Form, FormControl, FormField, FormItem, FormLabel, FormMessage,} from "~/components/ui/form";
import {FormData} from "~/domain";
import { useSession } from "next-auth/react"


export function RulesForm() {
    const session = useSession();
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [submitMessage, setSubmitMessage] = useState<{
        type: "success" | "error";
        message: string;
    } | null>(null);

    const form = useForm<FormData>({
        defaultValues: {
            event_type: "",
            rules: [{ name: "", error_message: "", query: "" }],
        },
        mode: "onChange",
    });

    const { fields, append, remove } = useFieldArray({
        control: form.control,
        name: "rules",
    });

    const onSubmit = async (data: FormData) => {
        setIsSubmitting(true);
        setSubmitMessage(null);

        try {
            const response = await fetch("http://localhost:3001/api/create_rules", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(data),
            });

            const result = await response.json();

            if (response.ok && result.success) {
                setSubmitMessage({
                    type: "success",
                    message: `Successfully created ${result.created_rule_ids.length} rule(s)!`,
                });
                form.reset();
            } else {
                setSubmitMessage({
                    type: "error",
                    message: result.error || "Failed to create rules",
                });
            }
        } catch (error) {
            setSubmitMessage({
                type: "error",
                message: error instanceof Error ? error.message : "An error occurred",
            });
        } finally {
            setIsSubmitting(false);
        }
    };
    console.log(session);
    return (<Form {...form}>
                            <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">

                                <FormField
                                    control={form.control}
                                    name="event_type"
                                    rules={{
                                        required: "Event type is required",
                                    }}
                                    render={({ field }) => (
                                        <FormItem>
                                            <FormLabel>
                                                Event Type <span className="text-destructive">*</span>
                                            </FormLabel>
                                            <FormControl>
                                                <Input
                                                    placeholder="e.g., user_registration, payment_processing"
                                                    {...field}
                                                />
                                            </FormControl>
                                            <FormMessage />
                                        </FormItem>
                                    )}
                                />

                                {/* Rules Section */}
                                <div className="space-y-4">
                                    <div className="flex items-center justify-between">
                                        <Label>
                                            Rules <span className="text-destructive">*</span>
                                        </Label>
                                        <Button
                                            type="button"
                                            variant="outline"
                                            size="sm"
                                            onClick={() => append({ name: "", error_message: "", query: "" })}
                                        >
                                            <Plus className="h-4 w-4" />
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
                                                                onClick={() => remove(index)}
                                                                className="text-destructive hover:text-destructive"
                                                            >
                                                                <Trash2 className="h-4 w-4" />
                                                            </Button>
                                                        )}
                                                    </div>
                                                </CardHeader>
                                                <CardContent className="space-y-4">
                                                    {/* Rule Name */}
                                                    <FormField
                                                        control={form.control}
                                                        name={`rules.${index}.name`}
                                                        rules={{ required: "Rule name is required" }}
                                                        render={({ field }) => (
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
                                                                <FormMessage />
                                                            </FormItem>
                                                        )}
                                                    />

                                                    {/* Error Message */}
                                                    <FormField
                                                        control={form.control}
                                                        name={`rules.${index}.error_message`}
                                                        rules={{ required: "Error message is required" }}
                                                        render={({ field }) => (
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
                                                                <FormMessage />
                                                            </FormItem>
                                                        )}
                                                    />

                                                    {/* Query */}
                                                    <FormField
                                                        control={form.control}
                                                        name={`rules.${index}.query`}
                                                        rules={{ required: "Query is required" }}
                                                        render={({ field }) => (
                                                            <FormItem>
                                                                <FormLabel>
                                                                    Query <span className="text-destructive">*</span>
                                                                </FormLabel>
                                                                <FormControl>
                                                                    <Textarea
                                                                        placeholder="e.g., email LIKE '%@%.%'"
                                                                        rows={3}
                                                                        {...field}
                                                                    />
                                                                </FormControl>
                                                                <FormMessage />
                                                            </FormItem>
                                                        )}
                                                    />
                                                </CardContent>
                                            </Card>
                                        ))}
                                    </div>
                                </div>

                                {/* Submit Button */}
                                <div className="flex items-center justify-end pt-4">
                                    <Button type="submit" disabled={isSubmitting}>
                                        {isSubmitting ? "Submitting..." : "Create Rules"}
                                    </Button>
                                </div>

                                {/* Submit Message */}
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
