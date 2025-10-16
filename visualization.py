import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


class EarthquakeVisualizer:
    def __init__(self, connector):
        self.db = connector
        plt.style.use('seaborn-v0_8-whitegrid')
    
    def plot_magnitude_histogram(self, bins=20):
        df = self.db.fetch_all()
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

        region_palette = sns.color_palette("Set3", n_colors=df['region'].nunique())
        region_labels = df['region'].dropna().unique()
        
        source_palette = sns.color_palette("Set2", n_colors=df['source'].nunique())
        source_labels = df['source'].dropna().unique()

        sns.histplot(
            data=df,
            x='magnitude',
            hue='region',
            bins=bins,
            kde=True,
            multiple='stack',
            palette=region_palette,
            alpha=0.7,
            ax=ax1
        )
        ax1.set_title('By Region', fontsize=14, fontweight='bold', pad=20)
        ax1.set_xlabel('Magnitude', fontsize=12)
        ax1.set_ylabel('Count', fontsize=12)
        ax1.grid(True, alpha=0.3)
        
        ax1.legend(
            labels=region_labels,
            bbox_to_anchor=(1.05, 1),
            loc='upper left',
            fontsize=9,
            title="Region"
        )
        
        sns.histplot(
            data=df,
            x='magnitude',
            hue='source',
            bins=bins,
            kde=True,
            multiple='stack',
            palette=source_palette,
            alpha=0.7,
            ax=ax2
        )
        ax2.set_title('By Source', fontsize=14, fontweight='bold', pad=20)
        ax2.set_xlabel('Magnitude', fontsize=12)
        ax2.set_ylabel('Count', fontsize=12)
        ax2.grid(True, alpha=0.3)
            
        ax2.legend(
            labels=source_labels,
            bbox_to_anchor=(1.05, 1),
            loc='upper left',
            fontsize=9,
            title="Source"
        )

        plt.tight_layout()
        fig.suptitle('Earthquake Magnitude Distribution', fontsize=16, fontweight='bold', y=1.02)
        plt.show()