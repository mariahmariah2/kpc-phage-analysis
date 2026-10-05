# Genomic Predictors of Phage Susceptibility and In-Silico Chimeric Phage Engineering in Kenyan Carbapenemase-Producing *Klebsiella pneumoniae*

**Project repository:** github.com/mariahmariah2/kpc-phage-analysis

---

## 1. Background and Rationale

Carbapenemase-producing *Klebsiella pneumoniae* (CRKP) is a critical antimicrobial resistance threat, and bacteriophage therapy is an increasingly promising adjunct to antibiotics against such strains. However, phage host range is governed primarily by bacterial surface genomics — capsule type, outer membrane porin integrity, and anti-phage defense systems — not by which carbapenemase a strain carries. No prior study had characterized these phage-susceptibility-relevant genomic features in Kenyan CRKP isolates specifically, despite local groups having already isolated and genomically characterized candidate therapeutic phages against Kenyan CRKP.

**Note on scope:** this project originally targeted *bla*KPC-producing isolates specifically. A review of the published Kenyan AMR genomics literature (Musila et al. 2021; Muraya et al. 2022; Dinda et al. 2024) found no confirmed *bla*KPC-positive *K. pneumoniae* genome reported from Kenya to date — the carbapenemase burden in Kenya is dominated by *bla*NDM-1 and *bla*OXA-181. The project scope was accordingly reframed to carbapenemase-producing *K. pneumoniae* broadly.

---

## 2. Genomic Screening

**Data source:** Muraya et al. (2022), BioProject PRJNA777842, 130 genome assemblies (GenBank/RefSeq).

**Method:** Genomes were typed using Kleborate v3.2.4 (`--preset kpsc`), which reports species confirmation, MLST sequence type, capsule (KL) and O-antigen locus typing (via Kaptive), and acquired AMR gene content. GCA/RefSeq duplicate pairs were removed in Python/pandas (RefSeq entries retained preferentially).

**Results:**
- 130 assemblies → 89 unique genomes after deduplication → 69 confirmed true *K. pneumoniae* (remainder: *K. variicola*, *K. quasipneumoniae*).
- Capsule (KL) type diversity was high across the 69 isolates; no single KL type dominated (most common: KL2 and KL25, 5 isolates each).
- Only **2 isolates (2.9%)** carried an acquired carbapenemase gene:

| Isolate | ST | Carbapenemase | KL locus | Capsule phenotype | Porin status | O-type |
|---|---|---|---|---|---|---|
| GCF_024990975.1 | ST147 | *bla*NDM-1 | KL64 | Typeable (intact) | OmpK35 disrupted | O2α |
| GCA_024991015.1 | ST147-1LV | *bla*OXA-181 | KL64 | **Capsule-null** | OmpK35 + OmpK36 disrupted | O2α |

Both isolates also carried *bla*CTX-M-15 (ESBL). No *bla*KPC was detected in any isolate.

**Interpretation:** the two carbapenemase-positive isolates share capsule locus KL64 and O-antigen type O2α but differ critically in actual capsule expression — one presents a normal, typeable KL64 capsule; the other, despite carrying the same KL64 genotype, is phenotypically capsule-null. This divergence, within an otherwise closely related pair (same ST, same KL, same O-type), became the central problem the rest of this project addresses: a capsule-targeting phage strategy that works for one isolate should be expected to fail for the other.

---

## 3. Literature-Derived Phage Candidates

**KL64-targeting depolymerase:** P510dep (phage P510; GenBank MT966872; protein QOV05454.1, annotated "tail fibers protein," ORF38, 1017 aa) is a characterized depolymerase active against KL64-type capsules. Closely related, near-identical depolymerases (Dep37, phage vB_KpnP_IME1309, 97.25% identity; K64-ORF41, phage SH-KP152410) confirm KL64 depolymerase activity is a recurring, conserved phage strategy.

**Critical constraint identified:** published host-range data for phage SH-KP152410 (testing its depolymerase, K64-ORF41, against 48 KL64-genotype strains) showed that strains which were KL64-genotype but capsule-negative (8/48) were **not** lysed or haloed — i.e., depolymerase phages fail against capsule-null escape variants. This directly predicts that the Muraya OXA-181 isolate (KL64 genotype, capsule-null) would resist a standard KL64-depolymerase phage, while the NDM-1 isolate (KL64 genotype, intact capsule) should remain a viable target.

