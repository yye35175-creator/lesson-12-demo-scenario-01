CREATE TABLE found_items (
    id TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    storage_point TEXT NOT NULL,
    proof_colour TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'AVAILABLE'
        CHECK (status IN ('AVAILABLE', 'HELD', 'COLLECTED'))
);

CREATE TABLE claimants (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL
);

-- Add claims, foreign keys and the rule for at most one active claim per item.
