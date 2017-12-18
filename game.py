import pygame
import random
import time

'''
The User will always be X
Computer will always be O

SMART AI IMPLEMENTATION STARTS HERE
'''


def smartAI(board,player):


    print("todo")

'''
END MINIMAX, START GAME CODE

'''
def init():
    global ORANGE,BLACK,RED,GREEN,WHITE,BLUE,YELLOW,PINK,GRAY,winner,diffslot,screen,done,clock,difficulty,playbutton,resetbutton,board,playing,board_dimensions,userturn,paintx,painto
    playing = False
  
    winner = 0
    #0 for no one, 1 for player, 2 for computer.
  
    difficulty = "Hard"
    diffslot = pygame.Rect(300,450,200,49)
    userturn = False
    #Three Dim. Array
    paintx = []
    painto = []
    board = [["-","-","-"],["-","-","-"],["-","-","-"]]
    board_dimensions = [[(55,100,125,100),(175,100,150,100),(325,100,125,100)],[(55,200,125,120),(175,200,150,125),(325,200,125,125)],[(55,325,125,100),(175,325,150,100),(325,325,125,100)]]
    #Object definitions
    playbutton = pygame.Rect(0,450,150,49)
    resetbutton = pygame.Rect(150,450,150,49)
    #Setup
    clock = pygame.time.Clock()
    done = False
    pygame.init()
    width,height = 500,500
    #Colors
    ORANGE = 255,153,51
    RED = 255,0,0
    BLACK = 0,0,0
    WHITE = 255,255,255
    BLUE = 0,255,255
    YELLOW = 255,255,0
    GRAY = 160,160,160
    PINK = 255,51,255
    GREEN = 0,128,0
    
    screen = pygame.display.set_mode((width,height))

def checkEvents():
    global done,playing,board_dimensions,board,userturn,winner
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if playing:
                    for dimension in board_dimensions:
                        for subdimension in dimension:
                            rect = pygame.Rect(subdimension)
                            if (rect.collidepoint(event.pos)):
                                print("CLICKED")
                                row = board_dimensions.index(dimension)
                                column = dimension.index(subdimension)
                                print(row)
                                print(column)
                                if userturn:
                                    if winner == 0:
                                        
                                        print(winner)
                                        placeUser(row,column)
                if (playbutton.collidepoint(event.pos)):
                    if playing:
                        return
                    userturn = True
                    playing = True
                    blitAll()
                if (resetbutton.collidepoint(event.pos)):
                    init()
                    main()
                    
                                
    return


def drawSkeleton():
    #DRAW GRID
    pygame.draw.line(screen,BLACK,(175,100),(175,425),3)
    pygame.draw.line(screen,BLACK,(325,100),(325,425),3)
    pygame.draw.line(screen,BLACK,(55,200),(445,200),3)
    pygame.draw.line(screen,BLACK,(55,325),(445,325),3)

    #Draw Buttons
    #Play Button
    pygame.draw.rect(screen,BLACK,(playbutton.x,playbutton.y,playbutton.w,playbutton.h),2)
    pygame.draw.rect(screen,BLACK,(resetbutton.x,resetbutton.y,resetbutton.w,resetbutton.h),2)