**Resistance-escape precedent:** phage vB_KpnP_ZX1 (GenBank MW722080) was found to use a dual receptor-binding protein (RBP) system against *K. pneumoniae* 111-2: a primary, capsule-targeting RBP (ORF60) and an auxiliary "backup" RBP, ORF59 (protein QTH79845, 843 aa, annotated as an endoglucanase-family protein). Under selective pressure, host strains evolved capsule-loss resistance (via disruption of *wbaP*, *wbaZ*, or *wzc* — capsule synthesis genes) — directly analogous to the Muraya OXA-181 isolate's capsule-null phenotype. In response, phage progeny carrying a point mutation in ORF59 at residue 777 (Q777R or Q777K) gained the ability to recognize an alternative, O-antigen-associated binding site, restoring infectivity against the capsule-escape mutants (Zhang et al., PMC11795761).

**Design rationale:** both Muraya carbapenemase-positive isolates share O-antigen type O2α regardless of capsule status, making O-antigen-directed binding a genomically grounded, isolate-matched alternative target for the capsule-null OXA-181 isolate specifically.

---

## 4. Sequence Retrieval and Mutant Construction

Protein sequences were retrieved directly from NCBI (`efetch`, `fasta_cds_aa` format, via `curl`) for MT966872 and MW722080. ORF identities were confirmed against source-paper descriptions:
- **P510dep** = ORF38 = protein QOV05454.1, 1017 aa (confirmed by matching annotation and literature-reported ORF number).
- **ORF59** = protein QTH79845, 843 aa, confirmed by cross-checking against the paper's explicitly stated length (843 aa) and residue 777 identity (Q, glutamine) — verified by direct sequence indexing.

Two point-mutant ORF59 sequences were generated in Python by direct string substitution at position 777: **Q777R** and **Q777K**, both confirmed correct by direct residue inspection post-mutation.

---

## 5. Structural Prediction

Structures were predicted using **AlphaFold Server** (Google DeepMind, AlphaFold 3, non-commercial use; Abramson et al., *Nature*, 2024). ColabFold/AlphaFold2 (Google Colab) was attempted initially but abandoned after repeated runtime disconnects caused loss of in-progress results; it was retained as a parallel backup for longer jobs.

Single-chain predictions were obtained for:
- P510dep (1017 aa) — full-length
- ZX1 ORF59, wild-type (843 aa) — full-length

---

## 6. Domain Boundary Identification (PAE Analysis)

Exact residue-level domain boundaries were not reported in the primary literature for P510dep. Rather than assume boundaries, they were derived directly from AlphaFold's own output: the **Predicted Aligned Error (PAE)** matrix for each structure was extracted and plotted as a heatmap (Python/matplotlib), since independently-folding domains appear as distinct low-error blocks along the diagonal.

**P510dep:** a compact domain spanning approximately **residues 1–230** (consistent with an N-terminal tail-anchor domain), followed by an elongated region (**~230–1017**) showing the diagonal banding pattern characteristic of a repetitive β-helix solenoid fold — the expected architecture for a capsule depolymerase.

**ZX1 ORF59:** several domains, including a distinct, compact C-terminal domain spanning approximately **residues 770–843**, coinciding precisely with the Q777 mutation site reported in the literature.

These data-derived boundaries (P510dep binding domain: 230–1017; ORF59 C-terminal domain: 770–843) were used for all subsequent structural comparisons.

---

## 7. Structural Comparison and Design Correction

**Initial (uninformative) comparison:** whole-chain structural alignment of P510dep and ZX1 ORF59 using PyMOL's `align` command (sequence-guided superposition) produced a high RMSD (35.4 Å). This result was recognized as uninformative: `align` relies on sequence similarity to guide matching, and P510dep and ORF59 are evolutionarily unrelated proteins with no meaningful sequence similarity, so sequence-guided alignment cannot answer a purely structural question.

**Domain-level comparison, corrected method:** restricting the comparison to the data-derived domains (P510dep 230–1017 vs. ORF59 770–843) and using `cealign` — a sequence-independent, shape-based structural alignment — gave **RMSD = 8.45 Å over only 32 of 788 (P510dep) / 74 (ORF59) residues**. This result indicates the two domains do **not** share a common fold: P510dep's binding domain is an elongated β-helix solenoid, while ORF59's C-terminal domain is a compact, globular endoglucanase-family fold. A direct domain-swap or in-place fusion (replacing one domain's fold with the other's) is therefore not structurally supported.

