from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Dict


class YATLRuntime:
    def __init__(self, compiled_yatl: Dict[str, Any]):
        self.name = compiled_yatl["name"]
        self.description = compiled_yatl["description"]
        self.states = compiled_yatl["states"]
        self.actions = compiled_yatl["actions"]
        self.variables = compiled_yatl["variables"]
        self.current_state = compiled_yatl["initial_state"]
        self.context = {var_name: None for var_name in self.variables}

    def execute(self):
        while self.current_state:
            state = self.states[self.current_state]
            if state["type"] == "task":
                self._execute_action(state["action"])
                self.current_state = state.get("next")
            elif state["type"] == "choice":
                self.current_state = self._evaluate_choice(state)
            elif state["type"] == "loop":
                self._execute_loop(state)
                self.current_state = state.get("next")
            elif state["type"] == "parallel":
                self._execute_parallel(state)
                self.current_state = state.get("next")
            elif state["type"] == "end":
                break

    def _execute_action(self, action_name: str):
        action = self.actions[action_name]
        if action["language"] == "python":
            exec(action["code"], {"context": self.context})
        else:
            print(f"Unsupported language: {action['language']}")

    def _evaluate_choice(self, state: Dict[str, Any]) -> str:
        for choice in state["choices"]:
            if self._evaluate_condition(choice["condition"]):
                return choice["next"]
        return state["default"]

    def _evaluate_condition(self, condition: Dict[str, Any]) -> bool:
        variable = self.context[condition["variable"]]
        operator = condition["operator"]
        value = condition["value"]

        if operator == "equals":
            return variable == value
        elif operator == "not_equals":
            return variable != value
        elif operator == "greater_than":
            return variable > value
        elif operator == "less_than":
            return variable < value
        elif operator == "contains":
            return value in variable
        else:
            raise ValueError(f"Unsupported operator: {operator}")

    def _execute_loop(self, state: Dict[str, Any]):
        collection = self.context[state["collection"]]
        for item in collection:
            self.context[state["iterator"]] = item
            self._execute_state(state["body"])

    def _execute_parallel(self, state: Dict[str, Any]):
        with ThreadPoolExecutor() as executor:
            futures = []
            for branch in state["branches"]:
                future = executor.submit(self._execute_state, branch)
                futures.append(future)

            for future in as_completed(futures):
                future.result()  # This will raise an exception if the branch execution failed

    def _execute_state(self, state: Dict[str, Any]):
        if state["type"] == "task":
            self._execute_action(state["action"])
        elif state["type"] == "choice":
            next_state = self._evaluate_choice(state)
            if next_state:
                self._execute_state(self.states[next_state])
        elif state["type"] == "loop":
            self._execute_loop(state)
        elif state["type"] == "parallel":
            self._execute_parallel(state)
