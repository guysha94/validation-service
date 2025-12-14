"use client";

import { useLiveQuery } from "@tanstack/react-db";

/**
 * A wrapper around useLiveQuery that only runs on the client side.
 * This hook should only be used in client components.
 *
 * Note: This hook will still call useLiveQuery on the server during SSR,
 * which may cause warnings. To fully prevent SSR, use Next.js dynamic
 * imports with ssr: false for components using this hook.
 *
 * @param queryFn - The query function passed to useLiveQuery (e.g., (q) => q.from({validation: collection}))
 * @param getServerSnapshot - Function that returns the server-side snapshot (defaults to empty array)
 */
export function useLiveQuerySSR<T = any>(
  queryFn: (q: any) => any,
  getServerSnapshot: () => T[] = () => []
) {
  // Check if we're on the client side
  const isClient = typeof window !== 'undefined';

  // Always call useLiveQuery (React hooks rules)
  // On server, this will cause a warning but React will handle it
  const liveQueryResult = useLiveQuery(queryFn);

  // On server, return server snapshot
  // On client, return live query result
  if (!isClient) {
    return {
      data: getServerSnapshot() as T[],
      isLoading: true,
    };
  }

  return liveQueryResult;
}
