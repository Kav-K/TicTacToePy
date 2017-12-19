import pygame
import random
import time
'''
TicTacToePy by Kaveen Kumarasinghe
Course Code: ICS3UO
Student Number: 647992

The changes and commits that this code has undergone are documented on GITHUB. My github profile can be found at https://github.com/Kav-K/TicTacToePy.git The computer game mode is smart and implements AI. It uses an implementation of the min/max algorithm from game theory to find
the best possible move


'''




'''
MIN/MAX Implementation, find the next best move


'''


def calculateComputer(board,player):
    """
    Computes the next move for a player given the current board state and also
    computes if the player will win or not.
    Takes input as a list instead of a three dimensional array like we had before, the list here is in this type of format "XX-XOO--X"

    Returns next
    """


    #This whole function plays a virtual game, so switch the player each time it is called
    if player=='O': 
        nextplayer ="X"
    else:
        nextplayer = 'O'

    result=[] # list for appending the result
    empties= board.count('-')

    #We do this to check if the board is full. This is important because it stops the recursivity below when it reaches an end state.
    if  empties is 0:
        return 0,-1


    emptylist=[] # list for storing the indexes where '-' appears
    for i in range(len(board)):
        if board[i] == '-':
            #Build the list of empties.
            emptylist.append(i)

    for i in emptylist:
        #For each empty index in the empties list, set it equal to the player, and recursively obtain the next move by playing a "Virtual game" by repeating this set of instructions recursively. Reference looked at for this was https://cwoebker.com/posts/tic-tac-toe <- Their implementation was using objects, but I was able to comprehend and port it into an implementation of my own without object oriented programming
        board[i]=player

        row,column =calculateComputer(board,nextplayer)

        result.append(row)
        #Reset the square that was changed at the end of this
        board[i]='-'
    if player == 'X':
        resultor = max(result)
        #row,column. Using emptylist, because the next move has to be a suitable placement that isn't already taken up by anything
        return row,emptylist[result.index(resultor)]
    else :
        resultor = min(result)
        return resultor,emptylist[result.index(resultor)]




'''
The User will always be X
Computer will always be O

'''
def init(_gametype):
    global ORANGE,BLACK,RED,GREEN,WHITE,BLUE,YELLOW,PINK,GRAY,winner,diffslot,screen,done,clock,difficulty,playbutton,resetbutton,board,playing,board_dimensions,userturn,paintx,gametype,painto
    playing = False

    #Can be Computer or Human
    gametype = _gametype
    winner = 0
    #0 for no one, 1 for player, 2 for computer, or 0 for no one, 1 for player 1, 2 for player 2. 3 for TIE
  
    #Slot on the right hand bottom corner that shows the game state and tie/win state.
    diffslot = pygame.Rect(300,450,200,49)


    if gametype == "Computer":
        userturn = False
    else:
        userturn = 1


    #Arrays for the blitting of Xs and Os
    #These are used to paint the Xs and Os in the blitting function
    paintx = []
    painto = []

    #Three dimensional arrays for the board
    board = [["-","-","-"],["-","-","-"],["-","-","-"]]
    board_dimensions = [[(55,100,125,100),(175,100,150,100),(325,100,125,100)],[(55,200,125,120),(175,200,150,125),(325,200,125,125)],[(55,325,125,100),(175,325,150,100),(325,325,125,100)]]


    #Rect Object definitions
    playbutton = pygame.Rect(0,450,150,49)
    resetbutton = pygame.Rect(150,450,150,49)


    #Setup
    clock = pygame.time.Clock()
    done = False
    pygame.init()
    pygame.display.set_caption('Tic Tac Toe - Kaveen Kumarasinghe')
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

'''
Check mouse click events while the game is running. Called once per loop execution
'''