def checkWinner():
    global winner
    for row in range(0,3):
        if board[row][0] == board[row][1] and board[row][0] == board[row][2] and board[row][0] != "-":
         #  print("There is a winner!")
            if board[row][0] == "X":
                
                winner = 1
            else:
               
                winner = 2
            rect1 = pygame.Rect(board_dimensions[row][0])
            rect2 = pygame.Rect(board_dimensions[row][2])
            blitAll()
            pygame.draw.line(screen,BLACK,(rect1.centerx,rect1.centery),(rect2.centerx,rect2.centery),10)
            
    for col in range(0,3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != "-":
          #  print("There is a winner!")
            if board[0][col] == "X":
                winner = 1
            else:
                winner = 2
            rect1 = pygame.Rect(board_dimensions[0][col])
            rect2 = pygame.Rect(board_dimensions[2][col])
            blitAll()
            pygame.draw.line(screen,BLACK,(rect1.centerx,rect1.centery),(rect2.centerx,rect2.centery),10)
            
    if (board[0][0] == board[1][1] == board[2][2]) and (board[0][0] != "-"):
      #  print("There is a winner!")
        if board[0][0] == "X":
            winner = 1
        else:
            winner = 2
        rect1 = pygame.Rect(board_dimensions[0][0])
        rect2 = pygame.Rect(board_dimensions[2][2])
        blitAll()
        pygame.draw.line(screen,BLACK,(rect1.centerx,rect1.centery),(rect2.centerx,rect2.centery),10)        
     
    if (board[0][2] == board[1][1] == board[2][0]) and (board[0][2] != "-"):
        #print("There is a winner!")
        if board[0][2] == "X":
            winner = 1
        else:
            winner = 2
        rect1 = pygame.Rect(board_dimensions[0][2])
        rect2 = pygame.Rect(board_dimensions[2][0])
        blitAll()
  
        pygame.draw.line(screen,BLACK,(rect1.centerx,rect1.centery),(rect2.centerx,rect2.centery),10)        
       
 
  
   

def placeComputer():
    if difficulty == "Easy":
        global userturn
        ran1 = random.randint(0,2)
        ran2 = random.randint(0,2)
        if (board[ran1][ran2] == "-"):

            board[ran1][ran2] = "O"
            painto.append(board_dimensions[ran1][ran2])
            blitAll()
            checkWinner()
            userturn = True
            return
        else:
            try:
                placeComputer()
            except:
                print("ok")


    #Algorithm for smart placing here...
    #MINIMAX ALGORITHM IMPLEMENTATION
    print(smartAI(board,"O"))

def placeUser(row,column):
    global background,board_dimensions,board,paintx
    print("ROW: "+str(row),"Column: "+str(column))



    if board[row][column] != "O":
        board[row][column] = "X"
        print("DIMENSIONS: "+str(board_dimensions[row][column]))
        paintx.append(board_dimensions[row][column])
    
        blitAll()
        
       # time.sleep(0.8)

    #Computer turn here
    placeComputer()
    
    
def blitAll():
    global background,playing,userturn
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill(ORANGE)


    #TItle
    picture = pygame.image.load("title.png")
    picture = pygame.transform.scale(picture,(500,100))
    picturerect = picture.get_rect()
    picturerect.centerx = background.get_rect().centerx
    picturerect.centery = 50
    
    
    #End Title

    #Button Names
    
    if not playing:
        font = pygame.font.Font(None,38)
        play = font.render("Play",True,BLACK)
    else:
        font = pygame.font.Font(None,38)
        play = font.render("Playing",True,GRAY)
    playrect = play.get_rect()
    playrect.centerx = playbutton.centerx
    playrect.centery = playbutton.centery

    reset = font.render("Reset",True,BLACK)
    resetrect = reset.get_rect()
    resetrect.centerx = resetbutton.centerx
    resetrect.centery = resetbutton.centery

    if winner == 0:
        if difficulty == "Easy":
            easy = font.render("Easy",True,GREEN)
            easyrect = easy.get_rect()
            easyrect.centerx = diffslot.centerx
            easyrect.centery = diffslot.centery
            background.blit(easy,easyrect)
        else:
            hard = font.render("Hard",True,RED)
            hardrect = hard.get_rect()
            hardrect.centerx = diffslot.centerx
            hardrect.centery = diffslot.centery
            background.blit(hard,hardrect)
    else:
        if winner == 2:
            text = font.render("Comp Wins",True,RED)
        else:
            text = font.render("You Win",True,GREEN)
        textrect = text.get_rect()
        textrect.centerx = diffslot.centerx
        textrect.centery = diffslot.centery
        background.blit(text,textrect)
        oneblit = True
        
    
    #Blit Xs
    for section in paintx:
        font2 = pygame.font.Font(None,100)
        rect = pygame.Rect(section)
        X = font2.render("X",True,BLACK)
        Xrect = X.get_rect()
        Xrect.centerx = rect.centerx
        Xrect.centery = rect.centery
        background.blit(X,Xrect)
    #Blit Os
    for section in painto:
        font2 = pygame.font.Font(None,100)
        rect = pygame.Rect(section)
        O = font2.render("O",True,BLACK)
        Orect = O.get_rect()
        Orect.centerx = rect.centerx
        Orect.centery = rect.centery
        background.blit(O,Orect)
                

    print(board)
    #Draw all to screen
    background.blit(reset,resetrect)
    background.blit(picture,picturerect)
    background.blit(play,playrect)
    screen.blit(background, (0,0))
   
def main():
    global done,playing,background

    #Get background
    blitAll()
    
    while not done:
        #RESET Always 
        
        drawSkeleton() 
        checkEvents()
        checkWinner()
       

        pygame.display.flip()
        clock.tick(60)

init()
main()


    
    