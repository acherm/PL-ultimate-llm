# Samples with aspirational provenance

*Generated 2026-05-16 from `data/derived/swh_sample_verification.csv`.*

These 28 samples have **verified content** (`swh:1:cnt:<sha1>` is known
to SWH) but the qualified SWHID's `;origin=` qualifier points at a URL
SWH has never crawled. For 10 of the 28, the `;anchor=<rev>` qualifier
is also unverifiable. The bytes themselves are real, in SWH, and
citable by their bare content SWHID — but the provenance pointer that
makes the qualified SWHID a *complete* citation is not.

See [`SOURCES_AND_SWH_EVIDENCE.md`](SOURCES_AND_SWH_EVIDENCE.md) §8
for the methodology and the strong-vs-weak guarantee discussion.

## When this matters

- **Citing the bare content SWHID (`swh:1:cnt:<sha1>`)** — fine, the
  bytes are archived.
- **Citing the qualified SWHID with `;origin=` and `;anchor=`** — the
  qualifiers may misrepresent reality. SWH never crawled that URL or
  that commit; we're asserting context that the archive cannot back up.

## What to do

Three options, none of them urgent (the bytes still exist):

1. **Strip the qualifiers** on display when origin verification fails
   — fall back to the bare content SWHID + a note "origin not yet in
   SWH archive". The sample stays useful as evidence; the citation
   stays honest.
2. **Replace the origin** for samples whose anchor commit IS known
   (the 18 ori=no/rev=yes cases): if SWH has the revision via some
   *other* origin (fork, mirror), point at that origin instead. Needs
   a small lookup script.
3. **Regenerate via a SWH-native pipeline** when one lands — these
   samples are the natural first batch to replace.

## The 28 samples

Columns:
- `sample_path` relative to `samples/`
- `pl_id` taxonomy slot
- `sha1_git[:12]` content prefix
- `origin` the URL SWH does not know
- `anchor` the commit SHA prefix; `(yes)` if the commit is in SWH
  through some other origin, `(no)` if SWH doesn't have the commit at
  all