def checkEvents():
    global done,playing,board_dimensions,board,userturn,winner
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

       #Monitor Events for MOUSEBUTTONDOWN, specifically button 1 (left click)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if playing:
                    #If game playing, search through the dimensions to check if the collidepoint of the click is equal to the box
                    for dimension in board_dimensions:
                        for subdimension in dimension:
                            
                            #Convert the selected box into a Rect object so we can use it later
                            rect = pygame.Rect(subdimension)

                            if (rect.collidepoint(event.pos)):

                                #Obtain row and column from the two dimensions of the for loop
                                row = board_dimensions.index(dimension)
                                column = dimension.index(subdimension)

                           

                                if userturn:
                                    #Keep allowing clicks and places as long as there are no wins
                                    if winner == 0:
                                        
                                        
                                        placeUser(row,column)
                                        
                                        

                #If the collidepoint of the event click is within the bounds of the play button, start the game playing if not already playing
                #If already playing, do nothing.
                if (playbutton.collidepoint(event.pos)):
                    if playing:
                        return
                    userturn = True
                    playing = True
                
                #Jump into program from entry points again once the collidepoint of the event click within the bounds of the reset button
                if (resetbutton.collidepoint(event.pos)):
                    init(gametype)
                    main()

                #Once the collidepoint of the event click is within the bounds of the bottom right slot, change the game mode if not already playing
                if (diffslot.collidepoint(event.pos)):
                    if not playing:
                        if gametype == "2P":
                            init("Computer")
                        elif gametype == "Computer":
                            init("2P")
                        main()
                    
                                
    return


'''
Draw the skeleton, this is used once per time in the loop
'''
def drawSkeleton():
    #DRAW GRID
    #VERTICALS
    pygame.draw.line(screen,BLACK,(175,100),(175,425),3)
    pygame.draw.line(screen,BLACK,(325,100),(325,425),3)
    #HORIZONTALS
    pygame.draw.line(screen,BLACK,(55,200),(445,200),3)
    pygame.draw.line(screen,BLACK,(55,325),(445,325),3)

    #Draw Buttons
    #Play Button
    pygame.draw.rect(screen,BLACK,(playbutton.x,playbutton.y,playbutton.w,playbutton.h),2)
    #Reset Button
    pygame.draw.rect(screen,BLACK,(resetbutton.x,resetbutton.y,resetbutton.w,resetbutton.h),2)


