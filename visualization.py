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
            labels=region_labels[:10],
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
    
    def plot_time_trends(self):
        df = self.db.fetch_all()
        df['week_period'] = df['time'].dt.to_period('W').dt.start_time
        df['day_period'] = df['time'].dt.to_period('D').dt.start_time
        weekly_df = df.groupby('week_period').agg({'magnitude': 'mean', 'depth': 'count'}).rename(columns={'depth': 'count'})
        daily_df = df.groupby('day_period').agg({'magnitude': 'mean', 'depth': 'count'}).rename(columns={'depth': 'count'})
        
        fig, (ax1, ax3) = plt.subplots(2, 1, figsize=(16, 10))
        colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D']
        
        ax1.plot(weekly_df.index, weekly_df['count'], color=colors[0], linewidth=2, marker='o', markersize=3)
        ax1.set_ylabel('Weekly Count', color=colors[0], fontsize=12, fontweight='bold')
        ax1.tick_params(axis='y', labelcolor=colors[0])
        ax1.tick_params(axis='x', rotation=45)
        ax1.set_title('Weekly Earthquake Trends', fontsize=14, fontweight='bold', pad=20)
        
        ax2 = ax1.twinx()
        ax2.plot(weekly_df.index, weekly_df['magnitude'], color=colors[1], linewidth=2, marker='o', markersize=3)
        ax2.set_ylabel('Average Magnitude', color=colors[1], fontsize=12, fontweight='bold')
        ax2.tick_params(axis='y', labelcolor=colors[1])
        
        ax3.plot(daily_df.index, daily_df['count'], color=colors[2], linewidth=1.5, alpha=0.8)
        ax3.set_ylabel('Daily Count', color=colors[2], fontsize=12, fontweight='bold')
        ax3.tick_params(axis='y', labelcolor=colors[2])
        ax3.tick_params(axis='x', rotation=45)
        ax3.set_title('Daily Earthquake Trends', fontsize=14, fontweight='bold', pad=20)
        ax3.set_xlabel('Date', fontsize=12)
        
        ax4 = ax3.twinx()
        ax4.plot(daily_df.index, daily_df['magnitude'], color=colors[3], linewidth=1.5, alpha=0.8)
        ax4.set_ylabel('Average Magnitude', color=colors[3], fontsize=12, fontweight='bold')
        ax4.tick_params(axis='y', labelcolor=colors[3])
        
        plt.tight_layout()
        plt.show()
    
    def plot_scatter(self):
        df = self.db.fetch_all()
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 10))
        
        sns.scatterplot(
            data=df, 
            x='time', 
            y='magnitude', 
            s=40,
            ax=ax1,
            c='#2E86AB'
        )
        ax1.set_title('Magnitude vs Time', fontsize=14, fontweight='bold', pad=20)
        ax1.set_xlabel('Time', fontsize=12)
        ax1.set_ylabel('Magnitude', fontsize=12)
        ax1.tick_params(axis='x', rotation=45)
        
        sns.scatterplot(
            data=df, 
            x='time', 
            y='depth', 
            s=40,
            ax=ax2,
            c='#A23B72'
        )
        ax2.set_title('Depth vs Time', fontsize=14, fontweight='bold', pad=20)
        ax2.set_xlabel('Time', fontsize=12)
        ax2.set_ylabel('Depth', fontsize=12)
        ax2.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.show()
    
    def plot_box_distribution(self):
        df = self.db.fetch_all()
        df['depth_bin'] = pd.qcut(df['depth'], q=10, duplicates='drop')
        
        fig, ax = plt.subplots(figsize=(16, 8))

        sns.boxplot(data=df, x='depth_bin', y='magnitude', ax=ax, hue="depth_bin", palette='viridis', legend=False)
        
        ax.set_title('Magnitude Distribution by Depth Range', fontsize=14, fontweight='bold', pad=20)
        ax.set_xlabel('Depth Range (km)', fontsize=12)
        ax.set_ylabel('Magnitude', fontsize=12)
        ax.tick_params(axis='x', rotation=45)
        ax.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        plt.show()
    
    def plot_heatmap(self):
        df = self.db.fetch_all()
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        sns.kdeplot(
            data=df,
            x='longitude', y='latitude',
            fill=True, cmap='hot', thresh=0.05,
            ax=ax1, cbar=True
        )
        
        ax1.set_xlabel('Longitude', fontsize=12)
        ax1.set_ylabel('Latitude', fontsize=12)

        sns.kdeplot(
            data=df,
            x='distance_to_tokyo', y='magnitude',
            fill=True, cmap='hot', thresh=0.05,
            ax=ax2, cbar=True
        )
        ax2.set_xlabel('Distance to Tokyo', fontsize=12)
        ax2.set_ylabel('Magnitude', fontsize=12)


        plt.tight_layout()
        plt.show()