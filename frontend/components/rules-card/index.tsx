"use client";
import dynamic from "next/dynamic";

export const RulesCard = dynamic(
    () =>
        import("./RulesCard").then((mod) => ({
            default: mod.RulesCard,
        })),
    {
        ssr: false,
        loading: () => <div>Loading...</div>,
    }
);

export default RulesCard;
