import pandas as pd

df = pd.read_csv("results/muraya_kleborate/klebsiella_pneumo_complex_output.txt", sep="\t")

print(f"Total rows (including duplicates and non-K.pneumoniae): {len(df)}")

df["assembly_id"] = df["strain"].str.replace(r"^(GCA|GCF)_", "", regex=True)

df["is_refseq"] = df["strain"].str.startswith("GCF")
df_sorted = df.sort_values("is_refseq", ascending=False)
df_dedup = df_sorted.drop_duplicates(subset="assembly_id", keep="first")

print(f"After deduplication: {len(df_dedup)}")

species_col = "enterobacterales__species__species"
df_kpneumo = df_dedup[df_dedup[species_col] == "Klebsiella pneumoniae"].copy()

print(f"After filtering to K. pneumoniae only: {len(df_kpneumo)}")

cols_of_interest = {
    "strain": "strain",
    "klebsiella_pneumo_complex__mlst__ST": "ST",
    "klebsiella_pneumo_complex__kaptive__K_locus": "K_locus",
    "klebsiella_pneumo_complex__kaptive__K_type": "K_type",
    "klebsiella_pneumo_complex__kaptive__K_locus_confidence": "K_confidence",
    "klebsiella_pneumo_complex__kaptive__O_locus": "O_locus",
    "klebsiella_pneumo_complex__kaptive__O_type": "O_type",
    "klebsiella_pneumo_complex__amr__Omp_mutations": "Omp_mutations",
    "klebsiella_pneumo_complex__amr__Bla_Carb_acquired": "Carbapenemase_genes",
    "klebsiella_pneumo_complex__amr__Bla_ESBL_acquired": "ESBL_genes",
    "klebsiella_pneumo_complex__resistance_score__resistance_score": "resistance_score",
    "klebsiella_pneumo_complex__virulence_score__virulence_score": "virulence_score",
}
summary = df_kpneumo[list(cols_of_interest.keys())].rename(columns=cols_of_interest)

summary["has_carbapenemase"] = summary["Carbapenemase_genes"].apply(
    lambda x: False if pd.isna(x) or x == "-" else True
)

summary.to_csv("results/muraya_clean_summary.csv", index=False)
print("\nSaved: results/muraya_clean_summary.csv")

print("\n=== Carbapenemase-positive isolates ===")
carb_positive = summary[summary["has_carbapenemase"]]
print(carb_positive[["strain", "ST", "K_locus", "Carbapenemase_genes"]].to_string(index=False))

print(f"\nTotal carbapenemase-positive: {len(carb_positive)} / {len(summary)}")

print("\n=== KL type distribution (top 10) ===")
print(summary["K_locus"].value_counts().head(10))
