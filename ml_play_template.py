"""
The template of the script for the machine learning process in game pingpong
"""

# Import the necessary modules and classes
import games.pingpong.communication as comm
from games.pingpong.communication import (
    SceneInfo, GameStatus, PlatformAction
)
def update(self,scene_info):
        if scene_info["status"] != "GAME_ALIVE":
            return "RESET"
        if not self.ball_served:
            self.ball_served=True
            return "SERVE_TO_LEFT"
        else:
            if self.side == "1P":
                return "MOVE_LEFT"
            elif self.side =="2P":
                return "MOVE_RIGHT"
            else:
                return "NONE"
def ml_loop(side: str):
    ball_last=[101,101]
    comm.ml_ready()
    while True:
        scene_info = comm.get_scene_info()
        if scene_info.status == GameStatus.GAME_OVER or \
                scene_info.status == GameStatus.GAME_PASS:
            comm.ml_ready()

            scene_info = comm.get_scene_info()
        print(scene_info)

        ball_x_end = compute_x_end(scene_info.ball, ball_last)
        ball_last = scene_info.ball
        move  = (ball_x_end) - (scene_info.platform[0]+20)
        
        if move > 0:
            comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
        elif move < 0:
            comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
        else:
            comm.send_instruction(scene_info.frame, PlatformAction.NONE)
 
   
   
    """
    The main loop for the machine learning process

    The `side` parameter can be used for switch the code for either of both sides,
    so you can write the code for both sides in the same script. Such as:
    ```python
    if side == "1P":
        ml_loop_for_1P()
    else:
        ml_loop_for_2P()
    ```

    @param side The side which this script is executed for. Either "1P" or "2P".
    """

    # === Here is the execution order of the loop === #
    # 1. Put the initialization code here

    # 2. Inform the game process that ml process is ready
    comm.ml_ready()

    # 3. Start an endless loop
    while True:
        # 3.1. Receive the scene information sent from the game process
        scene_info = comm.get_scene_info()

        # 3.2. If either of two sides wins the game, do the updating or
        #      resetting stuff and inform the game process when the ml process
        #      is ready.
        if scene_info.status == GameStatus.GAME_1P_WIN or \
           scene_info.status == GameStatus.GAME_2P_WIN:
            # Do some updating or resetting stuff

            # 3.2.1 Inform the game process that
            #       the ml process is ready for the next round
            comm.ml_ready()
            continue

        # 3.3 Put the code here to handle the scene information

        # 3.4 Send the instruction for this frame to the game process
        comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
