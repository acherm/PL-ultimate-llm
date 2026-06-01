-- SWH popular-content-names mining for 1 extensions
-- spanning 1 in-repo languages.
-- Contents source: s3://softwareheritage/derived_datasets/2026-03-02/contents_with_extensions/0.parquet
--
-- Strategy: filter on `filename_last_extension` (BLOB) against an
-- IN-set of requested extensions. DuckDB pushes the predicate
-- into READ_PARQUET; the column's per-row-group Bloom filter
-- prunes row groups whose extension set doesn't overlap ours.

WITH cnts AS (
    SELECT
        c.id                                      AS content_id,
        c.length                                  AS length,
        c.filename                                AS filename_blob,
        c.filename_last_extension                 AS ext_blob,
        c.filename_occurrences                    AS occurrences,
        c.first_occurrence_timestamp              AS first_ts,
        c.first_occurrence_revrel                 AS first_revrel_id,
        c.first_occurrence_origin                 AS first_origin_id
    FROM read_parquet('s3://softwareheritage/derived_datasets/2026-03-02/contents_with_extensions/0.parquet') AS c
    WHERE c.filename_last_extension IN ('fsf'::BLOB)
      AND c.length BETWEEN 32 AND 200000
    
),
matched AS (
    SELECT
        content_id, length, filename_blob, occurrences,
        first_ts, first_revrel_id, first_origin_id,
        '.' || decode(ext_blob, 'ignore') AS extension
    FROM cnts
    WHERE occurrences >= 5
),
ranked AS (
    SELECT *,
        row_number() OVER (
            PARTITION BY extension
            ORDER BY occurrences DESC, length ASC, content_id ASC
        ) AS rk
    FROM matched
)
SELECT
    extension,
    rk,
    content_id,
    decode(filename_blob, 'ignore') AS filename_str,
    length,
    occurrences,
    first_ts,
    first_revrel_id,
    first_origin_id
FROM ranked
WHERE rk <= 30
ORDER BY extension, rk;