| sample_path | pl_id | sha1_git[:12] | origin (ori=no) | anchor (rev_known) |
|---|---|---|---|---|
| pl/bitbake/ec5efcd408dc00e481bb3a83a5b7a27709717bcd/metadata.json | pl/bitbake | ec5efcd408dc | https://github.com/yinbaiyuan/houzzkit-f1-opensource | 526de23e1e0f (no) |
| pl/firrtl/611ef9260fcdd91631d3859f0df075640bf02fb6/metadata.json | pl/firrtl | 611ef9260fcd | https://github.com/comparch-security/chipyard-random-llc | fa843cfd41a5 (no) |
| pl/firrtl/bd215be4eb34ddf0755025738283e228b174318e/metadata.json | pl/firrtl | bd215be4eb34 | https://github.com/comparch-security/chipyard-random-llc | fa843cfd41a5 (no) |
| pl/fortran/7629668e705c792bea37e726af0d79485d54bdc3/metadata.json | pl/fortran | 7629668e705c | https://github.com/Dhondtguido/CalculiX | 350e9c8352c8 (yes) |
| pl/go/aa559990f2685f2948216ba141a2068b0cdae9db/metadata.json | pl/go | aa559990f268 | https://github.com/0chain/zs3server | 069432566fcf (yes) |
| pl/jinja/d213448489b446f0e04b18616ad1213b2d6888ca/metadata.json | pl/jinja | d213448489b4 | https://github.com/Grokci/XRP_examples | 3ec8718b46cc (yes) |
| pl/linear-programming/cf7098be2e4d58ab2d6ae2068be4875f1ba42034/metadata.json | pl/linear-programming | cf7098be2e4d | https://github.com/summerspringwei/dataflow-scheduler | a459902eab14 (no) |
| pl/liquid/08306719ad8e6da390500976d2651c4435ec9937/metadata.json | pl/liquid | 08306719ad8e | https://github.com/outtable/confuse-9live | e261c788a510 (no) |
| pl/lookml/6c487f969c9820fffece9b82d9005746237eafcd/metadata.json | pl/lookml | 6c487f969c98 | https://github.com/looker-open-source/block-cortex-sap | d5d40f77b75b (yes) |
| pl/lsl/19ad7048a33e175737297b11dc0988d3826b364d/metadata.json | pl/lsl | 19ad7048a33e | https://github.com/holoneon/opensim-tranquillity-work | 7f6d27525122 (yes) |
| pl/lsl/b4ab5327b8144eca32858e3cb56cf81c91751752/metadata.json | pl/lsl | b4ab5327b814 | https://github.com/holoneon/opensim-tranquillity-work | 7f6d27525122 (yes) |
| pl/m4/e6c87cf5b0559c2058e1ba0dc1d796438c987047/metadata.json | pl/m4 | e6c87cf5b055 | https://github.com/corretto/corretto-17 | ef0f693065ed (yes) |
| pl/r/bf10fdf1440169ad1bbf15c9f7494a7f5e839f85/metadata.json | pl/r | bf10fdf14401 | https://github.com/Blue-Matter/MSEtool | f7f6738f2899 (yes) |
| pl/racket/ae72bd2260068f100a04f3bf67208da1045e4745/metadata.json | pl/racket | ae72bd226006 | https://github.com/jeapostrophe/blog-source | c637f9fe7b27 (yes) |
| pl/scilab/90e47e9d1844fd51459f905c132f0bb05f933365/metadata.json | pl/scilab | 90e47e9d1844 | https://github.com/cyclist-org/cyclist | 03fd40efbd97 (yes) |
| pl/scilab/e1aafeea1260089d10ad4a2a77fdfc6502717fbb/metadata.json | pl/scilab | e1aafeea1260 | https://github.com/cyclist-org/cyclist | 03fd40efbd97 (yes) |
| pl/shaderlab/0e1d66248b50ecf9234f421147102e40487c394e/metadata.json | pl/shaderlab | 0e1d66248b50 | https://github.com/Superppig/Ghost-Doc | 388457b96ab6 (yes) |
| pl/slash/b0edbed91284fe8c2791b7eb17b145ffc8893c2c/metadata.json | pl/slash | b0edbed91284 | https://github.com/jedsoft/jed | aaae6ecd2f04 (yes) |
| pl/yara/afdcfbc6432b04570faf777c62270a41e93ef049/metadata.json | pl/yara | afdcfbc6432b | https://github.com/rivitna/Malware | eda0c3083fd9 (yes) |
| unclassified/0347deaac2990d7ea12cc2a8a49b3bdb711d371f/metadata.json | unclassified | 0347deaac299 | https://github.com/tessarakkt/godot4-oceanfft | de057b68d0f2 (yes) |
| unclassified/053e745d27b0e435d81d9de06db5311594dd65b0/metadata.json | unclassified | 053e745d27b0 | https://github.com/Lind-Project/lind-wasm | 5be4c7e80c3e (no) |
| unclassified/1d5bbf4dab8220f8e5eb83ccb3b2d598b52cf264/metadata.json | unclassified | 1d5bbf4dab82 | https://github.com/opengauss-mirror/spq_plugin_v2 | f3e566678b27 (no) |
| unclassified/52346839c68d26458bb9ad34b3898586d6127aca/metadata.json | unclassified | 52346839c68d | https://github.com/theaifutureguy/AI-Chatbot-for-Lawyer | f4ecc4921913 (no) |
| unclassified/67e093f3ddd12d5059fc29462e5b64848d601fc1/metadata.json | unclassified | 67e093f3ddd1 | https://github.com/dshawshank/Blender-android_arm64 | b626f1fd18e9 (yes) |
| unclassified/b8d32bd2c542a3ae97a5d50840f0aac0f33d170b/metadata.json | unclassified | b8d32bd2c542 | https://github.com/niteshCopado/PartnerProduction | 925a58eef8de (no) |
| unclassified/d39353d8fae1f25692c551ff6c50a9416dee3c0e/metadata.json | unclassified | d39353d8fae1 | https://github.com/Lind-Project/lind-wasm | 5be4c7e80c3e (no) |
| unclassified/d6c8353da42015c26f04840a392fdad083dd3905/metadata.json | unclassified | d6c8353da420 | https://github.com/dshawshank/Blender-android_arm64 | c8b5b17d40c4 (yes) |
| unclassified/f68977ea3046e8b1afbe3cb58bc4c4d551d9573c/metadata.json | unclassified | f68977ea3046 | https://github.com/spcorcor18/LPO-8852 | f3f6500f030e (yes) |

## Regenerating this list

```bash
python3 tools/verify_swh_samples.py --check-origins         # rerun
# then regenerate this table from the CSV; the section above is built by:
python3 -c "
import csv, re
ori_re = re.compile(r';origin=([^;]+)')
anc_re = re.compile(r';anchor=(swh:1:rev:[0-9a-f]{40})')
with open('data/derived/swh_sample_verification.csv') as f:
    rows = list(csv.DictReader(f))
rs = [r for r in rows if r['ori_known'] == 'no']
print(f'Total: {len(rs)}')
for r in sorted(rs, key=lambda x: (x['pl_id'], x['sha1_git'])):
    om = ori_re.search(r['qualified_swhid'])
    am = anc_re.search(r['qualified_swhid'])
    origin = om.group(1) if om else '-'
    anchor = (am.group(1)[len('swh:1:rev:'):][:12] if am else '-')
    print(f'| {r[\"sample_path\"]} | {r[\"pl_id\"]} | {r[\"sha1_git\"][:12]} | {origin} | {anchor} ({r[\"rev_known\"]}) |')
"
```
