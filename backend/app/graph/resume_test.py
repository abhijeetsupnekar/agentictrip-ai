from app.graph.workflow import graph

paused_state = {
    "user_input": "Book option 2",
    "intent": "flight",
    "workflow_stage": "waiting_for_selection",
    "selected_option": None,
    "flights": [
        {
            "airline": "Air India",
            "outbound_route": "PNQ → DEL",
            "departure": "2026-05-22T22:00:00",
            "arrival": "2026-05-23T00:25:00",
            "duration": "PT2H25M",
            "stops": 0,
            "price": "61.64",
            "currency": "GBP",
            "cabin_class": "economy",
            "passengers": 1,
        },
        {
            "airline": "Indigo",
            "outbound_route": "PNQ → DEL",
            "departure": "2026-05-22T08:45:00",
            "arrival": "2026-05-22T11:10:00",
            "duration": "PT2H25M",
            "stops": 0,
            "price": "63.21",
            "currency": "GBP",
            "cabin_class": "economy",
            "passengers": 1,
        },
    ],
    "messages": [],
}


result = graph.invoke(
    paused_state, config={"configurable": {"thread_id": "resume-thread"}}
)

print("\nRESUMED GRAPH STATE:\n")

print(result)
