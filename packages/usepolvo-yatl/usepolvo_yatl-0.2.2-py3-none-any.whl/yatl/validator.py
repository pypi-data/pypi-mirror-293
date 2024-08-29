from typing import Any, Dict


class YATLValidator:
    def __init__(self):
        self.errors = []

    def validate(self, parsed_yatl: Dict[str, Any]) -> bool:
        self.errors = []

        self._validate_structure(parsed_yatl)
        self._validate_states(parsed_yatl.get("states", {}))
        self._validate_actions(parsed_yatl.get("actions", {}))
        self._validate_variables(parsed_yatl.get("variables", {}))
        self._validate_initial_state(parsed_yatl)

        return len(self.errors) == 0

    def _validate_structure(self, data: Dict[str, Any]):
        required_keys = ["name", "description", "initial_state", "states", "actions", "variables"]
        for key in required_keys:
            if key not in data:
                self.errors.append(f"Missing required key: {key}")

    def _validate_states(self, states: Dict[str, Any]):
        if not isinstance(states, dict):
            self.errors.append("'states' must be a dictionary")
            return

        for state_name, state_data in states.items():
            self._validate_state(state_name, state_data)

    def _validate_state(self, state_name: str, state_data: Dict[str, Any]):
        if "type" not in state_data:
            self.errors.append(f"State '{state_name}' is missing 'type'")

        if state_data.get("type") == "task":
            if "action" not in state_data:
                self.errors.append(f"Task state '{state_name}' is missing 'action'")
            if "next" not in state_data:
                self.errors.append(f"Task state '{state_name}' is missing 'next'")

        elif state_data.get("type") == "choice":
            if "choices" not in state_data or not isinstance(state_data["choices"], list):
                self.errors.append(f"Choice state '{state_name}' must have a 'choices' list")
            if "default" not in state_data:
                self.errors.append(f"Choice state '{state_name}' is missing 'default'")

        elif state_data.get("type") == "loop":
            if "collection" not in state_data:
                self.errors.append(f"Loop state '{state_name}' is missing 'collection'")
            if "iterator" not in state_data:
                self.errors.append(f"Loop state '{state_name}' is missing 'iterator'")
            if "body" not in state_data:
                self.errors.append(f"Loop state '{state_name}' is missing 'body'")

    def _validate_actions(self, actions: Dict[str, Any]):
        if not isinstance(actions, dict):
            self.errors.append("'actions' must be a dictionary")
            return

        for action_name, action_data in actions.items():
            if "description" not in action_data:
                self.errors.append(f"Action '{action_name}' is missing 'description'")
            if "language" not in action_data:
                self.errors.append(f"Action '{action_name}' is missing 'language'")
            if "code" not in action_data:
                self.errors.append(f"Action '{action_name}' is missing 'code'")

    def _validate_variables(self, variables: Dict[str, Any]):
        if not isinstance(variables, dict):
            self.errors.append("'variables' must be a dictionary")

    def _validate_initial_state(self, data: Dict[str, Any]):
        initial_state = data.get("initial_state")
        if initial_state not in data.get("states", {}):
            self.errors.append(f"Initial state '{initial_state}' is not defined in states")
