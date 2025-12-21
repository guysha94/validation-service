"use client";
import {createCollection} from '@tanstack/react-db'
import {queryCollectionOptions} from '@tanstack/query-db-collection'
import {rulesSchema, validationsSchema} from './schemas'
import {api} from "~/lib/api";
import {getQueryClient} from "~/lib/query-client";


export const validationsCollection = createCollection(
    queryCollectionOptions({
        id: 'validations',
        schema: validationsSchema,
        queryClient: getQueryClient(),
        queryKey: ['validations'],
        getKey: (item) => item.id,
        queryFn: () => api.validations.getAll(),
        onInsert: ({transaction}) => {
            const mutation = transaction.mutations[0];
            return api.validations.create(mutation.modified);
        },
        onUpdate: ({transaction}) => {
            const mutation = transaction.mutations[0];
            return api.validations.update(mutation.original.id, mutation.changes);
        },
    }),
);

export const rulesCollection = createCollection(
    queryCollectionOptions({
        id: 'rules',
        schema: rulesSchema,
        queryClient: getQueryClient(),
        queryKey: ['rules'],
        getKey: (item) => item.id,
        queryFn: () => api.rules.getAll(),
        onInsert: ({transaction}) => {
            return api.rules.create(transaction.mutations.map(m => m.modified));
        },
        onUpdate: async ({transaction}) => {

            if(transaction.mutations.length ===0) return;
            if(transaction.mutations.length ===1){
                const mutation = transaction.mutations[0];
                return api.rules.updateOne(mutation.original.id, mutation.changes);
            }

            const updates = transaction.mutations.map(m => ({
                id: m.key,
                changes: m.changes
            }))
            return await api.rules.updateMany(updates);
        },
    }));
