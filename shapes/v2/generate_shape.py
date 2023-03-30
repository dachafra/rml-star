#!/usr/bin/env python

import argparse
import sys
from os import path
from glob import glob
from rdflib import Graph, Namespace
from rdflib.plugins.serializers.turtle import TurtleSerializer
from rdflib import plugin

SUBSHAPE_FORMAT = 'turtle'
SUBSHAPE_GLOB_PATTERN = '*.ttl'
SHACL = Namespace('http://www.w3.org/ns/shacl#')
RML = Namespace('http://w3id.org/rml/core/')
RMLS = Namespace('http://w3id.org/rml/core/star/')


class TurtleWithPrefixes(TurtleSerializer):
    """
    A turtle serializer that always emits prefixes
    Workaround for https://github.com/RDFLib/rdflib/issues/1048
    """
    roundtrip_prefixes = True  # Undocumented, forces to write all prefixes


class ShapeGenerator:
    """
    Generates a complete SHACL shape of all the SHACL subshapes.
    Useful for using the shapes in the shacl.org Playground.
    """
    def __init__(self, glob_pattern: str, rdf_format: str,
                 destination: str) -> None:
        self._glob_pattern: str = glob_pattern
        self._rdf_format: str = rdf_format
        self._destination: str = destination
        self._shape = Graph()
        self._shape.bind('sh', SHACL)
        self._shape.bind('rml', RML)
        self._shape.bind('rmls', RMLS)
        # Register TurtleWithPrefixes serializer as 'tortoise' format
        plugin.register('tortoise',
                        plugin.Serializer,
                        'generate_shape',
                        'TurtleWithPrefixes')

    def generate(self) -> None:
        """
        Generate a full shape from the sub shapes.
        """
        print('Reading subshapes:')
        for sub_shape in glob(self._glob_pattern):
            if 'star.ttl' in sub_shape:
                continue
            print(f"\t{sub_shape}")
            g = Graph()
            g.bind('sh', SHACL)
            g.bind('rml', RML)
            g.bind('rmls', RMLS)
            self._shape += g.parse(sub_shape, format=self._rdf_format)

        print(f'Writing shape to {self._destination}')
        self._shape.serialize(destination=self._destination, format='tortoise')


if __name__ == '__main__':
    p = argparse.ArgumentParser(description='Generate a complete SHACL shape '
                                'from the subshapes.')
    p.add_argument('destination', type=str, help='Location to write the '
                   'complete SHACL shape as Turtle.')
    # Arguments parsing
    args = p.parse_args()
    if not path.exists(args.destination):
        print(f'{args.destination} file path does not exist!')
        sys.exit(1)

    if path.isdir(args.destination):
        args.destination = path.join(args.destination, 'star.ttl')

    # Generate shape
    generator = ShapeGenerator(SUBSHAPE_GLOB_PATTERN, SUBSHAPE_FORMAT,
                               args.destination)
    generator.generate()
