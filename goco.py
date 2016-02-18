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
import logging as log

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
    
    #TODO use a settings file to configure this
    generic_axioms_file = "axioms.jshop"
    generic_operators_file = "operators.jshop"
    domain_template_file = "domain-template.jshop"
     
    def __init__(self):
        self.commitments = dict()
        self.goals = dict()
    
    def parse_file(self, filename):
        f = open(filename,'r')
        text = f.read() #FIXME Deal with reading very large files
        # print text
        self.parse_commitments(text)
        self.parse_goals(text)
    
    def read_text_file(self,filename):
        f = open(filename, 'r')
        text = f.read()#FIXME Deal with reading very large files
        return text
    
    def generate_jshop_domain(self,input_file=None,operators_file=None):
        """ Generates the JSHOP source code for a GoCo domain"""
        domain_name = "goco"
        domain_operators = ""
        output_file=None
        if(input_file is not None):
            #assert(isinstance(input_file, string))
            assert(input_file.find(".goco") > 0)
            domain_name = input_file[:input_file.find(".goco")]
            self.parse_file(input_file)
            assert(len(self.commitments)+len(self.goals) > 0)
            output_file = domain_name+".jshop"
        
        if(operators_file is not None):
            domain_operators = self.read_text_file(operators_file)
        
        domain_source = self.read_text_file(self.domain_template_file)
        axioms_source = self.read_text_file(self.generic_axioms_file)
        operators_source = self.read_text_file(self.generic_operators_file)
        
        domain_axioms = self.generate_commitment_rules()+self.generate_goal_rules()
        
        output = domain_source % (domain_name,axioms_source,domain_axioms,operators_source,domain_operators)
        if(output_file == None):
            print "Outputting to std out"
            print output
        else:
            print "Writing domain to %s " % output_file
            f = open(output_file, 'w')
            f.write(output)
            f.close()
        
    
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
        r = ""
        
        for gid in self.goals:
            r+=self.goals[gid].gen_lisp()+"\n"
            
        return r

def parse_expresion(expr, root=None):
    """Parses an expression in the GoCo grammar -- Right now, VERY limited TODO create a decent parser for this"""
    if(expr==""): return None
    
    tokens = re.findall("\s*(-?\w+(\([\w+,?]*\))?|(\s*\^))",expr)
    #print "Tokens: ",tokens
    
    return tokens

def lispify(expr):
    """ Transforms an expression into a LISP-like expression"""
    # TODO Implement this properly, as this is pretty hacky right now
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
    parser.add_option("-p", "--operators", dest="operators", action="store", type="string",
                      help="read domain specific operators from FILE", metavar="FILE")
    parser.add_option("-d", "--dir-output", dest="output", action="store", type="string",
                      help="write reports to DIR", metavar="DIR")
    parser.add_option("-q", "--quiet",
                      action="store_false", dest="verbose", default=True,
                      help="don't print status messages to stdout")
    
    (options, args) = parser.parse_args()
    
    if(options.quiet):
        log.info("Suppressing most output")
        log.basicConfig(format="%(levelname)s: %(message)s", level=log.CRITICAL)
    elif(options.verbose):
        log.info("Verbose output."):
        log.basicConfig(format="%(levelname)s: %(message)s", level=log.INFO)
    else(not options.quiet):
        log.basicConfig(format="%(levelname)s: %(message)s", level=log.WARNING)
    
    if(len(args)==0):
        log.critical("Must supply a filename with goals and commitments")
    
    
    goco = GoCo()
    #goco.parse_file(args[0])
    #goco.parse_file('healthcare.goco')
    # print goco.generate_commitment_rules()
    goco.generate_jshop_domain(args[0],options.operators)
    