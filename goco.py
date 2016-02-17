#
#  goco.py - The Goal+Commitment planning framework preprocessor
#  htn-goco
#
#  Created by Felipe Meneguzzi on 2016-01-19.
#  Copyright 2016 Felipe Meneguzzi. All rights reserved.
#

import re
from optparse import OptionParser
from __builtin__ import str

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
        antecedent = "(:- (p ?c %s (?t)) (and (commitment ?c ?ci ?d ?a) (var ?c ?ci (?t)) %s))" % (self.cid, lispify(self.antecedent))
        consequent = "(:- (q ?c %s (?t)) (and (commitment ?c ?ci ?d ?a) (var ?c ?ci (?t)) %s))" % (self.cid, lispify(self.consequent))
        
        return comment+"\n"+antecedent+"\n"+consequent+"\n"

class Goal:
    def __init__(self,(gid,agent,precond,success,failure)):
        self.gid = gid
        self.agent = agent
        self.precond = precond
        self.success = success
        self.failure = failure
    
    def __str__(self):
        return str(self.gid)+"("+str(self.agent)+", "+str(self.precond)+", "+str(self.success)+", "+str(self.failure)+")"

    def tuple(self):
        return (self.gid,self.agent,self.precond,self.success,self.failure)
    
    def gen_lisp(self):
        comment = ";"+str(self)
        precond = "(:- (pg ?g %s (?t)) (and (goal ?g ?gi ?a) (var ?g ?gi (?t)) %s)" % (self.gid, lispify(self.precond))
        success = "(:- (s ?g %s (?t)) (and (goal ?g ?gi ?a) (var ?g ?gi (?t)) %s)" % (self.gid, lispify(self.success))
        failure = "(:- (f ?g %s (?t)) (and (goal ?g ?gi ?a) (var ?g ?gi (?t)) %s)" % (self.gid, lispify(self.failure))
        
        return comment+"\n"+precond+"\n"+success+"\n"+failure+"\n"

class GoCo:
    def __init__(self):
        self.commitments = dict()
        self.goals = dict()
    
    def parse_file(self, filename):
        f = open(filename,'r')
        text = f.read() #FIXME Deal with reading very large files
        # print text
        self.parse_commitments(text)
        self.parse_goals(text)
        
    
    def parse_commitments(self,text):
                # commTuples = re.findall(r"""
        #             \s*(C.) # Commitment id
        #             \((\w+) # Debtor
        #             ,\s*(\w+) # Creditor
        #             ,\s*(.+) # Antecedent
        #             ,\s*(.+) # Consequent
        #             \)""",text)
        commTuples = re.findall("\s*(C.*)\((\w+),\s*(\w+),\s*(.+),\s*(.+)\)",text)
#         print commTuples
        
        for c in commTuples:
            com = Commitment(c)
            self.commitments[com.cid] = com
    
    def parse_goals(self,text):
        goalTuples = re.findall("\s*(G.*)\((\w+),\s*(\w+),\s*(.+),\s*(.+)\)", text)
        for g in goalTuples:
            goal = Goal(g)
            self.goals[goal.gid] = goal
    
    def generate_commitment_rules(self):
        """ Generate the logical rules for the commitments"""
        r = ""
        for cid in self.commitments:
            r+=self.commitments[cid].gen_lisp()+"\n"
        return r
    
    def generate_goal_rules(self):
        pass

def parse_expresion(expr, root=None):
    """Parses an expression in the GoCo grammar -- Right now, VERY limited TODO create a decent parser for this"""
    if(expr==""): return None
    
    tokens = re.findall("\s*(-?\w+(\([\w+,?]*\))?|(\s*\^))",expr)
    print "Tokens: ",tokens
    
    return tokens

def lispify(expr):
    """ Transforms an expression into a LISP-like expression""" # TODO Implement this
    tokens = parse_expresion(expr)
    
    lisp_expr = "("
    
    if("v" in (t[0] for t in tokens)):
        lisp_expr += "or "
    else:
        lisp_expr += "and "
    
    for pred,terms,_ in tokens:
        if pred is not '^':
            negated = False
            if(pred[0]=='-'): 
                lisp_expr+="(not "
                pred = pred[1:]
                negated = True
            if terms is "": 
                lisp_expr+=pred
            else:
                pred = pred[:pred.find("(")]
#                 print pred
                lisp_expr+="("+pred+" "
                for t in re.findall("(\w+)", terms):
                    if t[0].isupper():
                        lisp_expr+="?"
                    lisp_expr+=t+" "
                lisp_expr=lisp_expr[:-1]+")"
                
            if(negated): lisp_expr+=")"
            
            lisp_expr+=" "
    lisp_expr = lisp_expr[:-1]+")"
    
    return lisp_expr


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
    