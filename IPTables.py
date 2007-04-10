#!/usr/bin/env python
#
# iptables class for python

import commands
import re
import string

class IPTablesError:
  def __init__(self, value):
    self.value=value
  def __str__(self):
    return `self.value`
    
class IPTablesRule:
  Packets = None
  Bytes = None
  Target = None
  Protocol = None
  Flags = None
  Source = None
  SourcePorts = None
  SourceIF = None
  Dest = None
  DestPorts = None
  DestIF = None
  State = None
  ToSource = None
  ToDest = None
    
class IPTablesChain:
  Chain = None
  Table = None
  Policy = None
  Packets = 0
  Bytes = 0
  Rules = []
  def __init__(Self,Chain,Table='filter'):
    Self.RuleMatch=re.compile('^[ \t]*[0-9]+')
    Self.Chain=Chain
    Self.Table=Table
    
  def __filter__(Self,Line):
    return Self.RuleMatch.search(Line) != None
    
  def __mkcmd__(Self,Cmd,Rule):
    if Rule.Target:
      Cmd=Cmd+' -j "%s"' % Rule.Target
    if Rule.Protocol:
      Cmd=Cmd+' -p "%s"' % Rule.Protocol
    if Rule.Flags:
      Cmd=Cmd+' %s' % Rule.Flags
    if Rule.SourceIF:
      Cmd=Cmd+' -i "%s"' % Rule.SourceIF
    if Rule.DestIF:
      Cmd=Cmd+' -o "%s"' % Rule.DestIF
    if Rule.Source:
      Cmd=Cmd+' -s "%s"' % Rule.Source
    if Rule.Dest:
      Cmd=Cmd+' -d "%s"' % Rule.Dest
    if Rule.Protocol in ("tcp","udp"):
      if Rule.SourcePorts:
        Cmd=Cmd+' --sport "%s"' % Rule.SourcePorts
      if Rule.DestPorts:
        Cmd=Cmd+' --dport "%s"' % Rule.DestPorts
    if Rule.State:
      Cmd=Cmd+' -m state --state "%s"' % Rule.State
    if Rule.ToSource:
      Cmd=Cmd+' --to-source "%s"' % Rule.ToSource
    if Rule.ToDest:
      Cmd=Cmd+' --to-destination "%s"' % Rule.ToDest
    return Cmd
    
  def appendRule(Self,Rule):
    """Append a new rule.
    
    Appends the rule *Rule* to the selected chain.
    """
    Cmd=Self.__mkcmd__('iptables -t "%s" -A "%s"' % (Self.Table, Self.Chain),Rule)
    Status, Output = commands.getstatusoutput(Cmd)
    if Status:
      raise IPTablesError(Output)
    
  def count(Self):
    """Count chain rules.
    
    Returns the number of rules in the chain. Remember to call the refresh()
    method to keep the rule list of the chain up to date.
    """
    return len(Self.Rules)  
    
  def deleteRuleIndex(Self,Index):
    """Delete a rule by index.
    
    Delete the rule with index *Index*.
    """
    Status, Output = commands.getstatusoutput('iptables -t "%s" -D "%s" %i'
      % (Self.Table, Self.Chain, Index+1))
    if Status:
      raise IPTablesError(Output)

  def deleteRule(Self,Rule):
    """Delete a rule.
    
    Deletes the rule *Rule* from the selected chain.
    """
    Cmd=Self.__mkcmd__('iptables -t "%s" -D "%s"' % (Self.Table, Self.Chain),Rule)
    Status, Output = commands.getstatusoutput(Cmd)
    if Status:
      raise IPTablesError(Output)
      
  def findRule(Self,Match):
    """Return Index of matching rule
    
    Returns the index of the chain rule that matches the rule 
    specified with *Match*. Returns -1 if rule was not found.
    """
    Count=0
    for Rule in Self.Rules:
      if Rule.Target==Match.Target and Rule.Protocol==Match.Protocol and Rule.Flags==Match.Flags and Rule.SourceIF==Match.SourceIF and Rule.DestIF==Match.DestIF and Rule.Source==Match.Source and Rule.Dest==Match.Dest:
        return Count
      Count=Count+1
    return -1
    
  def getRule(Self,Index):
    """Return Rule object.
    
    Return Rule object with index *Index*. Remember to call the refresh()
    method to keep the rule list of the chain up to date.
    """
    return Self.Rules[Index]
    
  def insertRule(Self,Index,Rule):
    """Insert a new rule."
    
    Insert the new rule *Rule* at index *Index*.
    """
    Cmd=Self.__mkcmd__('iptables -t "%s" -I "%s" %i' 
      % (Self.Table, Self.Chain, Index+1),Rule)
    Status, Output = commands.getstatusoutput(Cmd)
    if Status:
      raise IPTablesError(Output)

  def refresh(Self,Zero=0):
    """Refresh chain data.
    
    Refreshes chain data (Packet and byte counters, chain policy, rules).
    You need to call this method every time you need up-to-date informations
    from the chain. This data is not loaded or modified automatically to 
    increase performance. If *Zero* is 1 than the chains counters are
    zeroed after they have been read.
    """
    if Zero:
      Status, Output = commands.getstatusoutput('iptables -vnx -t "%s" -Z -L "%s"'
        % (Self.Table, Self.Chain))
    else:
      Status, Output = commands.getstatusoutput('iptables -vnx -t "%s" -L "%s"'
        % (Self.Table, Self.Chain))
    if Status:
      raise IPTablesError(Output)
    Lines=string.split(Output,'\n')
    Lines=filter(Self.__filter__,Lines)
    Items=string.split(Lines[0])
    Self.Policy=Items[3];
    Self.Packets=Items[4];
    Self.Bytes=Items[6];
    Self.Rules=[]
    for Line in Lines:
      Items=string.split(string.strip(Line))
      Rule=IPTablesRule()
      Rule.Packets=Items[0]
      Rule.Bytes=Items[1]
      if len(Items)==9:
        Rule.Target=Items[2]
        Rule.Protocol=Items[3]
        Rule.Flags=Items[4]
        Rule.SourceIF=Items[5]
        Rule.DestIF=Items[6]
        Rule.Source=Items[7]
        Rule.Dest=Items[8]
      else:
        Rule.Target=None
        Rule.Protocol=Items[2]
        Rule.Flags=Items[3]
        Rule.SourceIF=Items[4]
        Rule.DestIF=Items[5]
        Rule.Source=Items[6]
        Rule.Dest=Items[7]
      if Rule.Protocol=="all":
        Rule.Protocol=None
      if Rule.Flags=="--":
        Rule.Flags=None
      if Rule.SourceIF=="*":
        Rule.SourceIF=None
      if Rule.DestIF=="*":
        Rule.DestIF=None
      Self.Rules.append(Rule)
      
  def replaceRule(Self,Index,Rule):
    """Replace a rule."
    
    Replace the rule at index *Index* with *Rule*.
    """
    Cmd=Self.__mkcmd__('iptables -t "%s" -R "%s" %i' 
      % (Self.Table, Self.Chain, Index+1),Rule)
    Status, Output = commands.getstatusoutput(Cmd)
    if Status:
      raise IPTablesError(Output)
    
