#!/usr/bin/env python3

__author__ = 'cjm'

import argparse
import logging
import re
import yaml

def main():

    parser = argparse.ArgumentParser(description='DOSDB'
                                                 'fooo',
                                     formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('-t', '--to', type=str, required=False,
                        help='Renderer')
    parser.add_argument('-p', '--pattern', type=str, required=False,
                        help='YAML Pattern file')
    args = parser.parse_args()

    f = open(args.pattern, 'r') 
    tobj = yaml.load(f)
    bindings = {'imported': 'foo'}
    iri = 'x'
    print('Ontology: foo')
    apply_pattern(tobj, bindings, iri)
    

def get_values(tobj, bindings):
    lvars = tobj['vars']
    vals = []
    for v in lvars:
        vals.append(bindings[v])
    return vals

def apply_template(tobj, bindings):
    textt = tobj['text']
    vals = get_values(tobj, bindings)
    text = format(textt % tuple(vals))
    return text

def apply_pattern(p, bindings, iri):
    # build map of quoted entity replacements
    qm = {}
    for k in p['classes']:
        qm[k] = p['classes'][k]
    for k in p['relations']:
        qm[k] = p['relations'][k]
    print('Class: %s' % iri)
    if 'name' in p:
        tobj = p['name']
        text = apply_template(tobj, bindings)
        print(' Annotations: rdfs:label "%s"' % text)
    if 'def' in p:
        tobj = p['def']
        text = apply_template(tobj, bindings)
        # todo: protect against special characters
        print(' Annotations: IAO:0000115 "%s"' % text)
    if 'equivalentTo' in p:
        tobj = p['equivalentTo']
        text = apply_template(tobj, bindings)
        expr = replace_quoted_entities(qm, text)
        print(' EquivalentTo: %s' % expr)
    if 'subClassOf' in p:
        tobj = p['subClassOf']
        text = apply_template(tobj, bindings)
        expr = replace_quoted_entities(qm, text)
        print(' EquivalentTo: %s' % expr)

# Stolen from DOS' code
def replace_quoted_entities(qm, text):
    for k in qm:
        v = qm[k]
        text = re.sub("\'"+k+"\'", v, text)  # Suspect this not Pythonic. Could probably be done with a fancy map lambda combo.  
    return text



if __name__ == "__main__":
    main()
