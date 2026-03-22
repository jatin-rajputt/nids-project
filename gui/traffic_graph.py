import matplotlib.pyplot as plt
from engine.stats import stats

def show_graph():

    history = stats.get_packet_history()

    if not history:
        return

    times = [x[0] for x in history]
    packets = [x[1] for x in history]

    plt.figure("Network Traffic")
    plt.plot(times, packets)

    plt.xlabel("Time")
    plt.ylabel("Packets")
    plt.title("Network Traffic Monitor")

    plt.show()