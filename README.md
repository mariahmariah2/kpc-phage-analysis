# KPC phage analysis

Dry-lab (in silico) study of genomic predictors of bacteriophage susceptibility in carbapenemase-producing Kenyan *Klebsiella pneumoniae*, and a structure-based design for a dual-receptor-binding phage protein.

> **Status:** computational work only. No constructs have been synthesised or tested in the lab.

## Background

No confirmed KPC-positive Kenyan *K. pneumoniae* genome exists in the public record, so the project is framed around carbapenemase-producing *K. pneumoniae* broadly (Kenyan NDM-1/OXA-181 isolates). A comparison against global KPC lineages (e.g. ST258, ST11) was planned but has not been carried out.

## What was done

1. **Genomic screening.** Kleborate was run on the Muraya et al. 2022 Kenyan genomes (BioProject PRJNA777842). After removing GCA/GCF duplicates (89 unique genomes) and filtering to true *K. pneumoniae* (69 isolates), 2 carbapenemase-positive isolates were found, both ST147/KL64:
   - NDM-1 isolate (GCF_024990975.1): intact KL64 capsule, OmpK35 disrupted, O2α antigen
   - OXA-181 isolate (GCA_024991015.1): KL64 genotype but capsule-null, OmpK35 and OmpK36 both disrupted, O2α antigen
   - No KPC was found.
2. **Literature and sequence retrieval.** KL64-targeting depolymerase P510dep (GenBank MT966872, ORF38) and the dual receptor-binding protein system of phage vB_KpnP_ZX1 (MW722080), whose auxiliary protein ORF59 carries a Q777 site linked to recognition of capsule-deficient mutants. Protein sequences were retrieved from NCBI and verified; Q777R and Q777K mutants were generated.
3. **Structure prediction.** AlphaFold Server (AlphaFold 3) predictions for P510dep, ZX1 ORF59 (wild type), and chimeric constructs.
4. **Domain analysis.** Domain boundaries were derived from PAE plots. Whole-chain alignment was uninformative, and sequence-independent `cealign` of the two binding domains showed they do not share a common fold, so a direct domain swap is not supported.
5. **Chimeric design.** P510dep (1017 aa) + flexible GGGGS x3 linker + ORF59 Q777R C-terminal domain (residues 770-843) = 1106 aa, following the modular receptor-binding-protein engineering approach described for *Klebsiella* phages. An earlier build used the wild-type ORF59 domain and was corrected to the Q777R mutant; the corrected construct predicted as two independent domains.

## Limitations

- All structures are single-chain predictions; *Klebsiella* depolymerases typically function as homotrimers, which these do not capture.
- The design targets capsule (KL64) and O-antigen (O2α). These are not the carbapenem-resistance mechanisms in these isolates (NDM-1/OXA-181 enzymes and porin loss), so the design is aimed at host range, not at reversing resistance.
- The analysis rests on two carbapenemase-positive isolates from one dataset.
- A set of 15 Western Kenya isolates (Dinda et al. 2024) and a training-exercise dataset (PRJNA915250) have been identified but not analysed.

## Next phase

Design for true resistance reversal (phage steering): choose a receptor mechanistically coupled to carbapenem resistance, so that escaping the phage costs the bacterium its resistance.

## Repository layout

| Path | Contents |
|---|---|
| `scripts/` | `clean_kleborate_results.py` (dedupe, filter, summarise Kleborate output), `plot_pae.py` (PAE heatmaps) |
| `results/` | Kleborate output and `muraya_clean_summary.csv` |
| `data/phage_sequences/` | Small FASTA files: P510dep, ZX1 ORF59 (wild type, Q777R, Q777K), chimeras |
| `data/structures/` | Top-ranked AlphaFold models and PAE data, plus PAE plots |

Large genome downloads under `data/` are not tracked.

## Structure files

Only the top-ranked model (`*_model_0.cif`) and its PAE data (`*_full_data_0.json`) are tracked for each construct. The other four ranked models are not in this repository.

| Folder | Construct |
|---|---|
| `fold_p510dep_orf` | P510dep (KL64 depolymerase, ORF38) |
| `fold_zx1_orf59` | ZX1 ORF59, wild type |
| `fold_chimere_p510_and_zx` | First chimera (wild-type ORF59 C-terminal domain). **Superseded.** |
| `fold_chimera_p510dep_orf59q777r` | Corrected chimera (ORF59 Q777R C-terminal domain). **Current design.** |

## Tools

Conda environment (Python 3.10) with Kleborate v3.2.4, Kaptive v3.2.2, BLAST v2.17.0, AMRFinderPlus v4.2.7, samtools v1.24, bcftools v1.24, minimap2 v2.31; NCBI datasets CLI v18.37.0; PyMOL v3.1.8 (open-source build); AlphaFold Server (AlphaFold 3, Google DeepMind, non-commercial terms; Abramson et al., Nature 2024).
