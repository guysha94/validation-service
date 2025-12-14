import * as z from "zod";


const formSchema = z.object({
    type: z.string().min(2, {message: "Event type is required"}),
    title: z.string().nullable().default(""),
    icon: z.string().nullable().default(""),
})

export default function NewEventForm() {
    return (
        <div>
            <h1>New Event Form</h1>
            {/* Form fields go here */}
        </div>
    );
}