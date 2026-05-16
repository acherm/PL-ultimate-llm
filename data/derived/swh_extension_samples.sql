-- SWH popular-content-names mining for 84 extensions
-- spanning 1 in-repo languages.
-- Contents source: /tmp/swh_shards/0.parquet
--
-- Strategy: extract the extension ONCE per row via a single regex (capture
-- group is restricted to ASCII so `lower()` is safe), then filter against an
-- IN-set. This is O(rows) vs the previous O(rows * extensions) cross-join.
-- The full filename is only decoded for the final K * N output rows.

WITH cnts AS (
    SELECT
        c.id                                      AS content_id,
        c.length                                  AS length,
        c.filename                                AS filename_blob,
        c.filename_occurrences                    AS occurrences,
        c.first_occurrence_timestamp              AS first_ts,
        c.first_occurrence_revrel                 AS first_revrel_id,
        c.first_occurrence_origin                 AS first_origin_id,
        lower(regexp_extract(
            decode(c.filename, 'ignore'),
            '\.([A-Za-z0-9_+\-]{1,8})$',
            1
        )) AS ext_no_dot
    FROM read_parquet('/tmp/swh_shards/0.parquet') AS c
    WHERE c.length BETWEEN 32 AND 200000
      AND octet_length(c.filename) BETWEEN 4 AND 256
    USING SAMPLE 1.0 PERCENT (BERNOULLI)
),
matched AS (
    SELECT
        content_id, length, filename_blob, occurrences,
        first_ts, first_revrel_id, first_origin_id,
        '.' || ext_no_dot AS extension
    FROM cnts
    WHERE ext_no_dot <> ''
      AND ext_no_dot IN ('0', '2', '3', 'a', 'am', 'apk', 'arff', 'bmp', 'cache', 'class', 'cmd', 'conf', 'config', 'crc', 'dat', 'data', 'db', 'dds', 'dex', 'doctree', 'docx', 'fasta', 'fbx', 'flat', 'form', 'glif', 'h5', 'hh', 'hocr', 'ico', 'idb', 'import', 'in', 'inc', 'index', 'info', 'jar', 'jpeg', 'key', 'ko', 'list', 'lock', 'lst', 'map', 'markdown', 'mf', 'mk', 'mp3', 'mp4', 'mvt', 'npy', 'npz', 'o', 'ogg', 'out', 'parquet', 'pbf', 'pbxproj', 'pdb', 'pem', 'pickle', 'pm', 'ppm', 'pyc', 'rawproto', 'rdata', 'rds', 'scssc', 'sig', 'stdout', 'sum', 'tdb', 'tga', 'tif', 'tlog', 'uasset', 'vtp', 'wav', 'web', 'webp', 'xcscheme', 'xhtml', 'xls', 'xlsx')
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
WHERE rk <= 3
ORDER BY extension, rk;