**Revised design, following established precedent:** published work on engineering modular Klebsiella phage RBPs (*mBio*, "Engineering the Modular Receptor-Binding Proteins of Klebsiella Phages Switches Their Capsule Serotype Specificity") demonstrates that these proteins are modular — an N-terminal anchor domain (phage-tail attachment) is functionally separable from a central/C-terminal enzymatic-receptor domain (which determines target specificity) — and that fusing an intact donor receptor domain onto a recipient's anchor domain, connected by a linker, is an established, working engineering method. This does not require the two domains to share a fold; it requires only that each domain fold and present correctly once linked. This architecture also mirrors naturally multivalent phages (e.g., KpS110, which carries five independent tail-spike domains on one phage).

---

## 8. Chimeric Construct Design and Validation

**Construct:** full-length P510dep (1017 aa) + flexible Gly-Ser linker (GGGGS×3, 15 aa) + ZX1 ORF59 **Q777R mutant** C-terminal domain (residues 770–843, 74 aa) = **1106 aa total**.

*(Note: an initial version of this construct was built and folded using the wild-type ORF59 domain rather than the Q777R mutant. Since the wild-type domain lacks the O-antigen-recognition property — this is conferred specifically by the Q777R/K mutation per the source literature — that result demonstrated only that the fusion architecture was structurally viable, not that the attached domain carried the intended function. The construct was corrected to use the Q777R mutant domain, and the structural validation below reflects the corrected, biologically relevant construct.)*

**Structural prediction (AlphaFold Server):** the 1106 aa chimeric construct (P510dep + linker + ORF59-Q777R C-terminal domain) was submitted and successfully predicted.

**PAE validation:** the resulting PAE heatmap for the chimera closely reproduces the domain pattern of the standalone P510dep prediction — the compact N-terminal block (~1–230) and elongated solenoid region (~230–1017) are preserved — with a distinct, separate low-confidence-to-neighbors block at the construct's C-terminus (~1033–1106) corresponding to the attached ORF59-Q777R domain, and elevated error in the linker region (~1018–1032) consistent with the intended flexible, non-rigid connection.

**Visual (PyMOL) validation:** the predicted structure (top-ranked model) was loaded and rendered with domain-specific coloring (P510dep: skyblue; linker: yellow; ORF59-Q777R domain: orange). The ORF59-Q777R domain is clearly visible as a compact, independently-folded unit positioned away from the main P510dep body, connected only via the flexible linker, with no evidence of structural clash or interference between the two domains. P510dep's own characteristic elongated β-helix architecture is fully preserved and visually unchanged from its standalone prediction.

---

## 9. Conclusions

1. Kenyan carbapenemase-producing *K. pneumoniae* genomes (Muraya et al. 2022 dataset) carry *bla*NDM-1 and *bla*OXA-181, not *bla*KPC; both confirmed carbapenemase-positive isolates share KL64 capsule locus and O2α antigen but differ in capsule expression (intact vs. capsule-null).
2. Published KL64-depolymerase phages are predicted, from directly comparable published host-range data, to infect the capsule-intact isolate but fail against the capsule-null isolate.
3. A real, published phage-resistance-evolution precedent (ZX1/ORF59/Q777R) provides a validated, genomically-matched alternative targeting strategy (O-antigen recognition) for the capsule-null isolate.
4. A chimeric receptor-binding protein — P510dep's native capsule-binding domain, linked to the functionally relevant ORF59-Q777R O-antigen-binding domain — was designed and computationally validated (via AlphaFold 3 structural prediction, PAE-based domain analysis, and PyMOL structural visualization) to fold as two independent, non-clashing, properly-presenting binding domains on a single protein.

This constitutes a complete, literature-grounded, data-validated instance of in-silico bacteriophage receptor-binding protein engineering (specifically, synthetic/chimeric tail-fiber modeling via AlphaFold-based structural prediction), positioned within an established and recognized methodology in the phage engineering field.

**Explicitly out of scope / future work:** wet-lab confirmation (gene synthesis, cloning of the chimeric construct into a phage backbone, propagation, and infectivity testing against the two Muraya isolates) would be required to confirm actual biological function. The native oligomeric state of both parent proteins (likely homotrimeric, consistent with other characterized Klebsiella depolymerases) was not modeled; single-chain predictions may not fully capture functional trimeric geometry. Domain-boundary estimates were derived computationally (PAE-based) rather than from published residue-level annotations, as none were available for P510dep specifically.

---

## 10. Proposed Wet-Lab Validation Pathway

The in-silico result establishes structural plausibility only. Confirming that the chimeric receptor-binding protein (RBP) actually functions — folds correctly as a trimer, assembles into a phage particle, and confers the intended dual host range — requires a defined sequence of wet-lab steps. These are outlined below as the project's next phase, in the order they would logically be executed, with the specific mechanism and purpose of each stage made explicit.

