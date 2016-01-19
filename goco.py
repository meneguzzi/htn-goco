#
#  goco.py - The Goal+Commitment planning framework preprocessor
#  htn-goco
#
#  Created by Felipe Meneguzzi on 2016-01-19.
#  Copyright 2016 Felipe Meneguzzi. All rights reserved.
#

import re
from optparse import OptionParser

class Commitment:
    def __init__(self,(cid,debtor,creditor,antecedent,consequent)):
        self.cid = cid
        self.debtor = debtor
        self.creditor = creditor
        self.antecedent = antecedent
        self.consequent = consequent
        
    def __str__(self):
        return str(self.cid)+"("+str(self.debtor)+", "+str(self.creditor)+", "+str(self.antecedent)+", "+str(self.consequent)+")"
    
    def tuple(self):
        return (self.cid,self.debtor,self.creditor,self.antecedent,self.consequent)
    
    def gen_lisp(self):
        comment = ";"+str(self)
        antecedent = "(:- (p ?c %s (?t)) (and (commitment ?c ?ci ?d ?a) (var ?c ?ci (?t)) (%s))" % (self.cid,GoCo.lispify(self.antecedent))
        consequent = "(:- (q ?c %s (?t)) (and (commitment ?c ?ci ?d ?a) (var ?c ?ci (?t)) (%s))" % (self.cid,GoCo.lispify(self.consequent))
        
        return comment+"\n"+antecedent+"\n"+consequent

class GoCo:
    def __init__(self):
        self.commitments = dict()
    
    def parse_file(self, filename):
        f = open(filename,'r')
        text = f.read() #FIXME Deal with reading very large files
        print text
        # commTuples = re.findall(r"""
#             \s*(C.) # Commitment id
#             \((\w+) # Debtor
#             ,\s*(\w+) # Creditor
#             ,\s*(.+) # Antecedent
#             ,\s*(.+) # Consequent
#             \)""",text)
        commTuples = re.findall("\s*(C.*)\((\w+),\s*(\w+),\s*(.+),\s*(.+)\)",text)
        print commTuples
        
        for c in commTuples:
            com = Commitment(c)
            self.commitments[com.cid] = com
    
    @classmethod
    def lispify(self, expr):
        """ Transforms an expression into a LISP-like expression""" # TODO Implement this
        return expr
    
    def generate_commitment_rules(self):
        """ Generate the logical rules for the commitments"""
        r = ""
        for cid in self.commitments:
            r+=self.commitments[cid].gen_lisp()+"\n"
        return r
            
            


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-d", "--dir-output", dest="output", action="store", type="string",
                      help="write reports to DIR", metavar="DIR")
    parser.add_option("-q", "--quiet",
                      action="store_false", dest="verbose", default=True,
                      help="don't print status messages to stdout")
    
    (options, args) = parser.parse_args()
    print options
    print args
    
    goco = GoCo()
    # goco.parse_file(args[0])
    goco.parse_file('healthcare.goco')
    print goco.generate_commitment_rules()
    