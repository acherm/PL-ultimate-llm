-- SWH popular-content-names mining for 881 extensions
-- spanning 1836 in-repo languages.
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
      AND ext_no_dot IN ('1', '1in', '1m', '1x', '2', '3', '3in', '3m', '3p', '3pm', '3qt', '3x', '4', '4dm', '4th', '5', '6', '6pl', '6pm', '7', '8', '9', '_coffee', '_js', '_ls', 'a51', 'abap', 'ada', 'adb', 'ado', 'adoc', 'adp', 'ads', 'agda', 'ahk', 'ahkl', 'aj', 'ak', 'al', 'alg', 'als', 'ampl', 'apex', 'apl', 'app', 'arc', 'arr', 'as', 'asc', 'asciidoc', 'asm', 'asn', 'asn1', 'astro', 'asy', 'au3', 'aug', 'auk', 'aux', 'avdl', 'aw', 'awk', 'b', 'bal', 'bas', 'bash', 'bat', 'bats', 'bb', 'bbappend', 'bbclass', 'bbx', 'be', 'befunge', 'bf', 'bi', 'bicep', 'bison', 'blade', 'bmx', 'bones', 'boo', 'boot', 'bpl', 'bqn', 'bro', 'brs', 'bsv', 'builder', 'bzl', 'c', 'c++', 'c3', 'cairo', 'cake', 'capnp', 'carbon', 'cats', 'cbl', 'cbx', 'cc', 'ccp', 'cdc', 'cdf', 'ceylon', 'cfm', 'cfml', 'cgi', 'cginc', 'ch', 'chem', 'chpl', 'cil', 'circom', 'cirru', 'cj', 'cjs', 'cjsx', 'ck', 'cl', 'cl2', 'clar', 'click', 'clj', 'cljc', 'cljs', 'cljscm', 'cljx', 'clp', 'cls', 'clue', 'clw', 'cmake', 'cmd', 'cnc', 'cob', 'cobol', 'cocci', 'coffee', 'command', 'cp', 'cpp', 'cppm', 'cpy', 'cql', 'cr', 'cs', 'csh', 'csl', 'csx', 'ctp', 'cts', 'cu', 'cue', 'cuh', 'curry', 'cw', 'cxx', 'cy', 'cyp', 'cypher', 'd', 'd2', 'dart', 'das', 'dats', 'dcl', 'ddl', 'decls', 'dfm', 'dfy', 'dhall', 'di', 'djs', 'dlm', 'dm', 'do', 'doh', 'dpr', 'druby', 'dsp', 'dtx', 'duby', 'dwl', 'dyalog', 'dyl', 'dylan', 'e', 'ec', 'ecl', 'eclxml', 'ect', 'edgeql', 'eh', 'ejs', 'eliom', 'eliomi', 'elm', 'elv', 'em', 'eps', 'epsi', 'erl', 'es', 'es6', 'escript', 'esdl', 'ex', 'exs', 'eye', 'f', 'f77', 'factor', 'fan', 'fbs', 'fcgi', 'feature', 'fir', 'fish', 'flex', 'flix', 'flux', 'fnl', 'for', 'forth', 'fp', 'fpp', 'fr', 'frag', 'frg', 'frm', 'frt', 'fs', 'fsh', 'fshader', 'fst', 'fsti', 'fth', 'ftl', 'ftlh', 'fut', 'fx', 'fxh', 'fy', 'g', 'g4', 'gaml', 'gap', 'gawk', 'gco', 'gcode', 'gd', 'gemspec', 'geo', 'geom', 'gi', 'gleam', 'glf', 'glsl', 'glslf', 'glslv', 'gms', 'gn', 'gni', 'gnu', 'gnuplot', 'go', 'god', 'golo', 'gp', 'gql', 'grace', 'graphql', 'graphqls', 'groovy', 'grt', 'gs', 'gshader', 'gst', 'gsx', 'gtpl', 'gvy', 'gyp', 'gypi', 'h', 'h++', 'ha', 'hack', 'haml', 'hats', 'hb', 'hbs', 'hc', 'hcl', 'hh', 'hhi', 'hic', 'hip', 'hlean', 'hlsl', 'hlsli', 'hocon', 'hoon', 'hpp', 'hqf', 'hql', 'hrl', 'hs', 'hs-boot', 'hsc', 'hta', 'hx', 'hxsl', 'hxx', 'hy', 'i', 'i3', 'i7x', 'ice', 'iced', 'icl', 'idc', 'idr', 'ig', 'ihlp', 'ijs', 'ik', 'ily', 'imba', 'inc', 'ink', 'inl', 'ino', 'ins', 'intr', 'io', 'iol', 'ipp', 'ispc', 'iuml', 'ixx', 'j', 'j2', 'jac', 'jade', 'jai', 'jake', 'janet', 'jav', 'java', 'jbuilder', 'jcl', 'jflex', 'jinja', 'jinja2', 'jl', 'jq', 'js', 'jsb', 'jscad', 'jsfl', 'jsh', 'jslib', 'jsm', 'jsonnet', 'jspre', 'jss', 'jst', 'jsx', 'just', 'k', 'kdl', 'kid', 'kit', 'kk', 'kojo', 'kql', 'krl', 'ks', 'ksh', 'ksy', 'kt', 'ktm', 'kts', 'kv', 'l', 'las', 'lasso', 'lasso8', 'lasso9', 'latte', 'lbx', 'lean', 'leo', 'less', 'lex', 'lfe', 'lgt', 'lid', 'lidr', 'linq', 'liq', 'liquid', 'lisp', 'lkml', 'll', 'lmi', 'logtalk', 'lol', 'lookml', 'lp', 'lpr', 'ls', 'lsl', 'lslp', 'lsp', 'ltx', 'lua', 'luau', 'lvclass', 'lvlib', 'lvproj', 'ly', 'm', 'm2', 'm3', 'm4', 'ma', 'mako', 'man', 'mao', 'marko', 'mata', 'matah', 'matlab', 'mawk', 'maxhelp', 'maxpat', 'maxproj', 'mbt', 'mc', 'mcr', 'mdoc', 'mdx', 'me', 'mermaid', 'metal', 'metta', 'mg', 'minid', 'mint', 'mir', 'mirah', 'mjs', 'mkii', 'mkiv', 'mkvi', 'ml', 'ml4', 'mli', 'mligo', 'mlir', 'mll', 'mly', 'mm', 'mmd', 'mo', 'mod', 'mojo', 'monkey', 'monkey2', 'moo', 'moon', 'move', 'mq4', 'mq5', 'mqh', 'mrc', 'ms', 'mspec', 'mt', 'mts', 'mu', 'mud', 'muf', 'mumps', 'muse', 'mustache', 'mxt', 'mysql', 'mzn', 'n', 'nas', 'nasl', 'nasm', 'nawk', 'nb', 'nbp', 'nc', 'ncl', 'ne', 'nearley', 'ned', 'neon', 'nf', 'ni', 'nim', 'nimble', 'nimrod', 'nims', 'nit', 'nix', 'njk', 'njs', 'nl', 'nlogo', 'nomad', 'nqp', 'nr', 'nse', 'nsh', 'nsi', 'nss', 'nu', 'nut', 'ob2', 'odin', 'ol', 'omgrofl', 'ooc', 'opa', 'opal', 'opencl', 'orc', 'owl', 'ox', 'oxh', 'oxo', 'oxygene', 'oz', 'p', 'p4', 'p6', 'p6l', 'p6m', 'p8', 'pac', 'pact', 'pan', 'parrot', 'pas', 'pascal', 'pat', 'pb', 'pbi', 'pbt', 'pd', 'pd_lua', 'pddl', 'pde', 'pep', 'perl', 'pfa', 'ph', 'php', 'php3', 'php4', 'php5', 'phps', 'phpt', 'pic', 'pike', 'pkl', 'pl', 'pl6', 'plantuml', 'plot', 'plt', 'plx', 'pm', 'pm6', 'pml', 'pmod', 'podspec', 'pogo', 'polar', 'pony', 'por', 'pp', 'pprx', 'praat', 'prawn', 'prc', 'prg', 'pri', 'pro', 'prolog', 'prw', 'ps', 'ps1', 'psc', 'psd1', 'psgi', 'psm1', 'pug', 'puml', 'purs', 'pwn', 'pxd', 'pxi', 'py', 'py3', 'pyde', 'pyi', 'pyp', 'pyt', 'pyw', 'pyx', 'q', 'qasm', 'qbs', 'qc', 'ql', 'qll', 'qml', 'qs', 'r', 'r2', 'r3', 'rabl', 'rake', 'raku', 'rakumod', 'rb', 'rbbas', 'rbfrm', 'rbi', 'rbmnu', 'rbres', 'rbtbar', 'rbuild', 'rbw', 'rbx', 'rbxs', 'rchit', 'rd', 're', 'reb', 'rebol', 'red', 'reds', 'reek', 'rei', 'res', 'resi', 'resource', 'rex', 'rexx', 'ring', 'rkt', 'rktd', 'rktl', 'rl', 'rmiss', 'rnh', 'rno', 'robot', 'roc', 'rockspec', 'roff', 'ron', 'rpgle', 'rpy', 'rq', 'rs', 'rsc', 'rsh', 'rsx', 'ru', 'ruby', 'rviz', 's', 'sage', 'sagews', 'sail', 'sas', 'sass', 'sats', 'sbatch', 'sbt', 'sc', 'scad', 'scala', 'scd', 'sce', 'scenic', 'sch', 'sci', 'scm', 'scpt', 'scrbl', 'sdc', 'sed', 'self', 'sh', 'shader', 'shen', 'sieve', 'sj', 'sjs', 'sl', 'slang', 'sld', 'slim', 'slint', 'sls', 'slurm', 'sma', 'smali', 'smithy', 'smk', 'sol', 'sp', 'sparql', 'spec', 'sps', 'sqf', 'sql', 'sqlrpgle', 'sra', 'sru', 'srw', 'ss', 'ssjs', 'st', 'stan', 'star', 'sthlp', 'story', 'sty', 'styl', 'sv', 'svelte', 'svh', 'sw', 'swg', 'swift', 'swig', 'syntax', 't', 'tab', 'tac', 'tact', 'tcc', 'tcl', 'tcsh', 'tea', 'tesc', 'tese', 'tex', 'texi', 'texinfo', 'tf', 'tfvars', 'thor', 'thrift', 'thy', 'tl', 'tlv', 'tm', 'tmac', 'tmux', 'toc', 'tofu', 'toit', 'toml', 'tool', 'tpl', 'tpp', 'trigger', 'ts', 'tsp', 'tst', 'ttl', 'tu', 'twig', 'txi', 'txl', 'txx', 'typ', 'uc', 'udf', 'udo', 'ur', 'urs', 'v', 'vala', 'vapi', 'vark', 'vb', 'vba', 'vbhtml', 'vbs', 'vcl', 'veo', 'vert', 'vh', 'vhd', 'vhdl', 'vhf', 'vhi', 'vho', 'vhs', 'vht', 'vhw', 'viw', 'volt', 'vrx', 'vs', 'vsh', 'vshader', 'vy', 'w', 'wast', 'wat', 'watchr', 'wdl', 'webidl', 'wgsl', 'whiley', 'wisp', 'wl', 'wlk', 'wls', 'wlt', 'wlua', 'workflow', 'wren', 'wsgi', 'x', 'x10', 'xc', 'xdc', 'xht', 'xhtml', 'xi', 'xm', 'xpl', 'xproc', 'xpy', 'xq', 'xql', 'xqm', 'xquery', 'xqy', 'xrl', 'xs', 'xsh', 'xsjs', 'xsjslib', 'xsl', 'xslt', 'xtend', 'y', 'yacc', 'yang', 'yap', 'yar', 'yara', 'yrl', 'yul', 'yy', 'zeek', 'zep', 'zig', 'zil', 'zimpl', 'zmpl', 'zpl', 'zs', 'zsh')
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
WHERE rk <= 2
ORDER BY extension, rk;
