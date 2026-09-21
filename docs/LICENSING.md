# Licensing status and release decision

The existing [LICENSE](../LICENSE) explicitly grants no open-source license. A public
repository alone does not establish permission to reuse or redistribute its source.
BalNLP should be described as working toward an open-source release until the owner
selects a license and confirms rights to contributed and recovered code.

| Material | Current treatment | Required before redistribution |
|---|---|---|
| BalNLP source | License not selected | Owner confirms provenance and chooses a standard license |
| Model/checkpoint files | Separate repositories and terms | Read license at each pinned revision; preserve attribution |
| Training/evaluation datasets | Not licensed by this source repository | Confirm permissions, consent, provenance, and applicable dataset terms |
| Third-party dependencies | Their own licenses | Review notices and distribution obligations |
| BalTokenizer | Separate project; README says unlicensed | Obtain its owner's licensing decision before reuse |

Apache-2.0 is a candidate for owner review because it includes explicit patent terms;
MIT is another common permissive option. This is a proposed release decision, not a
license grant or a determination of third-party rights. Confirm the recovered
BalMorph notebook and BalParser implementation's provenance before granting rights.
No model card license label automatically applies to this application or its datasets.

Once approved: replace the existing notice with the exact chosen license, add correct
copyright attribution, update package metadata and documentation, and review contributor
permissions. Do not include unapproved weights or datasets in a package distribution.
