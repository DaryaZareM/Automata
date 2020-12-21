


def decimalToBinary(n,l):  
    return list((l-len(bin(n).replace("0b", "")))*'0'+bin(n).replace("0b", ""))

def binaryToDecimal(s):
    b=0
    f=0
    for i in s:
        b+=int(i)*(2**f)
        f+=1
    return b
    

class NFA: 
    def __init__(self, states, states_number,alphabet, transition_function, t_function, start_state, accept_states):
        """[initial NFA machine]

        Arguments:
            states {[dict]} -- [all states of machine]
            alphabet {[dict]} -- [all alphabet of machine]
            transition_function {[list]} -- [edge of machine graph]
            start_state {[string]} -- [start state]
            accept_states {[dict]} -- [all accept states of machine]
            states_number {[int]} -- [number of states]
            t_function {[list]} -- [transition functin store in another type]
        """
        

      
        self.states = states
        self.states_number=states_number
        self.alphabet = alphabet
        self.transition_function = transition_function
        self.t_function = t_function
        print(self.t_function)
        self.start_state = start_state
        self.accept_states = accept_states
        self.new_accept_states=accept_states
        self.current_state = start_state
        self.remove_lambda()
    def remove_lambda(self):
        """[removin lambda from NFA machine]
        """
        """findin transition with lambda"""
        transitions_contains_lambda = list()
        for transition in self.transition_function:
            if transition[1]=='l':
                transitions_contains_lambda.append([transition[0],transition[1],self.transition_function[transition]])
                for fnstate in  self.transition_function[transition]:
                    if fnstate in accept_states:
                        
                        self.new_accept_states.update({transition[0]:transition[0]})
        
# x lambda y
        '''adding transitions that gose to a state that its lambda closer is not null'''
        # for each k that k==x
        for transition in transitions_contains_lambda:       
            for et in self.transition_function:
                for destination_of_tf in self.transition_function[et]:
                    if destination_of_tf == transition[0]:   
                        self.transition_function[(et[0],et[1])]+=(transition[2])
 
        '''adding transitions that start with vertex that its lambda closer is not null'''
        #for each k that k==y
        for transition in transitions_contains_lambda:
            for et in self.transition_function:
                for distance_of_transition in self.transition_function[(transition[0],transition[1])]:
                    if distance_of_transition == et[0]:
                        self.transition_function[(transition[0],et[1])]+=(self.transition_function[et])    




"""reading NFA from file"""      
filepath = 'NFA_Input_2.txt'  
with open(filepath,"r") as fp:
    l1 = fp.readline()
    ll1=l1[:len(l1)-1].split(" ")
    alphabet=list()
    for s in ll1:
        alphabet.append(s)
    alphabet.append('l')

    l2 = fp.readline()
    ll2=l2[:len(l2)-1].split(" ")
    states=dict()
    cn=0
    for a in ll2:
        states.update({a:cn})
        cn+=1
    
    l4 = fp.readline()
    start_state=states.get(l4[:len(l4)-1])
    
    l3 = fp.readline()
    ll3=l3[:len(l3)-1].split(" ")
    accept_states=dict()
    for a in ll3[:len(ll3)]:
        accept_states.update({states.get(a):states.get(a)})
    t_function=list()
    tf = dict()
    for  i in range (len(states)):
        for j in alphabet:
            tf.update({(i,j):list()})

    line = fp.readline()
    while line:
        l=line.split(' ')
        tf[(states.get(l[0]),l[1])].append (states.get(l[2][:len(l[2])-1]))
        t_function.append((states.get(l[0]),l[1],states.get(l[2][:len(l[2])-1])))
        line = fp.readline()
    
"""counstruct NFA object"""
n = NFA(states,len(states),alphabet, tf, t_function, start_state, accept_states)  

"""initial power set of NFA states as new DFA states"""
all_states=list()
stateList=range(n.states_number)
for i in range (2**(n.states_number)):
    cs=list()
    binaryn=decimalToBinary(i,n.states_number)
    for j in range(n.states_number):
        if binaryn[j] =='1':
            cs.append(stateList[j])
    all_states.append(cs)
"""make sigma table this table shows that in each DFA state with each alphabet machine gose to wich NFA states actually DFA state"""
sigma_table=list()
for state_set in all_states:
    row=list()
    for a in n.alphabet:
        distance_set=list()
        for s in state_set:
            distance_set+= (n.transition_function.get((s,a))) 
        row.append(distance_set)
    sigma_table.append(row)
'''
    remove duplicatons'''
for i in sigma_table:
    k=list()
    for j in i:
        j=list(dict.fromkeys(j))
        k.append(j)
    i=k
"""reading DFA transition functions from sigma table""" 
DFA_transition_function=list()
scount=0            
for i in sigma_table:
    alpha_counter=0
    for j in i:
        ds=['0']*n.states_number
        
        for k in j:
            
        
            ds[k]='1'

        if (n.alphabet[alpha_counter])!='l':
            DFA_transition_function.append(str(binaryToDecimal(decimalToBinary(scount,n.states_number)))+' '+str(n.alphabet[alpha_counter])+' '+str(binaryToDecimal(ds)))
        alpha_counter+=1
    scount+=1
"""finding DFA states that are a accept state"""
DFA_accept_states=list()
for i in all_states:
    for j in i:
        if j in n.new_accept_states:
            DFA_accept_states.append(i)
            break 
"""finding DFA alphabet actually it's same as NFA except it don't has lambda"""
DFA_alphabet=list()
for alpha in n.alphabet:
    if alpha!='l':
        DFA_alphabet.append(alpha)

dalphabet = DFA_alphabet
dtransition_function = DFA_transition_function
dstart_state = n.start_state
daccept_states = DFA_accept_states

with open('DFA',"w") as fp:


    for i in all_states:
        ds=['0']*n.states_number
        for k in i:
            ds[k]='1'
        fp.write(str(binaryToDecimal(ds))+' ')
    fp.write('\n')

    for i in dalphabet:
        fp.write(str(i)+' ')
    fp.write('\n')
    fp.write(str(dstart_state)+'\n')

    for i in daccept_states:
        ds=['0']*n.states_number
        for k in i:
            ds[k]='1'
        fp.write(str(binaryToDecimal(ds))+' ')
    fp.write('\n')

    for i in dtransition_function:
        fp.write(str(i)+'\n')

print('succesfully finished')
    