def __filter__(Line):
  return ChainMatch.search(Line) != None

def __map__(Line):
  return string.split(Line,None,2)[1]
    
def createChain(Chain, Table='filter'):
  """Create a new chain.
    
  Creates a new chain with the name *Chain* in the table *Table*.
  """
  Status, Output = commands.getstatusoutput('iptables -t "%s" -N "%s"' 
    % (Table, Chain))
  if Status:
    raise IPTablesError(Output)    

def deleteChain(Chain, Table='filter'):
  """Delete a chain.
  
  Deletes the chain with the name *Chain* from the table *Table*.
  """
  Status, Output = commands.getstatusoutput('iptables -t "%s" -X "%s"' 
    % (Table, Chain))
  if Status:
    raise IPTablesError(Output)    

def deleteChains(Table='filter'):
  """Delete all chains.
  
  Deletes all user defined chains from the table *Table*.
  """
  Status, Output = commands.getstatusoutput('iptables -t "%s" -X'
    % (Table))
  if Status:
    raise IPTablesError(Output)    

def flushChain(Chain, Table='filter'):
  """Flush a chain.
  
  Flushes the chain with the name *Chain* in the table *Table*. This
  is equivalent to deleting all rules of this chain one by one.
  """
  Status, Output = commands.getstatusoutput('iptables -t "%s" -F "%s"' 
    % (Table, Chain))
  if Status:
    raise IPTablesError(Output)    

def flushChains(Table='filter'):
  """Flush all chains.
  
  Flushes all chains in the table *Table*.
  """
  Status, Output = commands.getstatusoutput('iptables -t "%s" -F' 
    % (Table))
  if Status:
    raise IPTablesError(Output)    

def getChains(Table='filter'):
  """Return chain names.
   
  Returns a sequence containing all chain names of the table *Table*.
  """
  Status, Output = commands.getstatusoutput('iptables -n -t "%s" -L' % (Table))
  if Status:
    raise IPTablesError(Output)
  Lines=string.split(Output,'\n')
  return map(__map__,filter(__filter__,Lines))
  
def getChain(Chain,Table='filter'):
  """Return a Chain object.
  
  Returns te Chain object *Chain* of the table *Table*.
  """
  return IPTablesChain(Chain,Table);

def renameChain(Chain, NewChain, Table='filter'):
  """Renames a chain.
    
  Rename the chain *Chain* in the table *Table* in *NewChain*.
  """
  Status, Output = commands.getstatusoutput(
    'iptables -t "%s" -E "%s" "%s"' % (Table,Chain,NewChain))
  if Status:
    raise IPTablesError(Output)    

def setPolicy(Chain, Policy, Table='filter'):
  """Set policy.
  
  Sets the policy of the chain *Chain* in the table *Table* to *Policy*.
  """
  Status, Output = commands.getstatusoutput(
    'iptables -t "%s" -P "%s" "%s"' % (Table,Chain,Policy))
  if Status:
    raise IPTablesError(Output)
    
def zeroChain(Chain, Table='filter'):
  """Zero a chain.
  
  Zero the packet and byte counters of the chain *Chain* in the table *Table*.
  """
  Status, Output = commands.getstatusoutput('iptables -t "%s" -Z "%s"' 
    % (Table, Chain))
  if Status:
    raise IPTablesError(Output)    

def zeroChains(Table='filter'):
  """Zero all chains.
    
  Zeros packet and byte counters of all chains in the table *Table*.
  """
  Status, Output = commands.getstatusoutput('iptables -t "%s" -Z' 
    % (Table))
  if Status:
    raise IPTablesError(Output)    

ChainMatch=re.compile("^Chain")
