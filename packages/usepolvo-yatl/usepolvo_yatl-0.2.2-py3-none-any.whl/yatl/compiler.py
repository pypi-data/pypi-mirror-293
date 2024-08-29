from typing import Any, Dict


class YATLCompiler:
    def __init__(self):
        pass

    def compile(self, parsed_yatl: Dict[str, Any]) -> Dict[str, Any]:
        compiled_yatl = {
            "name": parsed_yatl["name"],
            "description": parsed_yatl["description"],
            "initial_state": parsed_yatl["initial_state"],
            "states": {},
            "actions": {},
            "variables": parsed_yatl["variables"],
        }

        for state_name, state_data in parsed_yatl["states"].items():
            compiled_state = self._compile_state(state_name, state_data)
            compiled_yatl["states"][state_name] = compiled_state

        for action_name, action_data in parsed_yatl["actions"].items():
            compiled_action = self._compile_action(action_name, action_data)
            compiled_yatl["actions"][action_name] = compiled_action

        return compiled_yatl

    def _compile_state(self, state_name: str, state_data: Dict[str, Any]) -> Dict[str, Any]:
        compiled_state = {
            "type": state_data.get("type", "task"),
            "next": state_data.get("next"),
        }

        if state_data.get("type") == "task":
            compiled_state["action"] = state_data.get("action")

        elif state_data.get("type") == "choice":
            compiled_state["choices"] = state_data.get("choices", [])
            compiled_state["default"] = state_data.get("default")

        elif state_data.get("type") == "loop":
            compiled_state["collection"] = state_data.get("collection")
            compiled_state["iterator"] = state_data.get("iterator")
            compiled_state["body"] = self._compile_state("body", state_data.get("body", {}))

        elif state_data.get("type") == "parallel":
            compiled_state["branches"] = [
                self._compile_state(f"branch_{i}", branch) for i, branch in enumerate(state_data.get("branches", []))
            ]

        return compiled_state

    def _compile_action(self, action_name: str, action_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "description": action_data.get("description"),
            "language": action_data.get("language"),
            "code": action_data.get("code"),
        }
