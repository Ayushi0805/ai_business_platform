"""
Phase 8 — LangGraph workflow engine.

LangGraph orchestrates the entire AI pipeline as a StateGraph,
passing order data through each processing node in sequence.

Install: pip install langgraph

Flow:
  receive_order → run_agents → run_rag → run_llm → make_decision → trigger_n8n → save_to_db
"""
from typing import TypedDict, Optional

class OrderState(TypedDict):
    order_id: int
    user_id: int
    product_id: int
    quantity: int
    total_price: float
    image_path: Optional[str]
    invoice_text: Optional[str]
    fraud: Optional[bool]
    image_analysis: Optional[dict]
    invoice_data: Optional[dict]
    rag_context: Optional[str]
    llm_verdict: Optional[str]
    decision: Optional[str]
    n8n_triggered: Optional[bool]


def node_run_agents(state: OrderState) -> OrderState:
    from app.agents.crew import run_crew
    order_data = {
        'total_price': state.get('total_price'),
        'quantity': state.get('quantity'),
        'user_id': state.get('user_id'),
        'image_path': state.get('image_path'),
        'invoice_text': state.get('invoice_text')
    }
    reports = run_crew(order_data)
    state['fraud'] = 'FRAUD' in reports.get('fraud_report', '').upper()
    return state


def node_run_rag(state: OrderState) -> OrderState:
    from app.rag.chain import query_rag
    query = f"Are there any special rules for product_id {state['product_id']} or orders over ${state['total_price']}?"
    state['rag_context'] = query_rag(query)
    return state


def node_run_llm(state: OrderState) -> OrderState:
    from app.llm.base_llm import ask_llm
    prompt = f"Context: {state['rag_context']}\nFraud: {state['fraud']}\nShould we approve this order?"
    verdict = ask_llm(prompt)
    if hasattr(verdict, 'content'):
        state['llm_verdict'] = verdict.content
    else:
        state['llm_verdict'] = str(verdict)
    return state


def node_make_decision(state: OrderState) -> OrderState:
    from app.decision.engine import make_decision
    state['decision'] = make_decision(
        fraud=state.get('fraud') or False,
        image_ok=True,
        invoice_valid=True,
        llm_verdict=state.get('llm_verdict') or ''
    )
    return state


def node_trigger_n8n(state: OrderState) -> OrderState:
    from app.services.n8n import trigger_n8n
    result = trigger_n8n({
        'order_id': state['order_id'],
        'decision': state['decision'],
        'fraud': state.get('fraud'),
        'total_price': state['total_price']
    })
    state['n8n_triggered'] = result is not None
    return state


def run_flow(initial_state: OrderState) -> OrderState:
    from langgraph.graph import StateGraph
    graph = StateGraph(OrderState)

    graph.add_node('run_agents', node_run_agents)
    graph.add_node('run_rag', node_run_rag)
    graph.add_node('run_llm', node_run_llm)
    graph.add_node('make_decision', node_make_decision)
    graph.add_node('trigger_n8n', node_trigger_n8n)

    graph.set_entry_point('run_agents')
    graph.add_edge('run_agents', 'run_rag')
    graph.add_edge('run_rag', 'run_llm')
    graph.add_edge('run_llm', 'make_decision')
    graph.add_edge('make_decision', 'trigger_n8n')

    app = graph.compile()
    final_state = app.invoke(initial_state)
    return final_state
