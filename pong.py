# import libraries
import simpleguitk as simplegui
import random


# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
PADDLE_VEL = 4


# helper function that spawns a ball by updating the 
# ball's position vector and velocity vector
# if right is True, the ball's velocity is upper right, else upper left
def ball_init(right):
    global ball_pos, ball_vel # these are vectors stored as lists

    # centre ball
    ball_pos = [WIDTH / 2, HEIGHT / 2]

    # randomise values for velocities
    horizontal_vel = random.randrange(120, 240) / 60
    vertical_vel = random.randrange(60, 180) / 60
    
    if right == True:
        ball_vel = [horizontal_vel, - vertical_vel]
    else:
        ball_vel = [- horizontal_vel, - vertical_vel]


# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel
    global score1, score2
    global initial_ball_direction
    
    # initialise paddle velocities for the key up/down handlers
    paddle1_vel = 0.0
    paddle2_vel = 0.0
    
    # make a random choice of true/false for ball direction
    initial_ball_direction = random.choice([True, False])
    ball_init(initial_ball_direction)
    
    # centralise the paddle positions
    paddle1_pos = HEIGHT / 2
    paddle2_pos = HEIGHT / 2
    
    # initialise scores
    score1 = 0
    score2 = 0
    
    
def draw(c):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, initial_ball_direction

    # update paddle's vertical position, keep paddle on the screen
    if paddle1_pos + paddle1_vel >= HALF_PAD_HEIGHT and paddle1_pos + paddle1_vel <= HEIGHT - HALF_PAD_HEIGHT:
        paddle1_pos += paddle1_vel
    if paddle2_pos + paddle2_vel >= HALF_PAD_HEIGHT and paddle2_pos + paddle2_vel <= HEIGHT - HALF_PAD_HEIGHT:
        paddle2_pos += paddle2_vel
        
    # draw mid line and gutters
    c.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    c.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    c.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
    
    # draw paddles
    c.draw_line([HALF_PAD_WIDTH, paddle1_pos - HALF_PAD_HEIGHT], [HALF_PAD_WIDTH, paddle1_pos + HALF_PAD_HEIGHT], PAD_WIDTH, "White")
    c.draw_line([WIDTH - HALF_PAD_WIDTH, paddle2_pos - HALF_PAD_HEIGHT], [WIDTH - HALF_PAD_WIDTH, paddle2_pos + HALF_PAD_HEIGHT], PAD_WIDTH, "White")
     
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    
    # check for paddle and gutter collision and reverse ball if point is scored
    
    # left wall
    if ball_pos[0] <= BALL_RADIUS + PAD_WIDTH:
        if ball_pos[1] >= paddle1_pos - HALF_PAD_HEIGHT and ball_pos[1] <= paddle1_pos + HALF_PAD_HEIGHT:
            
            # add 10% velocity then reverse motion
            ball_vel[0] += ball_vel[0] * 0.1
            ball_vel[0] = - ball_vel[0]
        else: 
            # give point to right player
            score2 += 1
            
            # new round with ball going towards winner
            ball_init(True)
    
    # right wall
    elif ball_pos[0] >= ((WIDTH - 1) - (BALL_RADIUS + PAD_WIDTH)):
        if ball_pos[1] >= paddle2_pos - HALF_PAD_HEIGHT and ball_pos[1] <= paddle2_pos + HALF_PAD_HEIGHT:
            
            # add 10% velocity then reverse motion
            ball_vel[0] += ball_vel[0] * 0.1
            ball_vel[0] = - ball_vel[0]
        else:
            # give point to left player
            score1 += 1
            
            # new round with ball going towards winner
            ball_init(False)
    
    # check for top and bottom collision
    if ball_pos[1] <= BALL_RADIUS or ball_pos[1] >= ((HEIGHT - 1) - BALL_RADIUS):
        ball_vel[1] = - ball_vel[1]
            
    # draw ball and scores
    c.draw_circle(ball_pos, BALL_RADIUS, 1, "White", "White")
    c.draw_text(str(score1), [WIDTH / 4, 50], 38, "White", "monospace")
    c.draw_text(str(score2), [WIDTH / 2 + WIDTH / 4, 50], 38, "White", "monospace")
    
        
def keydown(key):
    global paddle1_vel, paddle2_vel

    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel -= PADDLE_VEL
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel += PADDLE_VEL
    
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel -= PADDLE_VEL
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel += PADDLE_VEL
    
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel += PADDLE_VEL
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel -= PADDLE_VEL
    
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel += PADDLE_VEL
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel -= PADDLE_VEL

        
def	reset():
    new_game()


# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Reset game", reset, 100)


# start frame
frame.start()
new_game()
