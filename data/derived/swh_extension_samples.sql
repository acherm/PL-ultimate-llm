-- SWH popular-content-names mining for 141 extensions
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
    WHERE c.filename_last_extension IN ('ac'::BLOB, 'am'::BLOB, 'ann'::BLOB, 'asciipb'::BLOB, 'assets'::BLOB, 'aux'::BLOB, 'baml'::BLOB, 'bash'::BLOB, 'beam'::BLOB, 'blob'::BLOB, 'blp'::BLOB, 'br'::BLOB, 'build'::BLOB, 'cbp'::BLOB, 'cdb'::BLOB, 'code'::BLOB, 'comp'::BLOB, 'config'::BLOB, 'crc'::BLOB, 'crf'::BLOB, 'data'::BLOB, 'dbd'::BLOB, 'dcm'::BLOB, 'dcu'::BLOB, 'dds'::BLOB, 'dep'::BLOB, 'doctree'::BLOB, 'drawio'::BLOB, 'dwlt'::BLOB, 'egrid'::BLOB, 'enc'::BLOB, 'err'::BLOB, 'example'::BLOB, 'exml'::BLOB, 'exp'::BLOB, 'exr'::BLOB, 'fa'::BLOB, 'fasta'::BLOB, 'fits'::BLOB, 'flat'::BLOB, 'form'::BLOB, 'frm'::BLOB, 'fsf'::BLOB, 'gemspec'::BLOB, 'glif'::BLOB, 'glyph'::BLOB, 'hdb'::BLOB, 'history'::BLOB, 'icloud'::BLOB, 'idb'::BLOB, 'ide'::BLOB, 'ilk'::BLOB, 'import'::BLOB, 'in'::BLOB, 'index'::BLOB, 'internal'::BLOB, 'ipch'::BLOB, 'ipset'::BLOB, 'isql'::BLOB, 'item'::BLOB, 'job'::BLOB, 'jsonp'::BLOB, 'key'::BLOB, 'ko'::BLOB, 'lang'::BLOB, 'layout'::BLOB, 'lib'::BLOB, 'link'::BLOB, 'list'::BLOB, 'lst'::BLOB, 'mag'::BLOB, 'mail'::BLOB, 'mat'::BLOB, 'mca'::BLOB, 'mdl'::BLOB, 'mf'::BLOB, 'mjava'::BLOB, 'mk'::BLOB, 'model'::BLOB, 'module'::BLOB, 'mol'::BLOB, 'mvt'::BLOB, 'nex'::BLOB, 'nib'::BLOB, 'nq'::BLOB, 'page'::BLOB, 'pbxproj'::BLOB, 'pcap'::BLOB, 'pcm'::BLOB, 'pdbqt'::BLOB, 'pgm'::BLOB, 'plo'::BLOB, 'pm'::BLOB, 'ppm'::BLOB, 'profile'::BLOB, 'pth'::BLOB, 'pz'::BLOB, 'rawproto'::BLOB, 'rc'::BLOB, 'report'::BLOB, 'result'::BLOB, 'ri'::BLOB, 'rmet'::BLOB, 'root'::BLOB, 'rpt'::BLOB, 'rsp'::BLOB, 'scssc'::BLOB, 'sdf'::BLOB, 'ser'::BLOB, 'sig'::BLOB, 'stdout'::BLOB, 'stex'::BLOB, 'stg'::BLOB, 'strings'::BLOB, 'sum'::BLOB, 'suo'::BLOB, 'tdb'::BLOB, 'template'::BLOB, 'test'::BLOB, 'tests'::BLOB, 'tmx'::BLOB, 'trace'::BLOB, 'tsd'::BLOB, 'uasset'::BLOB, 'umap'::BLOB, 'user'::BLOB, 'v2'::BLOB, 'v8'::BLOB, 'vcproj'::BLOB, 'vi'::BLOB, 'vtp'::BLOB, 'vtpana'::BLOB, 'vtu'::BLOB, 'wxml'::BLOB, 'wxss'::BLOB, 'xaml'::BLOB, 'xcconfig'::BLOB, 'xcscheme'::BLOB, 'xtb'::BLOB, 'xyz'::BLOB, 'yy'::BLOB)
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
WHERE rk <= 3
ORDER BY extension, rk;
