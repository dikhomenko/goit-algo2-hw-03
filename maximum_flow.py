import networkx as nx


def build_logistics_graph():
    # Create graph
    G = nx.DiGraph()

    # Add edges with capacities
    G.add_edge("Термінал 1", "Склад 1", capacity=25)
    G.add_edge("Термінал 1", "Склад 2", capacity=20)
    G.add_edge("Термінал 1", "Склад 3", capacity=15)
    G.add_edge("Термінал 2", "Склад 3", capacity=15)
    G.add_edge("Термінал 2", "Склад 4", capacity=30)
    G.add_edge("Термінал 2", "Склад 2", capacity=10)

    G.add_edge("Склад 1", "Магазин 1", capacity=15)
    G.add_edge("Склад 1", "Магазин 2", capacity=10)
    G.add_edge("Склад 1", "Магазин 3", capacity=20)

    G.add_edge("Склад 2", "Магазин 4", capacity=15)
    G.add_edge("Склад 2", "Магазин 5", capacity=10)
    G.add_edge("Склад 2", "Магазин 6", capacity=25)

    G.add_edge("Склад 3", "Магазин 7", capacity=20)
    G.add_edge("Склад 3", "Магазин 8", capacity=15)
    G.add_edge("Склад 3", "Магазин 9", capacity=10)

    G.add_edge("Склад 4", "Магазин 10", capacity=20)
    G.add_edge("Склад 4", "Магазин 11", capacity=10)
    G.add_edge("Склад 4", "Магазин 12", capacity=15)
    G.add_edge("Склад 4", "Магазин 13", capacity=5)
    G.add_edge("Склад 4", "Магазин 14", capacity=10)

    return G


def add_super_source_and_sink(G):
    # Add a super source and connect it to all terminals
    G.add_node("Super Source")
    G.add_edge("Super Source", "Термінал 1", capacity=float("inf"))
    G.add_edge("Super Source", "Термінал 2", capacity=float("inf"))

    # Add a super sink and connect all stores to it
    G.add_node("Super Sink")
    for store in [f"Магазин {i}" for i in range(1, 15)]:
        G.add_edge(store, "Super Sink", capacity=float("inf"))


def generate_report(flow_dict):
    report = []

    for terminal in ["Термінал 1", "Термінал 2"]:
        # Copy the flows
        terminal_flows = dict(flow_dict[terminal])

        for warehouse in terminal_flows:
            if not warehouse.startswith("Склад"):
                continue

            warehouse_flows = dict(flow_dict[warehouse])

            # How much can flow from terminal to warehouse
            terminal_to_warehouse_flow = terminal_flows[warehouse]

            for store in warehouse_flows:
                if not store.startswith("Магазин"):
                    continue

                warehouse_to_store_flow = warehouse_flows[store]

                # Take the minimum flow available
                flow = min(terminal_to_warehouse_flow, warehouse_to_store_flow)

                if flow > 0:
                    report.append((terminal, store, flow))

                    # Decrease the remaining flows
                    terminal_to_warehouse_flow -= flow
                    warehouse_flows[store] -= flow

                if terminal_to_warehouse_flow == 0:
                    break

    return report


if __name__ == "__main__":
    # Build the logistics graph
    G = build_logistics_graph()

    # Add super source and super sink
    add_super_source_and_sink(G)

    # Calculate maximum flow using Edmonds-Karp algorithm
    flow_value, flow_dict = nx.maximum_flow(
        G, "Super Source", "Super Sink", flow_func=nx.algorithms.flow.edmonds_karp
    )

    # Generate the report
    print("Report:")
    print("Термінал Магазин Фактичний Потік (одиниць)")
    report = generate_report(flow_dict)
    total_flow = 0
    for terminal, store, flow in report:
        print(f"{terminal}\t{store}\t{flow}")
        total_flow += flow

    print(f"Total Flow: {total_flow} (одиниць)")
    print(f"Maximum flow for the entire network: {flow_value}")


# Склад	  | Реальний флоу                                                   |
# --------|-----------------------------------------------------------------|
# Склад 1 |	Термінал 1 >> Склад 1 = 25                                      |
# Склад 2 |	Термінал 1 >> Склад 2 (20) + Термінал 2 >> Склад 2 (10) = 30    |
# Склад 3 |	Термінал 1 >> Склад 3 (15) + Термінал 2 >> Склад 3 (15) = 30    |
# Склад 4 |	Термінал 2 >> Склад 4 = 30                                      |
# --------------------------------------------------------------------------|
# Maximum flow 115

# Після отримання таблиці дайте відповідь на наступні запитання:

# 1. Які термінали забезпечують найбільший потік товарів до магазинів?
# Tермінал 1 - 60 одиниць.
# 2. Які маршрути мають найменшу пропускну здатність і як це впливає на загальний потік?
# Термінал 2 >> Склад 2 - 10 одиниць.
# 3. Які магазини отримали найменше товарів і чи можна збільшити їх постачання, збільшивши пропускну здатність певних маршрутів?
# Магазин 13 - 5 одиниць.
# 4. Чи є вузькі місця, які можна усунути для покращення ефективності логістичної мережі?
# Збільшити потужність ліній від терміналів до складів: Термінал 2 >> Склад 2 з 10 до 20, загальний потік може вирости вище 115.
