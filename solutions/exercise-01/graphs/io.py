from . import Graph

import re
from html.entities import codepoint2name

NTRIPLES_PATTERN = re.compile(
    r'\s*'.join([r'^',
                  r'<(?P<subj>[^>]*)>',
                  r'<(?P<pred>[^>]*)>',
                  r'<(?P<obj>[^>]*)>',
                  r'.',
                  r'$']))
ENTITIES = str.maketrans({
    codepoint: '&{};'.format(name)
    for codepoint, name in codepoint2name.items()
})


def read_edge_list_graph(infile):
    "parse an edge-list formatted graph from `infile`"
    num_vertices = int(infile.readline())
    graph = Graph(range(num_vertices))

    for line in infile:
        source, target = line.split(' ')
        graph.add_edge(int(source), int(target))

    return graph


def write_metis_graph(outfile, graph):
    "write `graph` to `outfile`, in METIS format"
    print('{} {}'.format(graph.number_of_vertices,
                           graph.number_of_edges),
          file=outfile)

    for source in graph.vertices:
        if graph.out_degree(source) > 0:
            print(source,                # source vertex first
                  *graph.edges[source],  # then all target vertices
                  sep=' ',               # separated by a space
                  file=outfile)


def escape_html_entities(string):
    "replace known unicode codepoints in `string` with named HTML entities."
    return string.translate(ENTITIES)


def read_ntriples_graph(infile):
    "read a graph in N-Triples format from `infile`"
    graph = Graph([])

    for line in infile:
        match = NTRIPLES_PATTERN.match(line.strip())

        if match is None:
            print("line `{}' not readable.".format(line.strip()))
            continue

        graph.add_vertex(match['subj'])
        graph.add_vertex(match['obj'])
        graph.add_edge(source=match['subj'],
                       label=match['pred'],
                       target=match['obj'])

    return graph


def write_ntriples_graph(outfile, graph):
    "write `graph` to `outfile`, in N-Triples format"
    for subj in graph.vertices:
        if graph.out_degree(subj) > 0:
            for (pred, obj) in graph.edges[subj]:
                print('<{}> <{}> <{}> .'.format(
                    subj, pred, obj),
                      file=outfile)
