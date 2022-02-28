import random
import math


BOT_NAME = "23" #+ 19 


class RandomAgent:
    """Agent that picks a random available move.  You should be able to beat it."""
    def __init__(self, sd=None):
        if sd is None:
            self.st = None
        else:
            random.seed(sd)
            self.st = random.getstate()

    def get_move(self, state):
        if self.st is not None:
            random.setstate(self.st)
        return random.choice(state.successors())


class HumanAgent:
    """Prompts user to supply a valid move."""
    def get_move(self, state, depth=None):
        move__state = dict(state.successors())
        prompt = "Kindly enter your move {}: ".format(sorted(move__state.keys()))
        move = None
        while move not in move__state:
            try:
                move = int(input(prompt))
            except ValueError:
                continue
        return move, move__state[move]


class MinimaxAgent:
    """Artificially intelligent agent that uses minimax to optimally select the best move."""

    def get_move(self, state):
        """Select the best available move, based on minimax value."""
        nextp = state.next_player()
        best_util = -math.inf if nextp == 1 else math.inf
        best_move = None
        best_state = None
        for move, state in state.successors():
            util = self.minimax(state)
            if ((nextp == 1) and (util > best_util)) or ((nextp == -1) and (util < best_util)):
                best_util, best_move, best_state = util, move, state

        return best_move, best_state

    def minimax(self, state):
        """Determine the minimax utility value of the given state.

        Args:
            state: a connect383.GameState object representing the current board

        Returns: the exact minimax utility value of the state
        """
        successors = state.successors()
        player = state.next_player()
        if successors==[]:
           return state.utility()
        possibleValues = []
        for move, next in state.successors():
            if(move!=1):
                continue
            possibleValues.append(self.minimax(next))
        if (player==1):
            return max(possibleValues)
        return min(possibleValues)


class MinimaxHeuristicAgent(MinimaxAgent):
    """Artificially intelligent agent that uses depth-limited minimax to select the best move."""

    def __init__(self, depth_limit):
        self.depth_limit = depth_limit

    def minimax(self, state):
        """Determine the heuristically estimated minimax utility value of the given state.

        The depth data member (set in the constructor) determines the maximum depth of the game 
        tree that gets explored before estimating the state utilities using the evaluation() 
        function.  If depth is 0, no traversal is performed, and minimax returns the results of 
        a call to evaluation().  If depth is None, the entire game tree is traversed.

        Args:
            state: a connect383.GameState object representing the current board

        Returns: the minimax utility value of the state
        """
        return self.hminimax(state,0)

    def hminimax(self, state,depth):
        if(depth >= self.depth_limit):
            return self.evaluation(state)

        successors = state.successors()
        player = state.next_player()
        if successors==[]:
            return state.utility()
        possibleValues = []
        for move, next in state.successors():
            possibleValues.append(self.hminimax(next,depth+1))
        if (player==1):
            return max(possibleValues)
        return min(possibleValues)

    def evaluation(self, state):
        """Estimate the utility value of the game state based on features.

        N.B.: This method must run in constant time for all states!

        Args:
            state: a connect383.GameState object representing the current board

        Returns: a heuristic estimate of the utility value of the state
        """
        p1_score = 0
        p2_score = 0
        for run in state.get_rows() + state.get_cols() + state.get_diags():
            for elt, length in self.mstreaks(run):
                if (elt == 1) and (length >= 2):
                    p1_score += 1
                elif (elt == -1) and (length >= 2):
                    p2_score += 1
            for elt, length in self.streaks(run):
                if (elt == 1) and (length >= 3):
                    p1_score += length**2
                elif (elt == -1) and (length >= 3):
                    p2_score += length**2
            
        return p1_score- p2_score

    def streaks(self,lst):  
        """Get the lengths of all the streaks of the same element in a sequence."""
        rets = []  # list of (element, length) tuples
        prev = lst[0]
        curr_len = 1
        for curr in lst[1:]:
            if curr == prev:
                curr_len += 1
            else:
                rets.append((prev, curr_len))
                prev = curr
                curr_len = 1
        rets.append((prev, curr_len))
        return rets
    
    def mstreaks(self,lst):  
        """Get the lengths of all the streaks of the same element in a sequence."""
        rets = []  
        fchecker = False
        stack = []
        for curr in lst:
            if(curr == 0):# if its empty
                fchecker=True
                if len(stack)>=2:# if there is something in the stack
                    rets.append((stack[-1:][0],len(stack)))
                stack=[]
            elif(curr == 1 or curr == -1):
                if(len(stack)==0):#if there is nothing in the stack
                    stack.append(curr)
                elif(stack[-1:][0]==curr):#if the last element matches 
                    stack.append(curr)
                else:#if it didnt match
                    if(fchecker==True):#was it  a open list
                        rets.append((stack[-1:][0],len(stack)))
                    fchecker=False
                    stack=[]
                    stack.append(curr)
            else:
                if(fchecker==True and len(stack)!=0):#was it  a open list
                    rets.append((stack[-1:][0],len(stack)))
                    fchecker=False
                    stack=[] 
        
        if(fchecker==True and len(stack)!=0):#was it  a open list
            rets.append((stack[-1:][0],len(stack)))  

        return rets


