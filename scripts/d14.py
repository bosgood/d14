#!/usr/bin/env python3

import json
from urllib.request import urlopen, Request
from urllib.parse import urlencode
from urllib.error import HTTPError
import argparse
from pprint import pprint

FIRESTORM_ADDRESS = "192.168.5.1"


def firestorm_get(endpoint):
    """
    Makes a GET request to Firestorm
    @param endpoint: name of Firestorm endpoint
    @return JSON-decoded response body
    """
    resp = urlopen(f"http://{FIRESTORM_ADDRESS}/{endpoint}")
    body = resp.readlines()
    content = ""
    if len(body) > 0:
        content = json.loads(body[0].decode('utf-8'))

    if resp.code != 200:
        error = "<unknown>"
        if content:
            error = content
        raise Exception(f"Pixelblaze API error code {resp.code}: {error}")

    return content


def firestorm_post(endpoint, data):
    """
    Makes a POST request to Firestorm
    @param endpoint: name of Firestorm endpoint
    @param data: POST request content body
    @return JSON-decoded response body
    """
    json_bytes = json.dumps(data).encode('utf-8')
    req = Request(f"http://{FIRESTORM_ADDRESS}/{endpoint}",
                  method="POST")
    req.add_header('Content-Type', 'application/json')
    try:
        with urlopen(req, data=json_bytes) as resp:
            body = resp.read()
            return body.decode('utf-8')
    except HTTPError as err:
        return err


def discover():
    """
    Discovers all Pixelblaze nodes on the network
    @return List of complete Pixelblaze infos
    """
    nodes = firestorm_get("discover")
    return nodes


def scan():
    """
    Discovers all Pixelblaze nodes on the network
    @return List of Pixelblaze name/ID pairs
    """
    return [
        [n['name'], n['id']] for n in discover()
    ]


def scanmap():
    """
    Discovers all Pixelblaze nodes on the network
    @return Map of name/ID pairs, indexed by name
    """
    return {
        n['name']: n['id'] for n in discover()
    }


def command(cmd, targets):
    """
    Sends a command message to a set of nodes
    @param cmd: command name
    @param targets: Pixelblaze IDs
    @return command response body
    """

    # {
    #   "command": {
    #     "programName": "blink fade"
    #   },
    #   "ids": [
    #     6909667,
    #     9398311
    #   ]
    # }

    resp = firestorm_post("command", {
        'command': cmd,
        'ids': targets,
    })
    return resp


def pixelblaze_name_to_id(node_ids, node_id_ish):
    """
    Transform a Pixelblaze ID or name into an ID
    @param node_ids: a map of Pixelblaze node IDs by name
    @param node_id_ish: a Pixelblaze node ID or name
    @return a Pixelblaze node ID
    """
    try:
        id_num = int(node_id_ish)
        # Valid integer => already a node ID
        return id_num
    except ValueError:
        # Try to have a nicer error for node name typos, etc
        if node_id_ish not in node_ids:
            raise Exception(
                f"Unrecognized Pixelblaze name or ID: {node_id_ish}")

        # Not a valid integer => look up name in index
        return node_ids[node_id_ish]


def deploy(from_node_raw, to_nodes_raw):
    # Transform any name-based source or target specification into its Pixelblaze ID
    node_ids = scanmap()
    to_nodes_ids = [pixelblaze_name_to_id(node_ids, n) for n in to_nodes_raw]
    from_node_id = pixelblaze_name_to_id(node_ids, from_node_raw)

    data = {
        "from": from_node_id,
        "to": to_nodes_ids,
    }
    # Example curl command for performing this same request
    # curl -v -X POST -H 'Content-Type: application/json' -d '{"from": 811451, "to": [4514378, 8703982, 9987259, 9999035, 12327866, 14165434, 15792826, 16266426]}' http://192.168.5.1/clonePrograms
    resp = firestorm_post("clonePrograms", data)
    return resp


