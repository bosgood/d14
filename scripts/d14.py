#!/usr/bin/env python3

import json
from urllib.request import urlopen, Request
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
    req = Request(f"http://{FIRESTORM_ADDRESS}/{endpoint}",
                  data=data,
                  headers={'Content-Type': 'application/json'},
                  method="POST")
    # TODO need to finish POST implementation
    import ipdb
    ipdb.set_trace()


def discover():
    """
    Discovers all Pixelblaze nodes on the network
    @return List of Pixelblaze infos
    """
    nodes = firestorm_get("discover")
    return nodes


def deploy(from_node, to_nodes):
    # TODO need to establish target list to populate data
    # curl -v -X POST -H 'Content-Type: application/json' -d '{"from": 811451, "to": [4514378, 8703982, 9987259, 9999035, 12327866, 14165434, 15792826, 16266426]}' http://192.168.5.1/clonePrograms
    data = {}
    resp = firestorm_post("clonePrograms", data)
    # TODO need to run /clonePrograms again and view response body


def main():
    parser = argparse.ArgumentParser(
        description="Control the D14 sign")
    parser.add_argument('command', type=str, help='Command to run')

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
    elif args.command == 'deploy':
        # TODO need argument parsing here so targets can be specified in user-friendly ways
        result = deploy(args.source, args.dest)
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
