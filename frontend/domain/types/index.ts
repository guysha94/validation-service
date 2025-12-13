

export type  Rule= {
    name: string;
    error_message: string;
    query: string;
};

export type FormData ={
    event_type: string;
    rules: Rule[];
};