def main():
    parser = argparse.ArgumentParser(
        description="Control the D14 sign")
    parser.add_argument('command', type=str, help='Command to run')

    g_command = parser.add_argument_group(
        'command', 'command options'
    )
    g_command.add_argument(
        '--targets', help='node(s) to send command to', default=[], nargs='*')

    g_deployment = parser.add_argument_group(
        'deployment', 'pattern deployment options')
    g_deployment.add_argument(
        '--source', help='node to copy patterns from', default=None)
    g_deployment.add_argument(
        '--dest', help='node(s) to copy patterns to (empty => all)', default=None)

    args = parser.parse_args()

    # Subcommand selection
    if args.command == 'discover':
        nodes = discover()
        pprint(nodes)
    elif args.command == 'scan':
        names = scan()
        pprint(names)
    elif args.command == 'command':
        result = command(args.command, args.targets)
    elif args.command == 'deploy':
        # Basic argument validation for program cloning
        if not args.source:
            raise Exception(
                'Expected --source to be provided with a Pixelblaze ID')
        if not args.dest:
            raise Exception(
                'Expected --dest to be provided with Pixelblaze IDs')
        if args.source in args.dest:
            raise Exception(
                'Expected --dest not to contain the source Pixelblaze')

        targets = args.dest.split(',')
        result = deploy(args.source, targets)

        pprint(result)


if __name__ == "__main__":
    main()

"""
curl -v -X POST -H 'Content-Type: application/json' -d '{"from": 811451, "to": [4514378, 8703982, 9987259, 9999035, 12327866, 14165434, 15792826, 16266426]}' http://192.168.5.1/clonePrograms
"""

"""
[
    {'lastSeen': 1663285668415, 'address': '192.168.5.127', 'id': 4514378, 'programList': [{'id': 'GmbBoD4RPotp2Csep', 'name': '_dis2022-fireflies-v02'}, {'id': 'sWwoTCw5QphqCn3XF', 'name': '_dis2022-trailwave'}, {'id': 'eZexpi6oci6smqAvX', 'name': '_dis2023_calmpastel_2d'}, {'id': 'mrMbsS6TKaC9udXyt', 'name': '_dis2023_edgeburst_2d'}, {'id': 'bG6uqvfHfenBjqPt2', 'name': '_dis2023_pornj_noise_fade_2d'}, {'id': 'GES4qNDA3RqzbJSLF', 'name': '_dis2023_pornj_stripe_rotate_2d'}, {'id': 'LR4KPE7qNStxaFMaA', 'name': '_dis2022-edgeburst'}, {'id': 'ro9Gei457fBoxop9Y', 'name': '_dis2023_xorcery_2d_3d'}, {'id': 'Z6aFtRCE3AkpcP2E8', 'name': '_dis2022-fireflies'}, {'id': 'wPnJGj5d5hzgeLbZD', 'name': '_dis2022-pornjpulse'}, {'id': 'kpYKsFRRFospu4uqi', 'name': 'xorcery2d-white'}], 'ver': '3.30', 'exp': 0, 'pixelCount': 413, 'ledType': 5, 'dataSpeed': 2000000, 'colorOrder': 'BGR', 'sequenceTimer': 15, 'brightness': 0.88, 'name': 'distribution-e', 'fps': 46.90619, 'vmerr': 0, 'mem': 10218},
    {'lastSeen': 1663285668415, 'address': '192.168.5.196', 'id': 9999035, 'programList': [{'id': 'tJsh82wGLrMKGQ7Wq', 'name': 'low-power'}, {'id': 'LR4KPE7qNStxaFMaA', 'name': '_dis2022-edgeburst'}, {'id': 'Z6aFtRCE3AkpcP2E8', 'name': '_dis2022-fireflies'}, {'id': 'wPnJGj5d5hzgeLbZD', 'name': '_dis2022-pornjpulse'}, {'id': 'vk3PEKaZyfYXTeBEM', 'name': 'sweep-test-v01'}, {'id': 'kpYKsFRRFospu4uqi', 'name': 'xorcery2d-white'}, {'id': 'ro9Gei457fBoxop9Y', 'name': 'xorcery 2D/3D'}, {'id': 'GmbBoD4RPotp2Csep', 'name': '_dis2022-fireflies-v02'}, {'id': 'sWwoTCw5QphqCn3XF', 'name': '_dis2022-trailwave'}, {'id': 'kuJfFyCSkCKNasyNE', 'name': 'map-d'}], 'ver': '3.30', 'exp': 0, 'pixelCount': 267, 'ledType': 5, 'dataSpeed': 2000000, 'colorOrder': 'GBR', 'sequenceTimer': 15, 'brightness': 1, 'name': 'distribution-o', 'fps': 79.92007, 'vmerr': 0, 'mem': 10239}
]
"""
