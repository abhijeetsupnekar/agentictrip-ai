from app.graph.workflow import graph

initial_state = {
    "user_input": "show flights Pune to Delhi",
    "selected_option": 1,
    "intent": None,
    "source": None,
    "destination": None,
    "departure_date": None,
    "passengers": None,
    "cabin": None,
    "flights": [],
    "selected_flight": None,
    "booking_status": None,
    "messages": [],
}


result = graph.invoke(initial_state, config={"configurable": {"thread_id": "user-123"}})

print("\nFINAL GRAPH STATE:\n")

print(result)