### 10.1 Gene synthesis and codon optimization

The chimeric construct's amino acid sequence (`chimera_P510dep_ORF59Q777R_Cterm.fasta`) would be back-translated into a DNA sequence and codon-optimized for expression in *Klebsiella*/*E. coli* (the typical phage propagation host), then ordered from a commercial gene synthesis provider (e.g., Twist Bioscience, GenScript, IDT) as a double-stranded DNA fragment or cloned directly into a delivery plasmid. Codon optimization matters here because P510dep and ZX1 originate in different phage backgrounds, and inefficient codon usage in the host can reduce expression yield independent of whether the protein itself is correctly designed.

### 10.2 Installing the construct into a phage genome

The chimeric gene must replace (or be inserted alongside) the native tail-fiber/RBP gene in a real phage genome — most logically P510 itself, since the construct's backbone (the anchor domain) is P510dep's own native sequence, minimizing disruption to how the protein normally docks onto the phage tail. Two established methods are used for this in current phage engineering practice:

- **BRED (Bacteriophage Recombineering of Electroporated DNA):** host bacteria are engineered to express phage-derived recombination proteins (e.g., λ Red system), then co-electroporated with phage DNA and a linear DNA fragment carrying the chimeric gene flanked by homology arms matching the target locus. Homologous recombination swaps the native gene for the engineered one in a fraction of the resulting phage progeny, which are then screened/selected.
- **CRISPR-Cas-assisted phage engineering:** a CRISPR-Cas system is used to counter-select against unmodified (wild-type) phage genomes during replication, enriching for recombinant phages carrying the desired genomic edit. This is now the more commonly used approach where the counter-selection step substantially reduces the screening burden compared to BRED alone.
- **Yeast-based phage genome assembly** (for larger genomic edits or when working from a synthetic genome rather than native phage DNA): the phage genome is assembled and edited as a yeast artificial chromosome using yeast homologous recombination machinery, then "rebooted" (transformed back into a susceptible bacterial host to reconstitute an infectious phage particle).

Given this project's scale (a single gene-level RBP fusion with intact flanking sequence), BRED or CRISPR-assisted recombineering is the more proportionate and faster route; full genome synthesis/yeast assembly would only be warranted if larger-scale genome edits were planned.

### 10.3 Recombinant phage recovery and verification

Following recombineering, individual plaques are picked and screened by PCR (using primers spanning the edited locus) and Sanger sequencing to confirm the chimeric gene was correctly incorporated in place of (or alongside) the native gene, with no unintended mutations introduced during the editing process. This step is purely confirmatory of genotype — it does not yet establish that the engineered phage is viable or functional.

### 10.4 Phage viability and particle assembly confirmation

The recombinant phage is propagated on a permissive host strain (a KL64-capsule-positive, phage-susceptible *K. pneumoniae* strain, ideally not one of the two target clinical isolates, to avoid conflating "does the phage exist" with "does the phage have the intended new host range"). Successful plaque formation on this permissive host confirms the modified phage is still viable — i.e., that inserting the chimeric RBP did not disrupt essential tail assembly or DNA packaging. Transmission electron microscopy (TEM) can additionally confirm normal particle morphology (intact capsid and tail), ruling out gross assembly defects.

### 10.5 Functional receptor-binding and host-range testing — the core validation step

This is where the actual design hypothesis gets tested, via a set of standard phage microbiology assays, each addressing a specific question:

- **Spot test / plaque assay against both target isolates:** the engineered phage is spotted (or plated at serial dilutions) directly onto lawns of the two Muraya clinical isolates — the NDM-1 (capsule-intact) and OXA-181 (capsule-null) strains. Clearing zones (spots) or discrete plaques indicate successful infection and lysis. The key predicted outcome, if the design works as intended: the engineered phage should lyse **both** isolates, whereas the unmodified parent phage (P510) should lyse only the capsule-intact NDM-1 isolate and fail against the capsule-null OXA-181 isolate. This direct comparison (engineered vs. parental phage, across both isolates) is the single most important experiment in the whole validation pathway, since it directly tests the central claim of the project.
- **Efficiency of plating (EOP):** quantifies infection efficiency as a ratio relative to the permissive host, giving a graded measure of how well the engineered phage infects each target isolate rather than a simple yes/no readout.
- **Adsorption assay:** measures how quickly and completely the phage attaches to each bacterial strain by tracking free (unadsorbed) phage particles in the supernatant over time after mixing phage with bacterial culture. This isolates the specific question of whether receptor binding is occurring, independent of downstream steps like DNA injection or lysis — useful for distinguishing "the new domain isn't binding" from "the new domain binds but something downstream fails."
- **Receptor-blocking/competition assay:** pre-incubating the capsule-null isolate with purified O-antigen (or an O2α-specific antibody) before phage challenge; if the engineered phage's infectivity against this isolate is reduced by O-antigen blocking specifically, this would directly confirm the ORF59-Q777R domain is mediating infection via the intended O-antigen route, rather than through some other, unanticipated mechanism.

