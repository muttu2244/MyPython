#!/usr/bin/env python2.5
import sys, re
from logging import getLogger
from misc import pretty_print

log = getLogger()

#exclusion rules (global)
#case topo: [{cctsvcs1} [mod1] [encap1] [[cctsvcs2]] [mod2] [encap2] [portcfg]
#           [ {},         ".*",  ".*",     {},          ".*",  ".*",    ".*"],
#cctsvcs are lists, so their rules are dictionaries with the
#possible keys "is", "isnt", "has", "sans", values are lists
#All other fields are just regexps to be applied
rules = [

#cant route v4 to v6 in any form
    [ {}, ".*", "v6",     {}, ".*", "(?!v6)", ".*"],
    [ {}, ".*", "(?!v6)", {}, ".*", "v6",     ".*"],

#cant have an ipsec cct without ipsec cfg'd on cct
    [ {"sans": "service ipsec"}, ".*", "ipsec.*", {},                        ".*", ".*",      ".*"],
    [ {},                        ".*", ".*",      {"sans": "service ipsec"}, ".*", "ipsec.*", ".*"],

#cant have pppoe without service pppoe on cct
    [ {"sans": "service pppoe"}, ".*", "pppoe", {},                        ".*", ".*",      ".*"],
    [ {},                        ".*", ".*",      {"sans": "service pppoe"}, ".*", "pppoe", ".*"],
    
#cant mix dot1q and non-dot1q on same port or for same vlan case
    [ {}, "dot1q.*", ".*", {}, "raw",     ".*", "(same port|same vlan)"],
    [ {}, "raw",     ".*", {}, "dot1q.*", ".*", "(same port|same vlan)"],
    
#on same port, must have identical service types for non-vlan

#(revised... in 3.0 cant have ipsec and pppoe on same port, even diff vlan)
    [ {"is" : ["service pppoe"]},          ".*",  ".*", {"is" : ["service ipsec"]},           ".*",  ".*",    "same port"],
    [ {"is" : ["service ipsec"]},          ".*",  ".*", {"is" : ["service pppoe"]},           ".*",  ".*",    "same port"],    

    [ {"is" : ["none"]},          "raw",  ".*", {"isnt" : ["none"]},           ".*",  ".*",    "same port"],
    [ {"is" : ['service ipsec']}, "raw",  ".*", {"isnt" : ['service ipsec']},  ".*",  ".*",    "same port"],
    [ {"is" : ['service pppoe']}, "raw",  ".*", {"isnt" : ['service pppoe']},  ".*",  ".*",    "same port"],

#same issue applies to dot1 unassigned on same port
    [ {"is" : ["none"]},          "dot1q untagged",  ".*", {"isnt" : ["none"]},           "dot1q untagged",  ".*",    "same port"],
    [ {"is" : ['service ipsec']}, "dot1q untagged",  ".*", {"isnt" : ['service ipsec']},  "dot1q untagged",  ".*",    "same port"],
    [ {"is" : ['service pppoe']}, "dot1q untagged",  ".*", {"isnt" : ['service pppoe']},  "dot1q untagged",  ".*",    "same port"],

#same issue applies to dot1 same vlan case
    [ {"is" : ["none"]},          "dot1q",  ".*", {"isnt" : ["none"]},           "dot1q",  ".*",    "same vlan"],
    [ {"is" : ['service ipsec']}, "dot1q",  ".*", {"isnt" : ['service ipsec']},  "dot1q",  ".*",    "same vlan"],
    [ {"is" : ['service pppoe']}, "dot1q",  ".*", {"isnt" : ['service pppoe']},  "dot1q",  ".*",    "same vlan"],
    
#for same vlan case, both ccts must be dot1q
    [ {},          "dot1q untagged",  ".*", {},            "(?!dot1q untagged)",         ".*",    "same vlan"],
    [ {},          "(?!dot1q untagged)",         ".*", {},           "dot1q untagged",  ".*",    "same vlan"],
    [ {},          "(?!dot1q)",  ".*", {},           ".*",         ".*",    "same vlan"],
    [ {},          ".*",         ".*", {},           "(?!dot1q)",  ".*",    "same vlan"],

#per blessing, can use a plain egress port, as traffic is sent across fabric as pure IP
#so filter out any non-plain egress, except for "same port" or "same card" portcfg setting
#v4 cases
#     [ {"isnt" : ["none"]},  ".*",      ".*",     {},  ".*",  "(?!v6)",   "(?!(same port|same card|same vlan))"],
#     [ {},                   "(?!raw)", ".*",     {},  ".*",  "(?!v6)",   "(?!(same port|same card|same vlan))"],
#     [ {},                   ".*",      "(?!v4)", {},  ".*",  "(?!v6)",   "(?!(same port|same card|same vlan))"],

# #v6 cases
#     [ {"isnt" : ["none"]},  ".*",       ".*",      {},         ".*",  "v6",     "(?!(same port|same card|same vlan))"],
#     [ {},                   "(?!raw)",  ".*",      {},         ".*",  "v6",     "(?!(same port|same card|same vlan))"],
#     [ {},                   ".*",       "(?!v6)",  {},         ".*",  "v6",     "(?!(same port|same card|same vlan))"],

]

def enum_lists(setlist):
    return enum_lists_iter([],setlist)

