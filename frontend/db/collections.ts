"use client";
import {createCollection} from '@tanstack/react-db'
import {queryCollectionOptions} from '@tanstack/query-db-collection'
import {rulesSchema, validationsSchema} from './schemas'
import {api} from "~/lib/api";
import {getQueryClient} from "~/lib/query-client";


export const validationsCollection = createCollection(
    queryCollectionOptions({
        schema: validationsSchema,
        queryClient: getQueryClient(),
        queryKey: ['validations'],
        queryFn: () => api.validations.getAll(),
        getKey: (item) => item.id,
    }));

export const rulesCollection = createCollection(
    queryCollectionOptions({
        schema: rulesSchema,
        queryClient: getQueryClient(),
        queryKey: ['rules'],
        queryFn: () => api.rules.getAll(),
        getKey: (item) => item.id,
    }));
