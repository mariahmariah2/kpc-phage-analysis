import json
import numpy as np
import matplotlib.pyplot as plt

def plot_pae(json_path, title, output_path):
    with open(json_path) as f:
        data = json.load(f)
    pae = np.array(data['pae'])
    
    fig, ax = plt.subplots(figsize=(8, 7))
    im = ax.imshow(pae, cmap='Greens_r', vmin=0, vmax=30)
    ax.set_title(f'Predicted Aligned Error: {title}')
    ax.set_xlabel('Residue')
    ax.set_ylabel('Residue')
    plt.colorbar(im, ax=ax, label='PAE (Å)')
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    print(f"Saved: {output_path}")
    print(f"Matrix shape: {pae.shape}")

plot_pae(
    'data/structures/fold_p510dep_orf/fold_p510dep_orf_full_data_0.json',
    'P510dep (ORF38)',
    'data/structures/P510dep_PAE.png'
)

plot_pae(
    'data/structures/fold_zx1_orf59/fold_zx1_orf59_full_data_0.json',
    'ZX1 ORF59',
    'data/structures/ZX1_ORF59_PAE.png'
)