def enum_lists_iter(accum, setlist):


    result_set = []
    curset = setlist[0]
    if len(setlist) == 1:
        for item in curset:
            #magic needs to happen here with filters
            append = accum + [item]
            result_set.append(append)
    else:
        for item in curset:
            result_set.extend(enum_lists_iter(accum + [item], setlist[1:]))
    return result_set


#must handle portscvs list, tricky
#contains match on cctsvcs only, regexp on others
def match_rule(item, rule):
    [cctsvcs1, mod1, encap1, cctsvcs2, mod2, encap2, portcfg] = item
    [rule_cctsvcs1, rule_mod1, rule_encap1, rule_cctsvcs2, rule_mod2, rule_encap2, rule_portcfg] = rule

    if "is" in rule_cctsvcs1.keys():
        if cctsvcs1 != rule_cctsvcs1["is"]:
            return False
    elif "isnt" in rule_cctsvcs1.keys():
        if cctsvcs1 == rule_cctsvcs1["isnt"]:
            return False
    elif "has" in rule_cctsvcs1.keys():
        for svc in cctsvcs1:
            if re.match(rule_cctsvcs1["has"], svc):
                break
        else:
            return False
    elif "sans" in rule_cctsvcs1.keys():
        for svc in cctsvcs1:
            if re.match(rule_cctsvcs1["sans"], svc):
                return False
        
    if not re.match(rule_mod1, mod1):
        return False
        
    if not re.match(rule_encap1, encap1):
        return False

    if "is" in rule_cctsvcs2.keys():
        if cctsvcs2 != rule_cctsvcs2["is"]:
            return False
    elif "isnt" in rule_cctsvcs2.keys():
        if cctsvcs2 == rule_cctsvcs2["isnt"]:
            return False
    elif "has" in rule_cctsvcs2.keys():
        for svc in cctsvcs2:
            if re.match(rule_cctsvcs2["has"], svc):
                break
        else:
            return False
    elif "sans" in rule_cctsvcs2.keys():
        for svc in cctsvcs2:
            if re.match(rule_cctsvcs2["sans"], svc):
                return False

    if not re.match(rule_mod2, mod2):
        return False
    if not re.match(rule_encap2, encap2):
        return False
    if not re.match(rule_portcfg, portcfg):
        return False

    return True




def pretty_print_list(test_list):
    toponum=0
    for item in test_list:
        pretty_print(toponum, item)
        toponum += 1
        
#         [cctsvc1, mod1, encap1, cctsvc2, mod2, encap2, portcfg] = item
#         print "Topo", toponum, item
#         toponum += 1
#         continue

# #need to clean up and make some nice prettyprinting here
#         print "Topo", toponum, "--------------------------"
#         print "Circuit 1"
#         print "Port services defined: ",
#         for svc in cctsvc1:
#             print svc,
#         print
#         print "Circuit encap modifier:", mod1
#         print "Encapsulation:", encap1
#         print "Connected via:", portcfg
#         print "Circuit 2"
#         print "Port services defined: ",
#         for svc in cctsvc2:
#             print svc,
#         print
#         print "Circuit encap modifier:", mod2
#         print "Encapsulation:", encap2


def gen_tests(portservice1, modifiers1, encaps1, portservice2, modifiers2, encaps2, portcfgs):

    setlist = [portservice1, modifiers1, encaps1, portservice2, modifiers2, encaps2, portcfgs]
    test_list = enum_lists(setlist)

    for item in test_list[:]:
        for rule in rules:
            if match_rule(item, rule):
                test_list.remove(item)
                break


#filter out dupes, where dupes are [cctsvc1] [mod1] [encap1] [cctsvc2] [mod2] [encap2] [portcfg]
#                                  [cctsvc2] [mod2] [encap2] [cctsvc1] [mod1] [encap1] [portcfg]

    def myindex(idx, item):
        for j in range(idx, len(test_list)):
            if test_list[j] == item:
                return j
        return 0

## filter dupes after applying rules, as we are relying on cct ordering with blessing's new filter rules
#
#this is ugly, but reasonably fast, no list copying
    for i in range(len(test_list)):
        if i == len(test_list):
            break
        [cctsvc1, mod1, encap1, cctsvc2, mod2, encap2, portcfg] = test_list[i]
        other = [cctsvc2, mod2, encap2, cctsvc1, mod1, encap1, portcfg]
        idx = myindex(i+1, other)
        if idx:
            del test_list[idx]

    return test_list




def main():

#cedar encaps/forwarding set
    encaps =['v4', 'v6', 'ipsec v44', 'ipsec v46', 'pppoe']
#    encaps =['v4', 'ipsec v44', 'ipsec v46', 'pppoe']
#    encaps =['v4', 'ipsec v44', 'ipsec v46']        
    modifiers = ['raw', 'dot1q', 'dot1q untagged']
    cctservices = [['none'], ['service ipsec'], ['service pppoe']]
#    cctservices = [['none'], ['service ipsec'],]    
    portcfgs = ['same vlan', 'same port', 'same card', 'different card']

#     #pre-cedar encap/forwarding set
#     encaps =['v4', 'ipsec v44', 'ipsec v46', ]
#     modifiers = ['raw',]
#     cctservices = [['none'], ['service ipsec']]
#     portcfgs = ['same port', 'same card', 'different card']



    test_list = gen_tests(cctservices, modifiers, encaps, cctservices, modifiers, encaps, portcfgs)
    pretty_print_list(test_list)



if __name__=="__main__":
    main()
