from argparse import ArgumentParser
import logging
from typing import Any, Dict, List, Tuple, Union

from modlink import Agent, Action


class AgentArgParser:
    """
    Parses command line arguments for an agent so that it can perform an action.
    """

    def __init__(self, agent: "Agent"):
        self.agent = agent
        self.description = agent.describe()
        self.actions = self.description["actions"]
        self.actions = sorted(
            self.actions,
            key=lambda x: x["properties"]["action"]["value"],
        )
        self.parser = ArgumentParser(description=self.description["role"])
        self.subparsers = self.parser.add_subparsers(
            dest="action",
            help="Actions to perform.",
        )
        for action in self.actions:
            command = action["properties"]["action"]["value"]
            command = action["properties"]["action"]["value"]
            required_fields = action.get("required", [])
            subparser = self.subparsers.add_parser(
                name=command,
                help=action["description"],
            )
            definitions = action.get("$defs", {})
            properties = action["properties"]
            for prop_name, prop_details in properties.items():
                arg_name = f"--{prop_name}"
                if "action" in prop_name:
                    # Ignore the action property since it's already handled
                    continue
                if "type" in prop_details:
                    choices = None
                    arg_type = self._get_arg_type(prop_details["type"])
                elif "anyOf" in prop_details or "oneOf" in prop_details:
                    # Handling Optional and Literal cases
                    sub_schemas = prop_details.get("anyOf") or prop_details.get("oneOf")
                    arg_type, choices = self._resolve_of_choices(
                        definitions, sub_schemas
                    )
                elif "allOf" in prop_details:
                    ref = prop_details["allOf"][0]["$ref"]
                    arg_type = str
                    choices = self._resolve_enum_definitions(ref, definitions)
                else:
                    raise ValueError(
                        f"Unsupported property '{prop_name}', {prop_details}"
                    )

                subparser.add_argument(
                    arg_name,
                    type=arg_type,
                    help=prop_details.get("description", None),
                    required=prop_name in required_fields,
                    choices=choices,
                )

    def _resolve_of_choices(
        self, definitions: Dict, details: Dict
    ) -> Tuple[type, List[str]]:
        possible_types = []
        choices = None
        for schema in details:
            if "$ref" in schema:
                # Resolve the reference using the definitions object
                ref_name = schema["$ref"].split("/")[-1]
                resolved_schema = definitions.get(ref_name, {})
                if "type" in resolved_schema:
                    possible_types.append(self._get_arg_type(resolved_schema["type"]))
                if "enum" in resolved_schema:
                    choices = resolved_schema["enum"]
            elif "type" in schema and schema["type"] != "null":
                possible_types.append(self._get_arg_type(schema["type"]))
            if "enum" in schema:
                choices = schema["enum"]

        if not possible_types:
            raise ValueError(f"No valid types found for {details}.")
        elif len(possible_types) == 1:
            arg_type = possible_types[0]
        else:
            logging.info(f"Multiple types found, using Union. {possible_types}")
            arg_type = Union[tuple(possible_types)]
        return (arg_type, choices)

    def _resolve_enum_definitions(self, ref: str, definitions: Dict) -> List[str]:
        ref_key = ref.split("/")[-1]
        if ref_key in definitions:
            ref_def = definitions[ref_key]
            ref_options = ref_def.get("enum", [])
            return ref_options
        else:
            raise ValueError(f"Reference '{ref}' not found in definitions.")

    def _get_arg_type(self, type_str: str) -> type:
        if type_str == "integer":
            return int
        elif type_str == "number":
            return float
        elif type_str == "boolean":
            return bool
        elif type_str == "string":
            return str
        elif type_str == "array":
            return lambda x: x.split(";")
        elif type_str == "null":
            return type(None)
        else:
            raise ValueError(f"Unsupported type: {type_str}")

    def parse_args(self) -> Action | None:
        if self.agent.context is None:
            raise RuntimeError(
                "The agent must be attached to a context before parsing arguments."
            )
        args = self.parser.parse_args()
        if args.action is None:
            self.parser.print_help()
            return None
        filtered_args = {k: v for k, v in vars(args).items() if v is not None}
        logging.info(f"Performing action: {filtered_args}")
        return self.agent.action_from_dict(filtered_args)

    def parse_and_perform(self) -> Any:
        action = self.parse_args()
        if action is not None:
            return self.agent.perform(action)
        else:
            logging.error(f"Unable to parse action {action}")
            return None