def checkWinner():
    global winner
    #Check for row Wins
    for row in range(0,3):
        if board[row][0] == board[row][1] and board[row][0] == board[row][2] and board[row][0] != "-":
            #Determine who wins
            if board[row][0] == "X":
                
                winner = 1
            else:
               
                winner = 2
            #Obtain the two Rect objects for the start/end winning row

            rect1 = pygame.Rect(board_dimensions[row][0])
            rect2 = pygame.Rect(board_dimensions[row][2])
            #Draw a line for the winning row, this will stay on the screen since the checkEvents function is called once per loop.
            pygame.draw.line(screen,BLACK,(rect1.centerx,rect1.centery),(rect2.centerx,rect2.centery),10)
            return True
    #Check for column wins
    for col in range(0,3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != "-":
          
            if board[0][col] == "X":
                winner = 1
            else:
                winner = 2
            rect1 = pygame.Rect(board_dimensions[0][col])
            rect2 = pygame.Rect(board_dimensions[2][col])
      
            pygame.draw.line(screen,BLACK,(rect1.centerx,rect1.centery),(rect2.centerx,rect2.centery),10)
            return True
    #Check for left to right diagonal wins
    if (board[0][0] == board[1][1] == board[2][2]) and (board[0][0] != "-"):
  
        if board[0][0] == "X":
            winner = 1
        else:
            winner = 2
        rect1 = pygame.Rect(board_dimensions[0][0])
        rect2 = pygame.Rect(board_dimensions[2][2])
       
        pygame.draw.line(screen,BLACK,(rect1.centerx,rect1.centery),(rect2.centerx,rect2.centery),10)        
        return True
    #Check for right to left diagonal wins
    if (board[0][2] == board[1][1] == board[2][0]) and (board[0][2] != "-"):
      
        if board[0][2] == "X":
            winner = 1
        else:
            winner = 2
        rect1 = pygame.Rect(board_dimensions[0][2])
        rect2 = pygame.Rect(board_dimensions[2][0])
      
  
        pygame.draw.line(screen,BLACK,(rect1.centerx,rect1.centery),(rect2.centerx,rect2.centery),10)
        return True
    #Iterate through the board to see how many filled spots there are, if there is not a win, and it is full, CALL A TIE
    nonempty = 0
    for dimension in board:
        for subdimension in dimension:
            if subdimension != "-":
                nonempty += 1
    if nonempty >= 9:
        winner = 3
    return False
       
       
 
  
   
'''
Choose a random empty spot on the board to place as a computer.

'''
def placeComputer():
 

    #Convert the board into a 1D array first
    #We'll go from a string into a list, since it is much easier to do so

    totalstring = ""
    for dimension in board:
        for subdimension in dimension:
            row = board.index(dimension)
            column = dimension.index(subdimension)
            totalstring += board[row][column]
    print(totalstring)
    #Actually Get the Result
    #Board is always O, therefore player will always be O
    resultor,calcmove =  calculateComputer(list(totalstring),"O")
    #The calculated value is for a one dimensional board, therefore we must convert it into a 3 dimensional instruction
    #This is quite trivial
    row,column = 0,0
    #make sure result is valid
    #If the board is NOT in a winning state
        
    if resultor == 0:
        if calcmove == 0:
            row = 0
            column = 0
        elif calcmove == 1:
            row = 0
            column = 1
        elif calcmove == 2:
            row = 0
            column = 2
        elif calcmove == 3:
            row = 1
            column = 0
        elif calcmove == 4:
            row = 1
            column = 1
        elif calcmove == 5:
            row = 1
            column = 3
        elif calcmove == 6:
            row = 2
            column = 0
        elif calcmove == 7:
            row = 2
            column = 1
        elif calcmove == 8:
            row = 2
            column = 2
    #If board is in a winning state in favor of the user, just randomly place something somewhere.

        



    print(row)
    print(column)

    #This section is for if the game is in a WIN state, or if there is an unknown error, it will find the closest available position that is empty and select that spot.
    try:
        board[row][column] = "O"
        painto.append(board_dimensions[row][column])
    except:
        for dimension in board:
            for subdimension in dimension:
                if (subdimension == "-"):
                       row = board.index(dimension)
                       column = dimension.index(subdimension)
                       board[row][column] = "O"
                       painto.append(board_dimensions[row][column])
                       
                       break
    userturn = True
    return





def placeUser(row,column):
    global background,board_dimensions,board,paintx,painto,userturn
  
    
    #Switch the current user as this function runs each time (If the game type is 2Player)
    if gametype == "2P":
        if userturn == 1:
            placer = "X"
        else:
            placer = "O"
        #Change which user's turn it is
        if board[row][column] == "-":
            if userturn == 1:
                userturn = 2
            elif userturn == 2:
                userturn = 1
            #Set the value of the specified square in the 3dim board array
            board[row][column] = placer
            
            #Append the value to the paintx/painto list to be drawn by the blit.
            if placer == "X":
                paintx.append(board_dimensions[row][column])
            else:
                painto.append(board_dimensions[row][column])
     
    else:
        
        #This is for when it's computer gamemode, just append the user's click to the to be drawn array and call the computer decision function
        if board[row][column] == "-":
            board[row][column] = "X"
           
            paintx.append(board_dimensions[row][column])
        
         
            placeComputer()
    
    
def blitAll():
    global background,playing,userturn
    #GEt a background surface to blit everything else to, the background surface will be blit into the main screen surface in the end.
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill(ORANGE)


    #Title
    picture = pygame.image.load("title.png")
    picture = pygame.transform.scale(picture,(500,100))
    picturerect = picture.get_rect()
    picturerect.centerx = background.get_rect().centerx
    picturerect.centery = 50
    #End Title 
    
   



    #Button Names to be blitted    
    if not playing:
        font = pygame.font.Font(None,38)
        play = font.render("Play",True,BLACK)
    else:
        font = pygame.font.Font(None,38)
        play = font.render("Playing",True,GRAY)
    playrect = play.get_rect()
    #Set the center of the button to the center of the bounds of the box Rect object that was defined on init()
    playrect.centerx = playbutton.centerx
    playrect.centery = playbutton.centery

    reset = font.render("Reset",True,BLACK)
    resetrect = reset.get_rect()
    resetrect.centerx = resetbutton.centerx
    resetrect.centery = resetbutton.centery

    #If not in a win state, display the game moode (2 Player) or (Computer)
    if winner == 0:
        if gametype == "2P":
            easy = font.render("2 Player",True,GREEN)
            easyrect = easy.get_rect()
            #Set the text centered to the diffslot (The bottom right hand corner box)
            easyrect.centerx = diffslot.centerx
            easyrect.centery = diffslot.centery
            background.blit(easy,easyrect)
        else:
            hard = font.render("Computer",True,RED)
            hardrect = hard.get_rect()
            hardrect.centerx = diffslot.centerx
            hardrect.centery = diffslot.centery
            background.blit(hard,hardrect)
    else:
        #If in a win state, display the winner, or a tie
        if winner == 2:
            if gametype == "2P":
                text = font.render("P2 Wins",True,RED)
            else:
                text = font.render("Computer Wins",True,RED)
        elif winner == 1:
            if gametype == "2P":
                text = font.render("P1 Wins",True,GREEN)
            else:
                text = font.render("You Win",True,GREEN)
        elif winner == 3:
            text = font.render("TIE",True,YELLOW)
        textrect = text.get_rect()
        textrect.centerx = diffslot.centerx
        textrect.centery = diffslot.centery
        background.blit(text,textrect)

        
    
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
                

  
    #Draw all to screen
    background.blit(reset,resetrect)
    background.blit(picture,picturerect)
    background.blit(play,playrect)
    screen.blit(background, (0,0))
   
def main():
    global done,playing,background

  
   

    #Horizontal and vertical incrementors
    #Horizontal. Determines the start position of the animation, and whether it goes backwards or forward
    forwardh = True
    backwardh = False
    horizontal = 55
    

    #Vertical, determines the start position of the animation and whether it goes downwards or upwards
    downwardv = True
    upwardv = False
    vertical = 100
    while not done:
       
        #Animation Bounds
        if horizontal == 55:
            backwardh = False
            forwardh = True
        if horizontal == 300:
            backwardh = True
            forwardh = False
        #Animation Speed
        if forwardh:
            horizontal+= 2.5
        if backwardh:
            horizontal -= 2.5

        #Animation Bounds
        if vertical == 100:
            upwardv = False
            downwardv = True
        if vertical == 290:
            downwardv = False
            upwardv = True
        #Animation Speed
        if downwardv:
            vertical += 2.5
        if upwardv:
            vertical -= 2.5  



        blitAll()

        checkEvents()

        checkWinner()

        drawSkeleton() 
        
        #Draw the animated lines using the incrementors.
        pygame.draw.line(screen,RED,(horizontal,200),(horizontal+150,200),3)
        pygame.draw.line(screen,RED,(horizontal,325),(horizontal+150,325),3)

        pygame.draw.line(screen,RED,(175,vertical),(175,vertical+150),3)
        pygame.draw.line(screen,RED,(325,vertical),(325,vertical+150),3)


        pygame.display.flip()
        #Fix Frame Rate
        clock.tick(60)




init("2P")
main()


    
    