class MinimaxPruneAgent(MinimaxAgent):
    """Smarter computer agent that uses minimax with alpha-beta pruning to select the best move."""

    def minimax(self, state):
        """Determine the minimax utility value the given state using alpha-beta pruning.

        The value should be equal to the one determined by MinimaxAgent.minimax(), but the 
        algorithm should do less work.  You can check this by inspecting the value of the class 
        variable GameState.state_count, which keeps track of how many GameState objects have been 
        created over time.  This agent does not use a depth limit like MinimaxHeuristicAgent.

        N.B.: When exploring the game tree and expanding nodes, you must consider the child nodes
        in the order that they are returned by GameState.successors().  That is, you cannot prune
        the state reached by moving to column 4 before you've explored the state reached by a move
        to to column 1.

        Args: 
            state: a connect383.GameState object representing the current board

        Returns: the minimax utility value of the state
        """
        
        # Fill this in!
        
        successors = state.successors()
        player = state.next_player()
        if successors==[]:
            return state.utility()
        thisbound = [-math.inf,math.inf]
        for move, next in successors:
            temp = self.myhelperminimax(next,thisbound)
            if (player==-1) and (temp[0]<thisbound[1]):
                thisbound[1]=temp[0]
            elif(player==1) and (temp[1]>thisbound[0]) :
                thisbound[0]=temp[1]
        if(player==1):
         
            return thisbound[0]
        else:
            
            return thisbound[1]
            

    def myhelperminimax(self,state,pbound):
        successors = state.successors()
        player = state.next_player()
        if successors==[]:
            return [state.utility(),state.utility()]
        thisbound = [-math.inf,math.inf] 
      
        for move, next in successors:
            temp = self.myhelperminimax(next,thisbound)
            
            if (player==-1) and (temp[0]<thisbound[1]):
                thisbound[1]=temp[0]
            elif(player==1) and (temp[1]>thisbound[0]) :
                thisbound[0]=temp[1]
            if(thisbound[1]<=pbound[0] and player ==-1):
                
                return [thisbound[1],thisbound[1]]
            if(thisbound[0]>=pbound[1] and player ==1):
            
                return [thisbound[0],thisbound[0]]

        if(player==1):
            return [thisbound[0],thisbound[0]]
        else:
             return [thisbound[1],thisbound[1]]
        
    


# N.B.: The following class is provided for convenience only; you do not need to implement it!

class OtherMinimaxHeuristicAgent(MinimaxAgent):
    """Alternative heursitic agent used for testing."""

    def __init__(self, depth_limit):
        self.depth_limit = depth_limit

    def minimax(self, state):
        """Determine the heuristically estimated minimax utility value of the given state."""
        #
        # Fill this in, if it pleases you.
        #
        return 26  # Change this line, unless you have something better to do.

