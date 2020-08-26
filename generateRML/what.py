import csv
import rdflib
from rdflib import *
import os

workGraph = Graph()
workGraph.load('file:bfOutput/workExample.nq', format='nquads')
workGraph.serialize(destination='bfOutput/workExample.ttl', format='turtle')

expressionGraph = Graph()
expressionGraph.load('file:bfOutput/expressionExample.nq', format='nquads')
expressionGraph.serialize(destination='bfOutput/expressionExample.ttl', format='turtle')

manifestationGraph = Graph()
manifestationGraph.load('file:bfOutput/manifestationExample.nq', format='nquads')
manifestationGraph.serialize(destination='bfOutput/manifestationExample.ttl', format='turtle')

itemGraph = Graph()
itemGraph.load('file:bfOutput/itemExample.nq', format='nquads')
itemGraph.serialize(destination='bfOutput/itemExample.ttl', format='turtle')