### 10.6 Recombinant protein expression and binding confirmation (parallel, lower-cost validation)

As a faster and cheaper complement to building the whole phage, the chimeric RBP gene alone can be expressed recombinantly (e.g., in *E. coli*, with a purification tag) and tested directly for binding to both target isolates — using the same antibody/competition-based adsorption logic the ZX1 paper itself used to validate ORF59's function. This does not require a functioning engineered phage and can be done earlier in the pipeline, potentially before committing to the more involved phage recombineering step, as an early go/no-go checkpoint on whether the designed domain actually binds its intended target at all.

### 10.7 Summary of validation logic

| Stage | Question answered | Method |
|---|---|---|
| Gene synthesis | Can the construct be made? | Commercial synthesis, codon optimization |
| Phage recombineering | Can it be installed into a real phage genome? | BRED or CRISPR-assisted recombineering |
| Genotype verification | Was the edit correct? | PCR + Sanger sequencing |
| Viability/assembly | Does the modified phage still work at all? | Plaque assay on permissive host; TEM |
| Host-range/spot test | Does it infect the capsule-null isolate it was designed for, while retaining activity against the capsule-intact isolate? | Spot test / plaque assay on both clinical isolates, compared against parental phage |
| EOP | How efficiently does it infect each target? | Efficiency of plating |
| Adsorption assay | Is the new domain actually binding? | Free-phage depletion assay |
| Receptor-blocking assay | Is binding specifically via O-antigen, as designed? | Competition with purified O-antigen/antibody |
| Recombinant protein binding (parallel) | Does the isolated chimeric protein bind, independent of whole-phage context? | Expression + binding assay, as an earlier checkpoint |

This pathway moves from "can it be built" through "does it still function as a phage at all" to the specific, decisive test of "does it infect the capsule-null isolate the way the design intended" — with the spot test comparing engineered vs. parental phage against both clinical isolates serving as the single experiment that would most directly confirm or refute this project's central hypothesis.

---

## Appendix: Methods and Tooling

- **Compute environment:** 2019 Intel MacBook Pro, macOS Sequoia. Conda environment `kleborate_env`, managed via Miniforge.
- **Genomics:** Kleborate v3.2.4 (incl. Kaptive v3.2.2), BLAST v2.17.0, bcftools v1.24, samtools v1.24, minimap2 v2.31, ncbi-amrfinderplus v4.2.7, NCBI Entrez Direct.
- **Data retrieval:** NCBI `datasets` CLI v18.37.0 (bulk genome downloads); direct `curl` calls to NCBI eutils `efetch` (`fasta_cds_aa` format) for individual protein sequences (the bundled `edirect` CLI wrapper failed consistently with SSL errors on this machine).
- **Structure prediction:** AlphaFold Server (AlphaFold 3, Google DeepMind; non-commercial terms; cite Abramson et al., *Nature*, 2024). ColabFold/AlphaFold2 (Google Colab) used as a secondary/backup route.
- **Structural analysis:** PyMOL v3.1.8 (open-source feature set only). `cealign` (sequence-independent, shape-based alignment) used in preference to `align` (sequence-guided) for comparing structurally unrelated proteins.
- **Analysis scripts:** Python (pandas, numpy, matplotlib) for Kleborate output cleaning/deduplication and PAE heatmap generation.

**Key data files (repository):**
- `results/muraya_clean_summary.csv` — cleaned, deduplicated Kleborate output
- `data/phage_sequences/P510dep_ORF38.fasta`, `ZX1_ORF59_QTH79845.fasta`, `ZX1_ORF59_Q777R.fasta`, `ZX1_ORF59_Q777K.fasta`
- `data/phage_sequences/chimera_P510dep_ORF59Q777R_Cterm.fasta` — final validated construct
- `data/structures/` — AlphaFold Server prediction outputs and PAE plots
- `scripts/clean_kleborate_results.py`, `scripts/plot_pae.py`
