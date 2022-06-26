import json
from typing import Dict, Literal, Union


def write_to_file(
    filename,
    output_results: Dict,
    /,
    output: Union[Literal["json"], Literal["csv"]] = "json",
):
    """Output the results of an experiment to file in JSON or CSV format."""
    with open(filename, "w+") as f:
        if output == "json":
            encoded_output = json.dumps(output_results, indent=2)
            f.write(encoded_output)
        else:
            raise NotImplementedError("CSV output not supported yet!")
