import os
from reprlib import recursive_repr
from traitclass import Trait, TraitLevel, TraitLevelEffect
from triggerclass import Trigger, TriggerAffect
from utils import strlist, fulcom_re, whitel_re, trait_re, trigg_re
        
class EDCT():
    EDCT_fname = "export_descr_character_traits.txt"
    
    def __init__(self):
        self.Nwhite = 0
        self.Ntriggers = 0
        self.Ntraits = 0
        self.Nfulcom = 0
        self.Ntot = 0
        self.traits = strlist()
        self.triggers = strlist()
        self.current_view = strlist()
        self.edct_file = None
        self.comment_header = ""
        
    @recursive_repr()
    def __repr__(self):
        return "Traits: {:g} \n".format(self.Ntraits) + "\n".join(map(repr, self.traits)) + "Triggers: {:g} \n".format(self.Ntriggers) + "\n".join(map(repr, self.triggers))
    
    def update_names(self):
        self.traits.update_names()
        self.triggers.update_names()
        
    def parse_edct(self, folder):
        self.__init__()
        
        self.edct_file = folder
        edct = open(folder, "r",   encoding="utf8")
        parseTrait = False
        parseTrigg = False

        for l in edct:
            self.Ntot+=1
            if(fulcom_re.match(l)):
                self.Nfulcom+=1
            if(whitel_re.match(l)):
                # skip whitelines
                self.Nwhite+=1
                continue

            if((not parseTrait) and (not parseTrigg)):
                if(fulcom_re.match(l)):
                    # add full lines to fulcom
                    self.comment_header = self.comment_header + l
                    continue
            
            trait_ma = trait_re.match(l)
            
            if(trait_ma):
                parseTrait = True
                parseTrigg = False
                self.Ntraits+=1
                newtrait = Trait(trait_ma.group(1), trait_ma.group(2))
                self.traits.append(newtrait)
                continue
                
            if(parseTrait):
                parsed = newtrait.parse_line(l)
                if(parsed): continue
            
            trigg_ma = trigg_re.match(l)
            if(trigg_ma):
                parseTrait = False
                parseTrigg = True
                self.Ntriggers+=1
                #if(self.Ntriggers >1): print(newtrigg)
                newtrigg = Trigger(trigg_ma.group(1), trigg_ma.group(2))
                self.triggers.append(newtrigg)
                continue
                
            if(parseTrigg):
                newtrigg.parse_line(l)
                continue

            # if we are here, something is wrong
            print("ERROR: can't parse line\n{:s}".format(l))
                
        
        self.update_names()
        print("-- Total lines {:d}".format(self.Ntot))
        print("-- White lines skipped: {:d}".format(self.Nwhite))
        print("-- Full line comments found: {:d}".format(self.Nfulcom))
        print("-- Traits recorded: {:d}".format(self.Ntraits))
        print("-- Triggers recorded: {:d}".format(self.Ntriggers))
        edct.close()
    
    ###########################################################################
    ###                                 Filters                             ###
    ###########################################################################
    
    def affects_traits(self, targ_trait):
        # Returns a list of Traits that "targ_trait" affects (i.e. targ_trait present in the conditions)
        # For each Trait in the list returns the associated Triggers in which the Trait is affected
        if((not self.Ntraits) or (not self.Ntriggers)):
            return {}
        affects = {}
        
        for trig in self.triggers:
            hasit = False
            for cond in trig.conditions:
                lcond = cond.cond.split()
                if(len(lcond)!=1):
                    if((lcond[0] == "Trait") and (targ_trait == lcond[1])):
                        hasit = True
                        break
                    elif((lcond[1] == "Trait") and (targ_trait == lcond[2])):
                        hasit = True
                        break
                    
            if(hasit):
                for aff in trig.affects:
                    affects.setdefault(aff.aff, []).append(trig.name)
        return affects
        
    def is_affected_traits(self, targ_trait):
        # Returns a list of Traits that affects "targ_trait" (i.e. Trait is present in the conditions affecting targ_trait)
        # Also for each Trait in the list returns the associated Triggers in which "targ_trait" is affected
        if((not self.Ntraits) or (not self.Ntriggers)):
            return {}
        affected = {}
        
        for trig in self.triggers:
            hasit = False
            for aff in trig.affects:
                if(targ_trait == aff.aff):
                    hasit = True
                    break
            if(hasit):
                for cond in trig.conditions:
                    lcond = cond.cond.split()
                    if(len(lcond)!=1):
                        if(lcond[0] == "Trait"):
                            affected.setdefault(lcond[1], []).append(trig.name)
                        elif(lcond[1] == "Trait"):
                            affected.setdefault(lcond[2], []).append(trig.name)
        return affected
        
    def is_affected_triggers(self, targ_trait):
        # Returns a list of Triggers that affect "targ_trait"
        if((not self.Ntraits) or (not self.Ntriggers)):
            return []
        affected = []
        
        for trig in self.triggers:
            hasit = False
            for aff in trig.affects:
                if(targ_trait == aff.aff):
                    affected.append(trig.name)
                    break

        # remove duplicates (not needed)
        # seen = set()
        # return [seen.add(x) or x for x in affected if(x not in seen)]
        return affected
    
    ###########################################################################
    ###                            END  Filters                             ###
    ###########################################################################
    
    def get_trait(self, name):
        try:
            it = self.traits.names.index(name)
            return self.traits[it]
        except ValueError:
            print("ERROR: not present")

    def reload(self):
        if(not self.edct_file):
            print("ERROR: file not specified")
            return
        if(not os.path.isfile(self.edct_file)):
            print("ERROR: file not found")
            return
        self.parse_edct(self.edct_file)

    def save(self, fname):
        f = open(fname, "w")
        f.write(self.comment_header)
        for tt in edcteb2.traits:
            f.write(tt.as_string())
        for tt in edcteb2.triggers:
            f.write(tt.as_string())
        f.close()



if __name__ == "__main__":
    edcteb2 = EDCT()
    edcteb2.parse_edct(edcteb2.EDCT_fname)
    #print(edcteb2.traits[0].comment_head)
    for tt in edcteb2.triggers:
        for x in tt.comment_dict.items():
            if(x[0].startswith("a")):
                #print(x)
                pass
        #print(tt.comment_dict, end='')
        #print(tt.as_string())
    #for tt in edcteb2.triggers:
        #print(tt.name)
    #    print(tt.comment_head, end='')
    #    print(tt.as_string())
    edcteb2.save("test.txt")
        #print(edcteb2.traits)
#print(edcteb2.triggers[0]) #.as_string())
