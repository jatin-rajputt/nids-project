import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import tkinter as tk
import re

class AnalyticsPanel:
    def __init__(self, parent_frame):
        self.frame = parent_frame
        # Use a style context to handle dark mode globally
        plt.style.use('dark_background')
        self.fig, self.axes = plt.subplots(2, 2, figsize=(12, 8))
        self.fig.patch.set_facecolor('#1e1e2e')
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def update_charts(self, alert_log_path="data/alerts.log"):
        df = self._parse_alerts(alert_log_path)
        if df.empty:
            return

        # Clear axes first
        for ax in self.axes.flat:
            ax.clear()
            ax.set_facecolor('#0f172a')

        # Chart 1: Attack type distribution
        ax1 = self.axes[0, 0]
        sns.countplot(data=df, x='attack_type', palette='Set2', ax=ax1)
        ax1.set_title('Attack Type Distribution', color='white', fontweight='bold')
        ax1.set_xlabel("Attack Type", color='white')
        ax1.set_ylabel("Count", color='white')

        # Chart 2: Attacks over time
        ax2 = self.axes[0, 1]
        df['hour'] = df['timestamp'].dt.hour
        hourly = df.groupby(['hour','attack_type']).size().reset_index(name='count')
        sns.lineplot(data=hourly, x='hour', y='count', hue='attack_type', ax=ax2, marker='o')
        ax2.set_title('Attacks by Hour', color='white', fontweight='bold')
        ax2.set_xlabel("Hour of Day", color='white')

        # Chart 3: Top attacking IPs
        ax3 = self.axes[1, 0]
        top_ips = df['source_ip'].value_counts().head(10).reset_index()
        top_ips.columns = ['ip', 'count']
        sns.barplot(data=top_ips, x='count', y='ip', palette='flare', ax=ax3)
        ax3.set_title('Top 10 Source IPs', color='white', fontweight='bold')
        ax3.set_ylabel("Source IP", color='white')

        # Chart 4: Severity heatmap
        ax4 = self.axes[1, 1]
        # Ensure severity is ordered logically
        severity_order = ['LOW', 'MEDIUM', 'HIGH']
        df['severity'] = pd.Categorical(df['severity'], categories=severity_order, ordered=True)
        pivot = df.pivot_table(index='severity', columns='hour', aggfunc='size', fill_value=0)
        
        # cbar=False or handling the cbar ax is safer in tight Tkinter loops
        sns.heatmap(pivot, cmap='YlOrRd', ax=ax4, annot=True, fmt='d', cbar_kws={'label': 'Attack Count'})
        ax4.set_title('Severity Heatmap by Hour', color='white', fontweight='bold')

        # Apply white ticks AFTER clearing and plotting
        for ax in self.axes.flat:
            ax.tick_params(colors='white', labelsize=9)
            for spine in ax.spines.values():
                spine.set_edgecolor('#44475a')

        self.fig.tight_layout()
        self.canvas.draw()

    def _parse_alerts(self, path):
        rows = []
        try:
            with open(path) as f:
                for line in f:
                    # Improved regex to handle potential trailing spaces
                    m = re.match(r'\[(.+?)\] \[(\w+)\] (.+?) detected from (.+)', line.strip())
                    if m:
                        rows.append({
                            'timestamp': pd.to_datetime(m.group(1)),
                            'severity': m.group(2).upper(),
                            'attack_type': m.group(3).strip(),
                            'source_ip': m.group(4).strip()
                        })
        except (FileNotFoundError, Exception) as e:
            print(f"Error reading log: {e}")
        return pd.DataFrame(rows)