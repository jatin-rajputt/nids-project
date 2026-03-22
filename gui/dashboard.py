import tkinter as tk
from tkinter import ttk, scrolledtext
from gui.live_graph import LiveGraph
from gui.interface_selector import get_interfaces
from core.event_bus import consume


def start_dashboard(start_ids, stop_ids):

    root = tk.Tk()

    # 🎨 THEME COLORS
    BG = "#0f172a"
    PANEL = "#1e293b"
    TEXT = "#e2e8f0"
    BORDER = "#334155"

    root.configure(bg=BG)
    root.title("Advanced Network Intrusion Detection System")
    root.geometry("1200x650")

    # 🧱 PANEL CREATOR
    def create_panel(parent):
        frame = tk.Frame(parent, bg=PANEL, highlightbackground=BORDER, highlightthickness=1)
        return frame

    # 🧩 MAIN CONTAINER
    main = tk.Frame(root, bg=BG)
    main.pack(fill="both", expand=True, padx=10, pady=10)

    # LEFT SIDE (traffic + alerts stacked)
    left_container = tk.Frame(main, bg=BG)
    left_container.place(relx=0.02, rely=0.05, relwidth=0.58, relheight=0.9)

    # 🔥 TRAFFIC PANEL (TOP - BIG)
    traffic_frame = create_panel(left_container)
    traffic_frame.pack(fill="both", expand=True, pady=5)

    tk.Label(traffic_frame, text="Live Traffic", bg=PANEL, fg=TEXT,
            font=("Segoe UI", 12, "bold")).pack(pady=5)

    traffic_box = scrolledtext.ScrolledText(
        traffic_frame,
        bg=PANEL,
        fg=TEXT,
        insertbackground="white",
        borderwidth=0,
        font=("Consolas", 10)
    )
    traffic_box.pack(fill="both", expand=True, padx=5, pady=5)


    # 🔥 ALERT PANEL (BOTTOM - SMALL)
    alert_frame = create_panel(left_container)
    alert_frame.pack(fill="x", pady=5)

    tk.Label(alert_frame, text="Alerts", bg=PANEL, fg=TEXT,
            font=("Segoe UI", 11, "bold")).pack(pady=5)

    alert_box = scrolledtext.ScrolledText(
        alert_frame,
        height=8,   # small height
        bg=PANEL,
        fg="#f87171",
        insertbackground="white",
        borderwidth=0,
        font=("Consolas", 9)
    )
    alert_box.pack(fill="x", padx=5, pady=5)
        
    alert_frame.config(highlightbackground="#334155", highlightthickness=1)
   

    # 📦 RIGHT → GRAPHS
    graph_frame = create_panel(main)
    graph_frame.place(relx=0.66, rely=0.05, relwidth=0.32, relheight=0.9)

    # 3 stacked graphs
    g1 = tk.Frame(graph_frame, bg=PANEL)
    g1.pack(fill="both", expand=True)

    

    LiveGraph(graph_frame)
    

    # 🔽 TOP CONTROL BAR (Dropdown + Buttons)
    control = tk.Frame(root, bg=BG)
    control.place(relx=0.34, rely=0.01)

    interfaces = get_interfaces()
    interface_var = tk.StringVar()

    dropdown = ttk.Combobox(
        control,
        textvariable=interface_var,
        values=list(interfaces.keys()),
        width=40
    )
    dropdown.pack(side="left", padx=5)
    dropdown.current(0)

    def start():
        start_ids(interfaces[interface_var.get()])

    def stop():
        stop_ids()

    tk.Button(control, text="Start IDS", command=start,
              bg="#334155", fg="white").pack(side="left", padx=5)

    tk.Button(control, text="Stop IDS", command=stop,
              bg="#334155", fg="white").pack(side="left", padx=5)

    # 🔄 EVENT LOOP
    def update():
        attack_counter = {}
        if not root.winfo_exists():
            return

        while True:
            event = consume()
            if event is None:
                break

            if event["type"] == "traffic_event":
                traffic_box.insert(tk.END, event["data"] + "\n")
                traffic_box.see(tk.END)

            elif event["type"] == "alert_event":
                msg = event["data"]

                # extract IP
                if "from" in msg:
                    ip = msg.split("from")[-1].strip()

                    attack_counter[ip] = attack_counter.get(ip, 0) + 1

                    top_ip = max(attack_counter, key=attack_counter.get)

                    # top_ip_label.config(text=f"Top IP: {top_ip}")
                    # attack_count_label.config(text=f"Attacks: {attack_counter[top_ip]}")
                    # status_label.config(text="Status: ATTACKING", fg="#ef4444")

                alert_box.insert(tk.END, msg + "\n")
                alert_box.see(tk.END)

        root.after(200, update)

    update()

    def on_close():
        stop_ids()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)

    root.mainloop()