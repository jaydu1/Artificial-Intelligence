"""Implement your own custom search agent using any combination of techniques
you choose.  This agent will compete against other students (and past
champions) in a tournament.

         COMPLETING AND SUBMITTING A COMPETITION AGENT IS OPTIONAL
"""
import random


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")
    
    if game.is_winner(player):
        return float("inf")
    
    center = np.mean(game.get_blank_spaces())
    own_moves = len(game.get_legal_moves(player))
    if len(game.get_blank_spaces()) >= game.width*game.height/2:
        return np.sum((game.get_player_location(player) - center )**2)
    else:
        return float(own_moves) + np.sum((game.get_player_location(player) - center )**2)/game.width/game.height

class CustomPlayer:
    """Game-playing agent to use in the optional player vs player Isolation
    competition.

    You must at least implement the get_move() method and a search function
    to complete this class, but you may use any of the techniques discussed
    in lecture or elsewhere on the web -- opening books, MCTS, etc.

    **************************************************************************
          THIS CLASS IS OPTIONAL -- IT IS ONLY USED IN THE ISOLATION PvP
        COMPETITION.  IT IS NOT REQUIRED FOR THE ISOLATION PROJECT REVIEW.
    **************************************************************************

    Parameters
    ----------
    data : string
        The name of the search method to use in get_move().

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted.  Note that
        the PvP competition uses more accurate timers that are not cross-
        platform compatible, so a limit of 1ms (vs 10ms for the other classes)
        is generally sufficient.
    """

    def __init__(self, data=None, timeout=1.):
        self.score = custom_score
        self.time_left = None
        self.TIMER_THRESHOLD = timeout

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **********************************************************************
        NOTE: If time_left < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        # OPTIONAL: Finish this function!
        self.time_left = time_left
        
        # TODO: finish this function!
        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)
        
        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            depth = 0
            
            while(1):
                best_move = self.alphabeta(game, depth)
                if best_move==(-1, -1):
                    return best_move
                depth += 1
        
        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.
        
        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md
        
        **********************************************************************
        You MAY add additional methods to this class, or define helper
        functions to implement the required functionality.
        **********************************************************************
        
        Parameters
        ----------
        game : isolation.Board
        An instance of the Isolation game `Board` class representing the
        current game state
        
        depth : int
        Depth is an integer representing the maximum number of plies to
        search in the game tree before aborting
        
        alpha : float
        Alpha limits the lower bound of search on minimizing layers
        
        beta : float
        Beta limits the upper bound of search on maximizing layers
        
        Returns
        -------
        (int, int)
        The board coordinates of the best move found in the current search;
        (-1, -1) if there are no legal moves
        
        Notes
        -----
        (1) You MUST use the `self.score()` method for board evaluation
        to pass the project tests; you cannot call any other evaluation
        function directly.
        
        (2) If you use any helper functions (e.g., as shown in the AIMA
        pseudocode) then you must copy the timer check into the top of
        each helper function or else your agent will timeout during
        testing.
        """
        
        
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
                
                # MinValue Function
        def Alpha_Beta_min_value(self, game, depth, alpha, beta):
            # Timer Checker
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()
            # Terminal of the Game
            if not game.get_legal_moves():
                return game.utility(self)
            # Return the Score of the depth-level Nodes
            if (depth <= 0):
                return self.score(game,self)
            # Return the Max Value of other Nodes
            v = float("inf")
            for m in game.get_legal_moves():
                v = min(v, Alpha_Beta_max_value(self,game.forecast_move(m), depth-1, alpha, beta))
                if v<= alpha:
                    return v
                beta = min(beta, v)
            return v
                
        # MaxValue Function
        def Alpha_Beta_max_value(self, game, depth, alpha, beta):
            # Timer Checker
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()
            # Terminal of the Game
            if not game.get_legal_moves():
                return game.utility(self)
            # Return the Score of the Depth-level Nodes
            if (depth <= 0):
                return self.score(game,self)
            # Return the Max Value of Other Nodes
            v = float("-inf")
            for m in game.get_legal_moves():
                v = max(v, Alpha_Beta_min_value(self,game.forecast_move(m), depth-1, alpha, beta) )
                if v >= beta:
                    return v
                alpha = max(alpha, v)
            return v
                            
        # TODO: finish this function!
        m = game.get_legal_moves()
        if not m:        # If there is no legal moves
            return (-1, -1)
        else:
            best_m = (-1, -1)
            for i in m:
                v = Alpha_Beta_min_value(self, game.forecast_move(i), depth-1, alpha, beta)
                if v >= alpha:
                    alpha = v
                    best_m = i
            return best_m

