# Read P510dep full sequence
with open('data/phage_sequences/P510dep_ORF38.fasta') as f:
    p510dep_seq = ''.join(f.read().split('\n')[1:])

# Read ZX1 ORF59 full sequence, extract just the C-terminal domain (770-843)
with open('data/phage_sequences/ZX1_ORF59_QTH79845.fasta') as f:
    orf59_seq = ''.join(f.read().split('\n')[1:])

orf59_cterm_domain = orf59_seq[769:843]  # 0-indexed: residues 770-843

# Flexible glycine-serine linker (GGGGS x3 = 15 residues, standard in protein engineering)
linker = "GGGGSGGGGSGGGGS"

# Build the chimeric construct
chimera = p510dep_seq + linker + orf59_cterm_domain

print(f"P510dep length: {len(p510dep_seq)}")
print(f"ORF59 C-terminal domain length: {len(orf59_cterm_domain)}")
print(f"Linker length: {len(linker)}")
print(f"Total chimera length: {len(chimera)}")

with open('data/phage_sequences/chimera_P510dep_ORF59Cterm.fasta', 'w') as f:
    f.write(">chimera_P510dep_anchor_binding_linker_ORF59Cterm\n")
    f.write(chimera + "\n")

print("Saved: data/phage_sequences/chimera_P510dep_ORF59Cterm.fasta")
