import {z} from 'zod'


export const DateTimeSchema = z.union([z.string(), z.date()]).transform((val) => {
    if (!val) return val
    return typeof val === 'string' ? new Date(val) : val
}).nullable().default(null);

export const validationsSchema = z.object({
    id: z.string(),
    event_type: z.string(),
    label: z.string().nullable().default(null),
    icon: z.string().nullable().default(null),
    updated_at: DateTimeSchema,
    created_at: DateTimeSchema,
});

export type ValidationsSchema = z.infer<typeof validationsSchema>;

export const validationsInsertSchema = validationsSchema.omit({
    id: true,
});

export type ValidationsInsertSchema = z.infer<typeof validationsInsertSchema>;

export const rulesSchema = z.object({
    id: z.string(),
    validation_id: z.string(),
    name: z.string(),
    error_message: z.string(),
    query: z.string(),
    updated_at: DateTimeSchema,
    created_at: DateTimeSchema,
});

export type RulesSchema = z.infer<typeof rulesSchema>;

export const rulesInsertSchema = rulesSchema.omit({
    id: true,
});

export type RulesInsertSchema = z.infer<typeof rulesInsertSchema>;

export const usersSchema = z.object({
    id: z.string(),
    name: z.string(),
    email: z.string(),
    disabled: z.boolean(),
    updated_at: DateTimeSchema,
    created_at: DateTimeSchema,
});

export type UsersSchema = z.infer<typeof usersSchema>;

export const usersInsertSchema = usersSchema.omit({
    id: true,
});

export type UsersInsertSchema = z.infer<typeof usersInsertSchema>;
