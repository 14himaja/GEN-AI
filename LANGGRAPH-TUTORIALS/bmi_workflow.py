# bmi_langgraph.py

# Import LangGraph components for creating the workflow
from langgraph.graph import StateGraph, START, END

# TypedDict is used to define the structure of our state
from typing import TypedDict


# --------------------------------------------------
# 1. DEFINE STATE
# --------------------------------------------------

class BMIState(TypedDict):
    """
    State contains all the data that moves through the graph.
    """

    weight_kg: float       # User's weight in kilograms
    height_m: float        # User's height in meters
    bmi: float             # Calculated BMI
    category: str          # BMI category


# --------------------------------------------------
# 2. DEFINE NODES
# --------------------------------------------------

def calculate_bmi(state: BMIState) -> BMIState:
    """
    Calculate BMI using weight and height.
    """

    # Get weight and height from the state
    weight = state["weight_kg"]
    height = state["height_m"]

    # BMI formula: weight / height²
    bmi = weight / (height ** 2)

    # Store the calculated BMI back in the state
    state["bmi"] = round(bmi, 2)

    return state


def label_bmi(state: BMIState) -> BMIState:
    """
    Determine the BMI category based on the calculated BMI.
    """

    # Get BMI from the state
    bmi = state["bmi"]

    # Decide the category
    if bmi < 18.5:
        state["category"] = "Underweight"

    elif 18.5 <= bmi < 25:
        state["category"] = "Normal"

    elif 25 <= bmi < 30:
        state["category"] = "Overweight"

    else:
        state["category"] = "Obese"

    return state


# --------------------------------------------------
# 3. CREATE THE GRAPH
# --------------------------------------------------

# Create a StateGraph using our BMIState
graph = StateGraph(BMIState)


# --------------------------------------------------
# 4. ADD NODES
# --------------------------------------------------

# Add our functions as nodes in the graph
graph.add_node("calculate_bmi", calculate_bmi)
graph.add_node("label_bmi", label_bmi)


# --------------------------------------------------
# 5. ADD EDGES
# --------------------------------------------------

# Define the execution flow:
#
# START → calculate_bmi → label_bmi → END

graph.add_edge(START, "calculate_bmi")

graph.add_edge("calculate_bmi", "label_bmi")

graph.add_edge("label_bmi", END)


# --------------------------------------------------
# 6. COMPILE THE GRAPH
# --------------------------------------------------

# Compile the graph so that it becomes executable
workflow = graph.compile()


# --------------------------------------------------
# 7. PROVIDE INITIAL INPUT
# --------------------------------------------------

# Initial state contains weight and height
initial_state = {
    "weight_kg": 80,
    "height_m": 1.73
}


# --------------------------------------------------
# 8. EXECUTE THE GRAPH
# --------------------------------------------------

# Pass the initial state into the workflow
final_state = workflow.invoke(initial_state)


# --------------------------------------------------
# 9. DISPLAY THE FINAL STATE
# --------------------------------------------------

print(final_state)