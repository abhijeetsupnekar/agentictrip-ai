from langgraph.graph import StateGraph, END

from langgraph.checkpoint.memory import MemorySaver

from app.graph.state import AgentState

from app.graph.nodes import (
    intent_node,
    flight_search_node,
    booking_node,
    confirmation_node,
    resume_booking_node,
)

# -----------------------------------
# ROUTERS
# -----------------------------------


def route_intent(state: AgentState):

    intent = state.get("intent")

    print("ROUTING INTENT:", intent)

    if intent == "flight":
        return "flight_search_node"

    if intent == "book_flight_option":
        return "resume_booking_node"

    return END


def route_after_flight(state: AgentState):

    stage = state.get("workflow_stage")

    print("WORKFLOW STAGE:", stage)

    if stage == "waiting_for_selection":

        return END

    return "booking_node"


# -----------------------------------
# GRAPH
# -----------------------------------


workflow = StateGraph(AgentState)


# NODES

workflow.add_node(
    "intent_node",
    intent_node,
)

workflow.add_node(
    "flight_search_node",
    flight_search_node,
)

workflow.add_node(
    "resume_booking_node",
    resume_booking_node,
)

workflow.add_node(
    "booking_node",
    booking_node,
)

workflow.add_node(
    "confirmation_node",
    confirmation_node,
)


# ENTRY

workflow.set_entry_point("intent_node")


# ROUTES

workflow.add_conditional_edges(
    "intent_node",
    route_intent,
)

workflow.add_conditional_edges(
    "flight_search_node",
    route_after_flight,
)


# FLOW

workflow.add_edge(
    "resume_booking_node",
    "booking_node",
)

workflow.add_edge(
    "booking_node",
    "confirmation_node",
)

workflow.add_edge(
    "confirmation_node",
    END,
)


# MEMORY

memory = MemorySaver()


graph = workflow.compile(checkpointer=memory)
