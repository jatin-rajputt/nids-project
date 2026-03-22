import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from engine.stats import stats


class LiveGraph:

    def __init__(self, parent):

        self.fig, self.ax = plt.subplots(figsize=(6, 3))

        # DARK THEME
        self.fig.patch.set_facecolor("#1e293b")
        self.ax.set_facecolor("#1e293b")

        self.canvas = FigureCanvasTkAgg(self.fig, master=parent)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        self.packet_data = []
        self.alert_data = []

        self.max_points = 40

        self.update_graph()

    def update_graph(self):

        packets, alerts = stats.get_rates()

        self.packet_data.append(packets)
        self.alert_data.append(alerts)

        if len(self.packet_data) > self.max_points:
            self.packet_data.pop(0)
            self.alert_data.pop(0)

        self.ax.clear()

        # 🎨 STYLE
        self.ax.set_facecolor("#1e293b")

        # 🔥 PULSE EFFECT (line thickness changes)
        pulse_width = 2 + (packets % 3)

        # 🔥 GRADIENT TRAIL EFFECT
        for i in range(len(self.packet_data)):
            alpha = i / len(self.packet_data)

            self.ax.plot(
                self.packet_data[:i+1],
                color="#38bdf8",
                linewidth=2,
                alpha=alpha * 0.6
            )

        for i in range(len(self.alert_data)):
            alpha = i / len(self.alert_data)

            self.ax.plot(
                self.alert_data[:i+1],
                color="#f43f5e",
                linewidth=2,
                alpha=alpha * 0.6
            )

        # 🔥 MAIN GLOW LINES
        self.ax.plot(self.packet_data, color="#38bdf8", linewidth=pulse_width)
        self.ax.plot(self.alert_data, color="#f43f5e", linewidth=2)

        # GRID (cyber style)
        self.ax.grid(color="#334155", linestyle=":", linewidth=0.6, alpha=0.3)

        # AXIS STYLE
        self.ax.tick_params(colors="white")

        for spine in self.ax.spines.values():
            spine.set_color("#334155")

        self.ax.set_title("⚡ LIVE THREAT MATRIX", color="#a78bfa", fontsize=10)

        self.ax.set_ylim(bottom=0)
        self.ax.margins(x=0)

        self.canvas.draw()

        # ⚡ FAST REFRESH = SMOOTH ANIMATION
        self.canvas.get_tk_widget().after(500, self.update_graph)