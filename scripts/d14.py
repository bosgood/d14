#!/usr/bin/env python3

import json
from urllib.request import urlopen
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


def pixelblaze_post(endpoint, body):
    """
    Makes a POST request to Firestorm
    @param endpoint: name of Firestorm endpoint
    @param body: POST request content
    @return JSON-decoded response body
    """
    pass


def discover():
    nodes = firestorm_get("discover")
    return nodes


def main():
    parser = argparse.ArgumentParser(
        description="Control the D14 sign")
    parser.add_argument('command', type=str, help='Command to run')
    args = parser.parse_args()

    if args.command == 'discover':
        nodes = discover()
        pprint(nodes)

    elif args.command == 'deploy':
        pass


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
