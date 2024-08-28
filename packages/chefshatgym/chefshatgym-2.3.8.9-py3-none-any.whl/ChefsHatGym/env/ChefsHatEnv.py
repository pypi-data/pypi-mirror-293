import gym
import random
import numpy
from ChefsHatGym.KEF import DataSetManager
from ChefsHatGym.KEF import ExperimentManager
import copy
from gym import spaces
import os

GAMETYPE = {"POINTS": "POINTS", "MATCHES": "MATCHES"}
ROLES = {0: "Dishwasher", 1: "Waiter", 2: "Souschef", 3: "Chef"}


class ChefsHatEnv(gym.Env):
    """ChefsHatEnv is the Chefs Hat game enviromnet class that allows to start and execute each step of the game.
    To instatiate the class, use gym.make('chefshat-v1').
    """

    gameFinished = False  #: Whether the game has been finished (True) or not (False).
    metadata = {"render.modes": ["human"]}

    def __init__(self):
        """Constructor method. Use gym.make instead of it."""

        # if integratedState:
        self.action_space = spaces.Discrete(int(200))
        self.observation_space = spaces.Box(
            low=numpy.float32(numpy.zeros(228)), high=numpy.float32(numpy.ones(228))
        )
        # pass

    def startExperiment(
        self,
        gameType=GAMETYPE["POINTS"],
        stopCriteria=3,
        maxRounds=-1,
        maxInvalidActions=5,
        playerNames=[],
        logDirectory="",
        verbose=0,
        saveLog=False,
        saveDataset=False,
    ):
        """This method stores parameters for a new exeperiment. An experiment is a set of games (see startNewGame method).

        :param rewardFunctions: A list of reward functions for each player, defaults to []
        :param gameType: The game type ("POINTS" or "MATCHES"), defaults to GAMETYPE["POINTS"]
        :type gameType: str, optional
        :param stopCriteria: Number of "MATCHES" or "POINTS" to stop the experiment, defaults to 3
        :type stopCriteria: int, optional
        :param maxRounds: Number maximum of rounds, before stoping the game. If -1, continue until all cards are finished, defaults to -1
        :type maxRounds: int, optional
        :param maxInvalidActions: How many invalid or continuous pass actions an Agent can do before a random action is assigned to it, defaults to 10
        :type maxInvalidActions: int, optional
        :param playerNames: A list of names for each player, defaults to []
        :type playerNames: list, mandatory
        :param logDirectory: The path for log directory, defaults to ""
        :type logDirectory: str, optional
        :param verbose: Verbose level (0 to 1), defaults to 0
        :type verbose: int, optional
        :param saveLog: Whether the log file will be generated (True) or not (False), defaults to False
        :type saveLog: bool, optional
        :param saveDataset: Whether the game dataset will be saved (True) or not (False), defaults to False
        :type saveDataset: bool, optional
        """

        # Start all game variables
        self.gameType = gameType
        self.stopCriteria = stopCriteria
        self.maxRounds = maxRounds if maxRounds > 0 else 999999
        self.playerNames = playerNames
        self.saveDataset = saveDataset

        self.episodeNumber = 0

        self.logDirectory = logDirectory
        self.verbose = verbose
        self.saveLog = saveLog
        self.maxInvalidActions = maxInvalidActions

        self.playersInvalidActions = [0, 0, 0, 0]
        self.playersPassAction = [0, 0, 0, 0]

    def reset(self, seed=None, options=None):
        """This method increments episodeNumber, start a new game and return the first observation

        :return: The first observation array after the game has started. The observation is an int data-type ndarray.
        :rtype: ndarray
        """

        self.episodeNumber += 1
        self.startNewGame()
        return (numpy.array(self.getObservation()).astype(numpy.float32), {})

    def startNewGame(self):
        """Starts a new game using the parameters defined by the method startExperiment.
        You have to define the game type (per points or per game), and the stoping criteria (maximum points, maximum games).
        For logging purpose, set the saveLog, verbose and logDirectory in startExperiment method.
        """
        if not self.logDirectory == "":
            _path = os.path.split(self.logDirectory)
            self.experimentManager = ExperimentManager.ExperimentManager(
                _path[0],
                _path[1],
                verbose=self.verbose,
                saveLog=self.saveLog,
                save_dataset=self.saveDataset,
            )
            self.logger = self.experimentManager.logManager
            self.logger.newLogSession("Starting new Episode:" + str(self.episodeNumber))
            self.logger.write("Players :" + str(self.playerNames))
            self.logger.write(
                "Stop Criteria :" + str(self.stopCriteria) + " " + str(self.gameType)
            )
            self.logger.write("Max Rounds :" + str(self.maxRounds))
        else:
            self.logger = None
            self.experimentManager = None
            self.saveDataset = False

        self.score = [0, 0, 0, 0]  # the score
        self.performanceScore = [0, 0, 0, 0]  # the performance score
        self.board = []  # the current board
        self.maxCardNumber = 11  # The highest value of a card in the deck
        self.numberPlayers = 4  # number of players playing the game
        self.numberOfCardsPerPlayer = (
            0  # number of cards each player has at hand in the begining of the game
        )
        self.highLevelActions = self.getHighLevelActions()
        self.matches = 0
        self.gameFinished = False
        self.finishingOrder = []  # Which payers already finished this match

        # Variables per Match
        self.cards = []  # the deck
        self.playersHand = []  # the current cards each player has at hand
        self.currentPlayer = 0  # The current player playing the game
        self.playerStartedGame = 0  # who started the game
        self.currentRoles = []  # Current roles of each player
        self.currentSpecialAction = []
        self.currentPlayerDeclaredSpecialAction = []
        self.rounds = 0
        self.lastToDiscard = 0

        self.experimentManager.dataSetManager.startNewGame(
            agent_names=self.playerNames,
        )

        # self.startNewmatch()  # Initiate all the match parameters

        self.start_match_handle_cards()
        self.start_match_define_order()

    def start_match_handle_cards(self):
        """Handle the cards to the players."""

        # Stop by round set to false
        self.stoppedByRound = False

        # Create a deck
        flat = lambda l: [item for sublist in l for item in sublist]
        self.cards = flat(
            [[v for _ in range(v)] for v in range(1, self.maxCardNumber + 1)]
        ) + [self.maxCardNumber + 1 for _ in range(2)]

        self.lastActionPlayers = ["", "", "", ""]

        # shuffle the decks
        random.shuffle(self.cards)

        # create players hand
        self.playersHand = []
        for i in range(self.numberPlayers):
            self.playersHand.append([])

        self.numberOfCardsPerPlayer = int(len(self.cards) / len(self.playersHand))

        # initialize the board
        self.restartBoard()

        # Update the Match number

        self.matches += 1

        self.experimentManager.dataSetManager.startNewMatch(
            match_number=self.matches,
            game_score=self.score,
            current_roles=[ROLES[a] for a in self.currentRoles],
        )

        # deal the cards
        self.dealCards()

        if not self.experimentManager == None:
            self.logger.newLogSession("Match Number %f Starts!" % self.matches)
            self.logger.write("Deck: " + str(self.cards))
            for i in range(len(self.playerNames)):
                self.logger.write("Player " + str(i) + ":" + str(self.playersHand[i]))

    def start_match_define_order(self):
        """Define the starting order for each match"""
        # Establishes who starts the game randomly
        playerTurn = numpy.array(range(self.numberPlayers))
        random.shuffle(playerTurn)

        index = numpy.array(range(self.numberPlayers))
        random.shuffle(index)

        self.currentPlayer = playerTurn[index[0]]

        # verify if this player has a 12 in its hand, otherwise iterate to the next player

        while not (self.maxCardNumber + 1 in self.playersHand[self.currentPlayer]):
            self.currentPlayer = self.currentPlayer + 1
            if self.currentPlayer >= self.numberPlayers:
                self.currentPlayer = 0

        # save the player who started the game
        self.playerStartedGame = self.currentPlayer

        self.finishingOrder = []  # Reset the players that finished this match

        # Current round of the game set to 0
        self.rounds = 1

        if not self.experimentManager == None:
            self.logger.newLogSession("Round:" + str(self.rounds))

    def doSpecialAction(self, player, action):
        """Allows an agent to perform a special action

        Args:
            player (_type_): _description_
            action (_type_): _description_
        """
        if not self.experimentManager == None:
            self.logger.write(
                "- Player :"
                + str(player)
                + " declared "
                + str(self.currentSpecialAction)
                + "!"
            )

        if (
            action == "It is food fight!"
        ):  # If it is food fight, update the roles of the game.
            newcurrentRoles = []
            newcurrentRoles.append(self.currentRoles[3])  # Chef
            newcurrentRoles.append(self.currentRoles[2])  # sous-Chef
            newcurrentRoles.append(self.currentRoles[1])  # waiter
            newcurrentRoles.append(self.currentRoles[0])  # dishwasher
            self.currentRoles = []
            self.currentRoles = newcurrentRoles

            self.logNewRoles()

        self.experimentManager.dataSetManager.do_special_action(
            match_number=self.matches,
            source=self.playerNames[player],
            current_roles=[ROLES[a] for a in self.currentRoles],
            action_description=action,
        )

    def get_chef_souschef_roles_cards(self):
        """returns the cards at hand of the chef and souschef.

        Returns:
            _type_: _description_
        """

        # Chef, sous-Chef, waiter and dishwasher
        score = self.currentRoles

        dishwasherCards = sorted(self.playersHand[score[3]])[
            0:2
        ]  # get the minimum dishwasher cards
        waiterCard = sorted(self.playersHand[score[2]])[0]  # get the minimum waiterCard

        return (
            score[3],
            dishwasherCards,
            score[2],
            waiterCard,
            score[1],
            self.playersHand[score[1]],
            score[0],
            self.playersHand[score[0]],
        )

    def exchange_cards(self, souschefCard, chefCards, specialAction, playerDeclared):
        """Allows a chef and souschef agent to select the cards to be exchanged.

        Args:
            souschefCard (_type_): _description_
            chefCards (_type_): _description_
            specialAction (_type_): _description_
            playerDeclared (_type_): _description_
        """
        score = self.currentRoles
        souschefCard = souschefCard[0]

        dishwasherCards = sorted(self.playersHand[score[3]])[
            0:2
        ]  # get the minimum dishwasher cards
        waiterCard = sorted(self.playersHand[score[2]])[0]  # get the minimum waiterCard

        # update the dishwasher cards
        for i in range(len(dishwasherCards)):
            cardIndex = self.playersHand[score[3]].index((dishwasherCards[i]))
            self.playersHand[score[3]][cardIndex] = chefCards[i]

        # update the chef cards
        for i in range(len(chefCards)):
            cardIndex = self.playersHand[score[0]].index((chefCards[i]))
            self.playersHand[score[0]][cardIndex] = dishwasherCards[i]

        # update the waiter cards
        cardIndex = self.playersHand[score[2]].index((waiterCard))
        self.playersHand[score[2]][cardIndex] = souschefCard

        # update the souschef cards
        cardIndex = self.playersHand[score[1]].index((souschefCard))
        self.playersHand[score[1]][cardIndex] = waiterCard

        # Logging new cards exchanged!
        self.logger.newLogSession("Changing cards!")
        self.logger.write("--- Dishwasher gave:" + str(dishwasherCards))
        self.logger.write("--- Waiter gave:" + str(waiterCard))
        self.logger.write("--- Souschef gave:" + str(souschefCard))
        self.logger.write("--- Chef gave:" + str(chefCards))

        self.experimentManager.dataSetManager.do_card_exchange(
            match_number=self.matches,
            action_description=[
                specialAction,
                playerDeclared,
                dishwasherCards,
                waiterCard,
                souschefCard,
                chefCards,
            ],
            player_hands=self.playersHand,
        )

        self.start_match_define_order()

    def logNewRoles(self):
        """Add the new roles to log"""
        self.logger.newLogSession("Changind roles!")

        self.logger.write(
            "- Dishwasher Player:" + self.playerNames[self.currentRoles[3]]
        )
        self.logger.write("- Waiter: Player " + self.playerNames[self.currentRoles[2]])
        self.logger.write("- Souschef Player:" + self.playerNames[self.currentRoles[1]])
        self.logger.write("- Chef Player:" + self.playerNames[self.currentRoles[0]])

    def getObservation(self):
        """Get a new observation. The observation is composed of the current board, the playersHand and the possible actions.

        :return: The observation is an int data-type ndarray.
                    The observation array has information about the board game, the current player's hand, and current player possible actions.
                    This array must have the shape of (228, ) as follows:
                    The first 11 elements represent the board game card placeholder (the pizza area).
                    The game cards are represented by an integer, where 0 (zero) means no card.
                    The following 17 elements (from index 11 to 27) represent the current player hand cards in the sequence.
                    By the end, the last 200 elements (from index 27 to 227) represent all possible actions in the game.
                    The allowed actions for the current player are filled with one, while invalid actions are filled with 0.
        :rtype: ndarray
        """
        board = numpy.array(self.board) / (self.maxCardNumber + 2)
        playersHand = numpy.array(self.playersHand[self.currentPlayer]) / (
            self.maxCardNumber + 2
        )
        possibleActions = self.getPossibleActions(self.currentPlayer)

        return numpy.concatenate((board, playersHand, possibleActions)).astype(
            numpy.float32
        )

    def isGameOver(self):
        """isGameOver
        :return: Boolean flag if the game is over.
        :rtype: bool
        """
        gameFinished = False

        # input("here")
        # Verify if the game is over
        if self.gameType == GAMETYPE["POINTS"]:
            if self.score[numpy.argmax(self.score)] >= self.stopCriteria:
                gameFinished = True
        elif self.gameType == GAMETYPE["MATCHES"]:
            if self.matches >= self.stopCriteria:
                gameFinished = True

        if not self.experimentManager == None and gameFinished:
            # print(f"Adding to the log!")
            self.logger.newLogSession(
                "Game Over! Final Score:"
                + str(self.score)
                + " - Final Performance Score:"
                + str(self.performanceScore)
            )

        return gameFinished

    def nextPlayer(self):
        """nextPlayer
        advance to the next player
        """
        self.currentPlayer = self.currentPlayer + 1
        if self.currentPlayer == self.numberPlayers:
            self.currentPlayer = 0

        for i in range(len(self.lastActionPlayers)):
            if (
                (not self.lastActionPlayers[self.currentPlayer] == "")
                and self.lastActionPlayers[self.currentPlayer][0]
                == DataSetManager.actionPass
            ) or (
                (not self.lastActionPlayers[self.currentPlayer] == "")
                and self.lastActionPlayers[self.currentPlayer][0]
                == DataSetManager.actionFinish
            ):
                self.currentPlayer = self.currentPlayer + 1
                if self.currentPlayer == self.numberPlayers:
                    self.currentPlayer = 0

    def calculateScore(self, playerPosition):
        """calculateScore
        :param playerPosition: The finishing position of the player
        :type playerPosition: int, mandatory
        :return: Integer the score of the given player.
        :rtype: int
        """
        return 3 - playerPosition

    def getRandomAction(self, possibleActions):
        """getRandomAction
            Return a random allowed action.

        :param possibleActions: The list of possible actions
        :type possibleActions: list, mandatory
        :return: List the random action.
        :rtype: list
        """
        itemindex = numpy.array(numpy.where(numpy.array(possibleActions) == 1))[
            0
        ].tolist()

        random.shuffle(itemindex)
        aIndex = itemindex[0]
        a = numpy.zeros(200)
        a[aIndex] = 1

        return a.tolist()

    def decode_possible_actions(self, possibleActions):

        nonzeroElements = numpy.nonzero(possibleActions)

        currentlyAllowedActions = list(
            numpy.copy(numpy.array(self.highLevelActions)[nonzeroElements,])[0]
        )

        return currentlyAllowedActions

    def step(self, action):
        """Execute an action in the game.

        :param action: The action array with 200 elements, where the choosen action is the index of the highest value
        :type action: ndarray
        :return: a tuple cointaining:
                observation - ndarray
                return of reward function - float
                True if the match is over, False if not - bool
                info - dict: {
                'actionIsRandom':(bool),
                'validAction': (bool),
                'matches': (bool),
                'rounds': (int),
                'score': (int),
                'performanceScore': (int),
                'thisPlayer': (int),
                'thisPlayerFinished': (bool),
                'isPizzaReady': (bool),
                'boardBefore': (ndarray),
                'boardAfter': (ndarray),
                'board': (ndarray),
                'possibleActions': (list),
                'action': (ndarray),
                'thisPlayerPosition': (int),
                'lastPlayerAction': (int),
                'lastActionPlayers': (ndarray),
                'lastActionTypes': (ndarray),
                'RemainingCardsPerPlayer': (ndarray),
                'players': (list),
                'currentRoles': (list),
                'currentPlayer': (int),
                }

        :rtype: tuple
        """
        validAction = False
        isMatchOver = False
        isPizzaReady = False
        actionIsRandom = False
        thisPlayerPosition = -1

        possibleActions = self.getPossibleActions(self.currentPlayer)
        # Calculate the currentlyAllowedActions in a high-level
        nonzeroElements = numpy.nonzero(possibleActions)

        currentlyAllowedActions = list(
            numpy.copy(numpy.array(self.highLevelActions)[nonzeroElements,])[0]
        )

        thisPlayer = copy.copy(self.currentPlayer)
        boardBefore = copy.copy(self.board)

        observationBefore = copy.copy(self.getObservation())

        if (
            self.playersInvalidActions[thisPlayer] >= self.maxInvalidActions
            or self.playersPassAction[thisPlayer] >= self.maxInvalidActions
        ):
            action = self.getRandomAction(possibleActions)
            actionIsRandom = True

        if self.isActionAllowed(
            thisPlayer, action, possibleActions
        ):  # if the player can make the action, do it.
            validAction = True
            self.playersInvalidActions[thisPlayer] = 0

            cardsDiscarded = []
            if numpy.argmax(action) == len(possibleActions) - 1:  # Pass action
                actionComplete = (DataSetManager.actionPass, [0])
                self.playersPassAction[thisPlayer] += 1
            else:  # Discard action
                self.playersPassAction[thisPlayer] = 0
                cardsDiscarded = self.discardCards(self.currentPlayer, action)

                actionComplete = (DataSetManager.actionDiscard, cardsDiscarded)
                self.lastToDiscard = self.currentPlayer

            # thisPlayerStopByRound = False
            # if self.rounds > self.maxRounds:
            #     thisPlayerStopByRound = True

            # Verify if the player has finished this match
            if self.hasPlayerFinished(self.currentPlayer):
                # if (
                #     not self.currentPlayer in self.finishingOrder
                # ) or thisPlayerStopByRound:
                #     # If the game stops by rounds, calculate the position based on the amount of cards at hand
                #     if thisPlayerStopByRound:
                #         if not self.stoppedByRound:
                #             positions = {}
                #             amountOfCardsByPlayer = [
                #                 numpy.count_nonzero(a) for a in self.playersHand
                #             ]

                #             for a, count in zip(
                #                 self.playerNames, amountOfCardsByPlayer
                #             ):
                #                 positions[a] = count

                #             sortedPositions = dict(
                #                 sorted(positions.items(), key=lambda x: x[1])
                #             )

                #             playerIndex = [
                #                 self.playerNames.index(a)
                #                 for a in sortedPositions.keys()
                #             ]
                #             self.finishingOrder = playerIndex
                #             self.stoppedByRound = True

                #         self.playersHand[self.currentPlayer] = numpy.zeros(
                #             len(self.playersHand[self.currentPlayer])
                #         )
                #     else:

                self.finishingOrder.append(self.currentPlayer)

                actionComplete = (DataSetManager.actionFinish, cardsDiscarded)

                # Calculate and update the player score
                playerFinishingPosition = self.finishingOrder.index(self.currentPlayer)
                points = self.calculateScore(playerFinishingPosition)

                self.score[self.currentPlayer] += points

                pScore = (points * 10) / self.rounds
                # self.performanceScore[self.currentPlayer] += pScore
                self.performanceScore[self.currentPlayer] = (
                    self.performanceScore[self.currentPlayer] * (self.matches - 1)
                    + pScore
                ) / self.matches
                thisPlayerPosition = playerFinishingPosition

            # Update the player last action
            self.lastActionPlayers[self.currentPlayer] = actionComplete

            if not self.experimentManager == None:
                self.logger.write(
                    " -- Player "
                    + str(thisPlayer)
                    + " - "
                    + str(self.playerNames[self.currentPlayer])
                )
                self.logger.write(
                    " --- Player Hand: " + str(self.playersHand[self.currentPlayer])
                )
                self.logger.write(" --- Board Before: " + str(boardBefore))
                self.logger.write(
                    " --- Action: " + str(self.highLevelActions[numpy.argmax(action)])
                )
                self.logger.write(" --- Board After: " + str(self.board))

            boardAfter = self.getObservation()[0:11].tolist()

            self.experimentManager.dataSetManager.doDiscard(
                match_number=self.matches,
                round_number=self.rounds,
                source=self.playerNames[thisPlayer],
                action_description=self.highLevelActions[numpy.argmax(action)],
                player_hands=self.playersHand,
                board_before=[int(b * 13) for b in boardBefore],
                board_after=[int(b * 13) for b in boardAfter],
                possible_actions=currentlyAllowedActions,
                player_finished=(
                    bool(thisPlayer in self.finishingOrder)
                    if len(self.finishingOrder) > 0
                    else False
                ),
            )

            # Identify if the pizza is ready
            isPizzaReady = False
            if self.makePizza():
                isPizzaReady = True

                self.experimentManager.dataSetManager.declare_pizza(
                    match_number=self.matches,
                    round_number=self.rounds - 1,
                    source=self.playerNames[self.lastToDiscard],
                )

                self.currentPlayer = self.lastToDiscard
                if self.currentPlayer in self.finishingOrder:
                    self.nextPlayer()
            else:
                self.nextPlayer()

            # If finish the game by rounds, calculate the finishing order, and remove the cards from the hands of all players.
            points_position = [0, 0, 0, 0]

            if self.rounds > self.maxRounds:

                # Calculate the players position based on the amount of cards they have in their hand
                positions = {}
                amountOfCardsByPlayer = [
                    numpy.count_nonzero(a) for a in self.playersHand
                ]

                print("---------------")
                print(f"AMount of cards by player: {amountOfCardsByPlayer}")

                for a, count in zip(self.playerNames, amountOfCardsByPlayer):
                    positions[a] = count

                sortedPositions = dict(sorted(positions.items(), key=lambda x: x[1]))

                print(f"Player position: {positions}")
                print(f"Player sorted position: {sortedPositions}")

                playerIndex = [
                    self.playerNames.index(a) for a in sortedPositions.keys()
                ]

                self.finishingOrder = playerIndex

                print(f"Finishing Order: {self.finishingOrder}")
                print("---------------")

                # Put all player hands to 0
                for i in range(len(self.playersHand)):
                    self.playersHand[i] = numpy.zeros(self.numberOfCardsPerPlayer)

                # Calculate the players score
                points_position = [
                    self.calculateScore(position) for position in self.finishingOrder
                ]

                print(f"Points Position: {points_position}")

                for count, point in enumerate(points_position):
                    self.score[count] += point

                    pScore = (point * 10) / self.rounds

                    self.performanceScore[count] = (
                        self.performanceScore[count] * (self.matches - 1) + pScore
                    ) / self.matches

            if self.isMatchover():
                isMatchOver = True

                # if the score exists, update roles
                if numpy.max(self.score) > 0:
                    # Chef, sous-Chef, waiter and dishwasher
                    self.currentRoles = [self.finishingOrder[i] for i in range(4)]

                self.experimentManager.dataSetManager.saveFile()

                if isPizzaReady:
                    log_round = self.rounds - 1
                else:
                    log_round = self.rounds

                points_position = [
                    self.calculateScore(position) for position in self.finishingOrder
                ]

                self.experimentManager.dataSetManager.end_match(
                    match_number=self.matches,
                    round_number=log_round,
                    match_score=points_position,
                    game_score=self.score,
                    current_roles=[ROLES[a] for a in self.currentRoles],
                )

                if self.isGameOver():
                    self.gameFinished = True
                    self.experimentManager.dataSetManager.end_experiment(
                        match_number=self.matches,
                        round_number=log_round,
                        current_roles=[ROLES[a] for a in self.currentRoles],
                        game_score=self.score,
                        game_performance=self.performanceScore,
                    )
                else:
                    self.logNewRoles()
                    self.start_match_handle_cards()

            # if self.gameFinished:
            #     self.experimentManager.dataSetManager.saveFile()
        else:
            self.playersInvalidActions[thisPlayer] += 1
            isMatchOver = False
            boardAfter = self.getObservation()[0:11].tolist()

        # Sanitizing the action
        arg_max_action = numpy.argmax(action)
        action[arg_max_action] = 1

        # this_row["Match"] = match_number
        # this_row["Round"] = round_number
        # this_row["Agent_Names"] = [agent_names]
        # this_row["Source"] = source
        # this_row["Action_Type"] = action_type
        # this_row["Action_Description"] = action_description
        # this_row["Player_Finished"] = player_finished
        # this_row["Player_Hands"] = [player_hands]
        # this_row["Board_Before"] = [board_before]
        # this_row["Board_After"] = [board_after]
        # this_row["Possible_Actions"] = [possible_actions]
        # this_row["Current_Roles"] = [current_roles]
        # this_row["Match_Score"] = [match_score]
        # this_row["Game_Score"] = [game_score]
        # this_row["Game_Performance_Score"] = [game_performance_score]

        info = {}
        # Game Settings Info
        info["Matches"] = int(self.matches)
        info["Rounds"] = int(self.rounds)
        info["Player_Names"] = self.playerNames

        # This Player Info
        info["Author_Index"] = int(thisPlayer)
        info["Author_Possible_Actions"] = currentlyAllowedActions

        # Action Info
        info["Action_Valid"] = bool(validAction)
        info["Action_Random"] = bool(actionIsRandom)
        info["Action_Index"] = int(numpy.argmax(action))
        info["Action_Decoded"] = self.highLevelActions[numpy.argmax(action)]

        # Gameplay Status
        info["Is_Pizza"] = bool(isPizzaReady)
        info["Pizza_Author"] = int(self.lastToDiscard) if isPizzaReady else -1
        info["Finished_Players"] = [
            bool(p in self.finishingOrder) for p in range(self.numberPlayers)
        ]
        info["Cards_Per_Player"] = [
            len(list(filter(lambda a: a > 0, self.playersHand[i])))
            for i in range(self.numberPlayers)
        ]
        info["Next_Player"] = int(self.currentPlayer)

        # Board Info
        info["Board_Before"] = [int(a * 13) for a in observationBefore[0:11].tolist()]
        info["Board_After"] = [int(a * 13) for a in boardAfter]

        # Match Info
        info["Current_Roles"] = self.currentRoles
        info["Match_Score"] = points_position
        info["Game_Score"] = self.score
        info["Game_Performance_Score"] = self.performanceScore

        # info["actionIsRandom"] = actionIsRandom
        # info["validAction"] = validAction
        # info["matches"] = int(self.matches)
        # info["rounds"] = int(self.rounds)
        # info["score"] = self.score
        # info["performanceScore"] = self.performanceScore
        # info["thisPlayer"] = int(thisPlayer)
        # info["thisPlayerFinished"] = thisPlayer in self.finishingOrder
        # info["PlayersFinished"] = [
        #     p in self.finishingOrder for p in range(self.numberPlayers)
        # ]
        # info["isPizzaReady"] = isPizzaReady
        # info["boardBefore"] = observationBefore[0:11].tolist()
        # info["boardAfter"] = boardAfter
        # info["board"] = numpy.array(self.getObservation() * 13, dtype=int).tolist()[:11]
        # info["possibleActions"] = possibleActions
        # info["possibleActionsDecoded"] = currentlyAllowedActions
        # info["action"] = action
        # info["thisPlayerPosition"] = int(thisPlayerPosition)
        # info["lastActionPlayers"] = self.lastActionPlayers
        # info["lastActionTypes"] = [
        #     "" if a == "" else a[0] for a in self.lastActionPlayers
        # ]
        # info["RemainingCardsPerPlayer"] = [
        #     len(list(filter(lambda a: a > 0, self.playersHand[i])))
        #     for i in range(self.numberPlayers)
        # ]
        # info["players"] = self.playerNames
        # info["currentRoles"] = self.currentRoles
        # info["currentPlayer"] = int(self.currentPlayer)

        reward = 0
        return (
            numpy.array(self.getObservation()).astype(numpy.float32),
            reward,
            isMatchOver,
            False,
            info,
        )

    def render(self, mode="human", close=False):
        pass

    def close(self):
        pass

    def makePizza(self):
        """Make a pizza. Update the game to the next round and collect all cards from the board

        :return: pizzaReady - bool
        :rtype: bool
        """
        playersInGame = []
        for i in range(len(self.lastActionPlayers)):
            if not (i in self.finishingOrder):
                playersInGame.append(i)

        # print ("self.lastActionPlayers:" + str(self.lastActionPlayers))
        # print ("FInishing Order:" + str(self.finishingOrder))
        numberFinished = 0
        numberOfActions = 0

        for i in playersInGame:
            if (not self.lastActionPlayers[i] == "") and (
                self.lastActionPlayers[i][0] == DataSetManager.actionPass
            ):
                numberFinished += 1

            if not self.lastActionPlayers[i] == "":
                numberOfActions += 1

        # print ("Players in game:" + str(playersInGame))
        # print ("Number of Actions:" + str(numberOfActions))
        # print("Number Finished:" + str(numberFinished))

        pizzaReady = False
        if (numberFinished >= len(playersInGame) - 1) and (
            numberOfActions == len(playersInGame)
        ):
            self.restartBoard()
            pizzaReady = True

            if not self.experimentManager == None:
                self.logger.newLogSession("Pizza ready!!!")

            self.nextRound()

        return pizzaReady

    def nextRound(self):
        """move the game to the next round"""
        self.rounds = self.rounds + 1

        newLastActionPlayers = ["", "", "", ""]
        for actionIndex, action in enumerate(self.lastActionPlayers):
            if (not action == "") and action[0] == DataSetManager.actionFinish:
                newLastActionPlayers[actionIndex] = action

        # print ("Previous actions:" + str(self.lastActionPlayers))
        # print ("Next actions:" + str(newLastActionPlayers))
        self.lastActionPlayers = newLastActionPlayers

        if not self.experimentManager == None:
            self.logger.newLogSession("Round:" + str(self.rounds))

    def isMatchover(self):
        """Verify if this match is over
        look at the players hand, if 3 of them have 0 cards, match over.
        if match over,  add plyers to the finishing order


        :return: isMatchOver - bool
            :rtype: bool
        """
        isMatchOver = True

        players_finished = 0
        for i in range(len(self.playersHand)):
            if numpy.array(self.playersHand[i]).sum() == 0:
                players_finished += 1

        if players_finished < 3:
            isMatchOver = False
        else:
            # Add the last player on the finishing order
            for i in range(len(self.playersHand)):
                if not i in self.finishingOrder:
                    self.finishingOrder.append(i)
                    break

        if isMatchOver:
            if not self.experimentManager == None:
                self.logger.newLogSession(
                    "Match "
                    + str(self.matches)
                    + " over! Current Score:"
                    + str(self.score)
                )

        return isMatchOver

    def getHighLevelActions(self):
        """Generate all the possible actions in a human-friendly way

        :return: highLevelActions - List
            :rtype: list
        """
        highLevelActions = []

        for cardNumber in range(self.maxCardNumber):
            for cardQuantity in range(cardNumber + 1):
                highLevelActions.append(
                    "C" + str(cardNumber + 1) + ";Q" + str(cardQuantity + 1) + ";J0"
                )
                highLevelActions.append(
                    "C" + str(cardNumber + 1) + ";Q" + str(cardQuantity + 1) + ";J1"
                )
                highLevelActions.append(
                    "C" + str(cardNumber + 1) + ";Q" + str(cardQuantity + 1) + ";J2"
                )

        highLevelActions.append("C0;Q0;J1")
        highLevelActions.append("pass")

        return highLevelActions

    # the number of possible actions is: self.maxCardNumber * self.maxCardNumber * 3 + 2
    # where the *3 refers to the options: discard a card, card+1 joker, card + 2 jokers
    # the 2 refers to: discard only one joker, and pass action
    def getPossibleActions(self, player):
        """Given a player, return the actions this player is allowed to make

            :param player: the player index
            :type player: int

        :return: getPossibleActions - (ndarray)
            :rtype: (ndarray)
        """
        firstAction = self.playerStartedGame == self.currentPlayer and self.rounds == 1

        # print(
        #     f"First action = {firstAction} - Player started game ({self.playerStartedGame}) == currentPlayer ({self.currentPlayer}) and self.rounds({self.rounds}) == 1"
        # )

        # print ("Player:", player)
        possibleActions = []

        unique, counts = numpy.unique(self.board, return_counts=True)
        currentBoard = dict(zip(unique, counts))

        unique, counts = numpy.unique(self.playersHand[player], return_counts=True)
        currentPlayerHand = dict(zip(unique, counts))

        highestCardOnBoard = 0
        for boardItem in currentBoard:
            if not boardItem == self.maxCardNumber + 1:
                highestCardOnBoard = boardItem

        jokerQuantityBoard = 0

        if self.maxCardNumber + 1 in self.board:
            jokerQuantityBoard = currentBoard[self.maxCardNumber + 1]

        if self.maxCardNumber + 1 in currentPlayerHand.keys():
            jokerQuantity = currentPlayerHand[self.maxCardNumber + 1]
        else:
            jokerQuantity = 0

        cardDescription = ""
        for cardNumber in range(self.maxCardNumber):
            for cardQuantity in range(cardNumber + 1):
                isThisCombinationAllowed = 0
                isthisCombinationOneJokerAllowed = 0
                isthisCombinationtwoJokersAllowed = 0

                # print("Card:" + str(cardNumber + 1) + " Quantity:" + str(cardQuantity + 1))

                """If this card number is in my hands and the amount of cards in my hands is this amount"""
                if (cardNumber + 1) in self.playersHand[player] and currentPlayerHand[
                    cardNumber + 1
                ] >= cardQuantity + 1:
                    # print("-- this combination exists in my hand!")

                    """Check combination without the joker"""
                    """Check if this combination of card and quantity can be discarded given teh cards on the board"""
                    """Check if this cardnumber is smaller than the cards on the board"""
                    """ and check if the cardquantity is equal of higher than the number of cards on the board (represented by the highest card on the board ) + number of jokers on the board"""
                    if (cardNumber + 1 < highestCardOnBoard) and (
                        cardQuantity + 1
                        >= currentBoard[highestCardOnBoard] + jokerQuantityBoard
                    ):
                        """Check if this is the first move"""
                        """If it is the first move, onle 11s are allowed"""
                        if firstAction:
                            if cardNumber + 1 == self.maxCardNumber:
                                isThisCombinationAllowed = 1
                                # print("--- this combination can be put down on the board because it is first action!")
                        else:
                            """If it is not first move, anything on this combination is allowed!"""
                            # print("--- this combination can be put down on the board because and it is not first action!")
                            isThisCombinationAllowed = 1

                    """Check combination with the joker"""

                    if jokerQuantity > 0:
                        """Check for 1 joker at hand"""
                        """Check if this combination of card and quantity + joker can be discarded given the cards on the board"""
                        """Check if this cardnumber is smaller than the cards on the board"""
                        """ and check if the cardquantity + 1 joker is equal or higher than the number of cards on the board (represented by the highest card on the board ) + number of jokers on the board"""
                        if (cardNumber + 1 < highestCardOnBoard) and (
                            (cardQuantity + 1 + 1)
                            >= currentBoard[highestCardOnBoard] + jokerQuantityBoard
                        ):
                            """Check if this is the first move"""
                            """If it is the first move, onle 11s are allowed"""
                            if firstAction:
                                if cardNumber + 1 == self.maxCardNumber:
                                    # print(
                                    #     "--- this combination can be put down on the board because and it is first action and joker!")
                                    isthisCombinationOneJokerAllowed = 1
                            else:
                                """If it is not first move, anything on this combination is allowed!"""
                                # print(
                                #     "--- this combination can be put down on the board because and it is not first action and joker!")
                                isthisCombinationOneJokerAllowed = 1

                        if jokerQuantity > 1:
                            """Check for 2 jokers at hand"""
                            """Check if this combination of card and quantity + joker can be discarded given the cards on the board"""
                            """Check if this cardnumber is smaller than the cards on the board"""
                            """ and check if the cardquantity + 2 joker is equal or higher than the number of cards on the board (represented by the highest card on the board ) + number of jokers on the board"""
                            if (cardNumber + 1 < highestCardOnBoard) and (
                                (cardQuantity + 1 + 2)
                                >= currentBoard[highestCardOnBoard] + jokerQuantityBoard
                            ):
                                """Check if this is the first move"""
                                """If it is the first move, onle 11s are allowed"""
                                if firstAction:
                                    if cardNumber + 1 == self.maxCardNumber:
                                        # print(
                                        #     "--- this combination can be put down on the board because and it is first action and 2 jokers!")
                                        isthisCombinationtwoJokersAllowed = 1

                                else:
                                    """If it is not first move, anything on this combination is allowed!"""
                                    # print(
                                    #     "--- this combination can be put down on the board because and it is not first action and 2 jokers!")
                                    isthisCombinationtwoJokersAllowed = 2

                possibleActions.append(isThisCombinationAllowed)
                possibleActions.append(isthisCombinationOneJokerAllowed)
                possibleActions.append(isthisCombinationtwoJokersAllowed)

        canDiscardOnlyJoker = 0

        if (
            self.maxCardNumber + 1 in self.playersHand[player]
        ):  # there is a joker in the hand
            if not firstAction:
                if highestCardOnBoard == self.maxCardNumber + 2:
                    canDiscardOnlyJoker = 1

        possibleActions.append(canDiscardOnlyJoker)
        possibleActions.append(1)  # the pass action, which is always a valid action
        return possibleActions

    def isActionAllowed(self, player, action, possibleActions):
        """Given a player, the action and possible actions, verify if this action is allowed

        :param player: the player index
        :type player: int

        :param action: the action
        :type player: list

        :param possibleActions: the possible actions for this player
        :type player: (ndarray)

        :return: if the action is allowed or not - bool
        :rtype: bool
        """
        actionToTake = numpy.argmax(action)

        if (
            possibleActions[actionToTake] == 1
        ):  # if this specific action is part of the game
            return True
        else:
            return False

    def discardCards(self, player, action):
        """Discard a set of cards from a player's hand

        :param player: the player index
        :type player: int

        :param action: the action
        :type player: list

        :return: the discarded cards - list
        :rtype: list
        """
        cardsToDiscard = []
        actionIndex = numpy.argmax(action)
        takenAction = self.highLevelActions[actionIndex].split(";")
        cardValue = int(takenAction[0][1:])
        cardQuantity = int(takenAction[1][1:])
        jokerQuantity = int(takenAction[2][1:])

        for q in range(cardQuantity):
            cardsToDiscard.append(cardValue)
        for j in range(jokerQuantity):
            cardsToDiscard.append(12)

        self.restartBoard()

        originalCardDiscarded = cardsToDiscard.copy()
        # remove them from the players hand and add them to the board
        boardPosition = 0
        for cardIndex in range(len(self.playersHand[player])):
            for i in cardsToDiscard:
                if self.playersHand[player][cardIndex] == i:
                    self.playersHand[player][cardIndex] = 0

                    cardsToDiscard.remove(i)
                    self.board[boardPosition] = i
                    boardPosition = boardPosition + 1

        self.playersHand[player] = sorted(self.playersHand[player])
        return originalCardDiscarded

    def list_players_with_special_actions(self):
        """list players that are allowed to do a special actions

        Returns:
            _type_: list()
        """
        players_special_action = []
        for i in range(len(self.playersHand)):
            if (
                self.maxCardNumber + 1 in self.playersHand[i]
            ):  # Check if this specific player has jokers in his hand
                unique, counts = numpy.unique(self.playersHand[i], return_counts=True)
                currentPlayerHand = dict(zip(unique, counts))

                jokerQuantity = currentPlayerHand[self.maxCardNumber + 1]
                # If the player has 2 jokers, check which position it has finished
                if jokerQuantity == 2:
                    playerIndex = self.finishingOrder.index(i)

                    if playerIndex < 3:
                        specialAction = "Dinner served!"
                    else:
                        specialAction = "It is food fight!"

                    # Return the player and the type of special action they can do
                    players_special_action.append([i, specialAction])

        return players_special_action

    def declareSpecialAction(self):
        """Declare a special action (food fight/dinner is served)

        :return: if it is a special action
        :rtype: bool

        :return: if it is a food fight
        :rtype: bool
        """

        specialAction = ""
        for i in range(len(self.playersHand)):
            if self.maxCardNumber + 1 in self.playersHand[i]:
                # jokers =  self.playersHand[score[3]])
                unique, counts = numpy.unique(self.playersHand[i], return_counts=True)
                currentPlayerHand = dict(zip(unique, counts))

                jokerQuantity = currentPlayerHand[self.maxCardNumber + 1]
                if jokerQuantity == 2:
                    playerIndex = self.finishingOrder.index(i)

                    if playerIndex < 3:
                        specialAction = "Dinner served!"
                        self.currentSpecialAction = "DinnerServed"
                        self.currentPlayerDeclaredSpecialAction = i
                        return True, False
                    else:
                        specialAction = "It is food fight!"
                        self.currentSpecialAction = "FoodFight"
                        self.currentPlayerDeclaredSpecialAction = i

                        newcurrentRoles = []
                        newcurrentRoles.append(self.currentRoles[3])  # Chef
                        newcurrentRoles.append(self.currentRoles[2])  # sous-Chef
                        newcurrentRoles.append(self.currentRoles[1])  # waiter
                        newcurrentRoles.append(self.currentRoles[0])  # dishwasher
                        self.currentRoles = []
                        self.currentRoles = newcurrentRoles

                        self.exchangedCards = [i, specialAction, 0, 0]
                        return True, True

        self.currentSpecialAction = ""
        self.currentPlayerDeclaredSpecialAction = ""
        return (False, False)

    def changeRoles(self):
        """Change the player's roles, following a new game start"""

        score = self.currentRoles
        dishwasherCards = sorted(self.playersHand[score[3]])[
            0:2
        ]  # get the minimum dishwasher cards
        waiterCard = sorted(self.playersHand[score[2]])[0]  # get the minimum waiterCard
        souschefCard = sorted(self.playersHand[score[1]])[-1]
        chefCards = sorted(self.playersHand[score[0]])[-3:-1]

        # update the dishwasher cards
        for i in range(len(dishwasherCards)):
            cardIndex = self.playersHand[score[3]].index((dishwasherCards[i]))
            self.playersHand[score[3]][cardIndex] = chefCards[i]

        # update the chef cards
        for i in range(len(chefCards)):
            cardIndex = self.playersHand[score[0]].index((chefCards[i]))
            self.playersHand[score[0]][cardIndex] = dishwasherCards[i]

        # update the waiter cards
        cardIndex = self.playersHand[score[2]].index((waiterCard))
        self.playersHand[score[2]][cardIndex] = souschefCard

        # update the souschef cards
        cardIndex = self.playersHand[score[1]].index((souschefCard))
        self.playersHand[score[1]][cardIndex] = waiterCard

        self.exchangedCards = dishwasherCards, waiterCard, souschefCard, chefCards

        self.logNewRoles()

    def dealCards(self):
        """Deal the cards at the begining of a match"""
        self.numberOfCardsPerPlayer = int(len(self.cards) / len(self.playersHand))

        # For each player, distribute the amount of cards
        for playerNumber in range(len(self.playersHand)):
            self.playersHand[playerNumber] = sorted(
                self.cards[
                    playerNumber
                    * self.numberOfCardsPerPlayer : playerNumber
                    * self.numberOfCardsPerPlayer
                    + self.numberOfCardsPerPlayer
                ]
            )

        # match_number: int = 0,
        # round_number: int = 0,
        # agent_names: list = np.nan,
        # source: str = "SYSTEM",
        # action_type: str = np.nan,
        # action_description: str = np.nan,
        # player_hands: list = np.nan,
        # board_before: list = np.nan,
        # board_after: list = np.nan,
        # possible_actions: list = np.nan,
        # current_roles: list = np.nan,
        # match_score: list = np.nan,
        # game_score: list = np.nan,
        # game_performance_score: list = np.nan,

        self.experimentManager.dataSetManager.dealAction(
            match_number=self.matches, player_hands=self.playersHand
        )

    def restartBoard(self):
        """restart the board"""
        # clean the board
        self.board = []
        for i in range(self.maxCardNumber):
            self.board.append(0)

        # start the game with the highest card
        self.board[0] = self.maxCardNumber + 2
        # input ("Board:" + str(self.board))

    def hasPlayerFinished(self, player):
        """Identify it this specific player has finished the match

        :param player: the player index
        :type player: int


        :return: if the player has finished the match
        :rtype: bool
        """

        # if (
        #     self.maxRounds > -1
        #     and self.rounds >= self.maxRounds
        #     and not self.stoppedByRound
        # ):
        #     self.stoppedByRound = True
        #     positions = {}

        #     amountOfCardsByPlayer = [numpy.count_nonzero(a) for a in self.playersHand]

        #     for a, count in zip(self.playerNames, amountOfCardsByPlayer):
        #         positions[a] = count

        #     sortedPositions = dict(sorted(positions.items(), key=lambda x: x[1]))

        #     playerIndex = [self.playerNames.index(a) for a in sortedPositions.keys()]

        #     for i in playerIndex:
        #         self.finishingOrder.append(i)

        #     for p in range(len(self.playersHand)):
        #         self.playersHand[p] = numpy.zeros(len(self.playersHand[player]))

        #     return True

        return numpy.array(self.playersHand[player]).sum() <= 0
