
class Robot_nn(Robot):
    def __init__(self, p1=True, model=None):
        super().__init__(p1)
        self.n_games = 0
        self.epsilon = 0 # randomness
        self.gamma = 0.9 # discount rate
        self.memory = deque(maxlen=MAX_MEMORY) # popleft()
        if model is None:
            self.model = Linear_QNet(R*C, 256, C)
        else:
            self.model=model
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)
    def change_role(self, p1):
        self.p1=p1
    def calculate_reward(self, board1, board2):
        # take a look, how many more points do you get

        pass
    def train_short(self):
        pass
    def train_long(self):
        pass
    def remember(self):
        pass
    def _choose_pos(self, board_flatten):
        # random moves: tradeoff exploration / exploitation
        self.epsilon = 80 - self.n_games
        if random.randint(0, 200) < self.epsilon:
            pos1 = random.randint(0, C-1)
            return pos1
        else:
            state0 = torch.tensor(board_flatten, dtype=torch.float)
            prediction = self.model(state0)
            pos1 = torch.argmax(prediction).item()
        return pos1
    def choose_pos(self, board):
        # reverse if necessary
        if self.p1:
            board1=board.copy()
        else:
            board1=self.reverse_board(board)
        board1_flatten=board1.flatten()
        # predict
        pos1=self._choose_pos(board1_flatten)
        board2 = board1.copy()
        # fantacy move
        self.move_fantacy(board2, pos1, 1)
        board2_flatten=board2.flatten()
        self.calculate_reward(board1, board2)
        self.train_short()
        return pos1
    

def train():
    g1=Game()
    trainee=Robot_nn()
    while True:
        if bool(random.getrandbits(1)): # randomly choose mode
            r1=Robot(True)
            trainee.change_role(False)
            r2=trainee
        else:
            trainee.change_role(True)
            r1=trainee
            r2=Robot(False)
        while True:
            pos1=r1.choose_pos(g1.board)
            legal=g1.move(pos1)
            if not legal:
                message='P1 played illegal move, P2 wins'
                break
            g1.draw()
            message=g1.win_check()
            if len(message):
                break
            time.sleep(1)

            pos2=r2.choose_pos(g1.board)
            legal=g1.move(pos2)
            if not legal:
                message='P2 played illegal move, P1 wins'
                break
            g1.draw()
            message=g1.win_check()
            if len(message):
                break
            time.sleep(1)
            # auswerten

        print(message)
        g1.reset()