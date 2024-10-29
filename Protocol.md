## AI protocol

| SYMBOL  |             MEANING              |
|:-------:|:--------------------------------:|
|  size   |         size of the map          |
|    X    |       horizontal position        |
|    Y    |        vertical position         |
|  field  | 1-own stone \ 2-opponent's stone |
|  width  |    Correspond to X coordinate    |
| height  |    Correspond to Y coordinate    |
| message |          Error message           |

<br>

### KEY

|      KEY      |                                             DESCRIPTION                                             |
|:-------------:|:---------------------------------------------------------------------------------------------------:|
| timeout_turn  |              Maximum time in milliseconds for each turn (0 = play as fast as possible)              |
| timeout_match |                   Maximum time in milliseconds for the whole game (0 = no limit)                    |
|  max_memory   |                               Maximum memory in bytes (0 = no limit)                                |
|   time_left   |                            Remaining time of the player in milliseconds                             |
|   game_type   |     0 = opponent is human<br>1 = opponent is an AI<br>2 = tournament<br>3 = network tournament      |
|     rule      | Bitmask or sum of:<br>1 = exactly five in a row win<br>2 = continuous game<br>4 = renju<br>8 = caro |
|   evaluate    |                 Coordinates X, Y representing current position of the mouse cursor                  |

<br>

### COMMANDS

|                   MANAGER                   |                                       AI                                       |                                                                  DETAILS                                                                  | MANDATORY |
|:-------------------------------------------:|:------------------------------------------------------------------------------:|:-----------------------------------------------------------------------------------------------------------------------------------------:|:---------:|
|               START size\r\n                |                         OK\r\n \|\| ERROR message\r\n                          |                               Map size for the game (send ERROR + message if the map size is not supported)                               |     ✅     |
|                TURN X,Y\r\n                 |                                    X,Y\r\n                                     |                        The parameters are coordinate of the opponent's move (all coordinates are numbered from 0)                         |     ✅     |
|                  BEGIN\r\n                  |                                    X,Y\r\n                                     |                     The command is send to one of the AI at the begin of the game(the AI have to play on empty board)                     |     ✅     |
| BOARD<br>X,Y,field<br>X,Y,field<br>DONE\r\n |                                    X,Y\r\n                                     |                     The command is send to one of the AI at the begin of the game(the AI have to play on empty board)                     |     ✅     |
|             INFO key value\r\n              |                                      none                                      |                                                 Send information set for the current game                                                 |     ✅     |
|                   END\r\n                   |                                      none                                      |                                AI have to terminate as soon as possible (should delete its temporary file)                                |     ✅     |
|                  ABOUT\r\n                  | name="[NAME]", version="[VERSION]", author="[AUTHOR]", country="[COUNTRY]"\r\n |                                            AI have to sent information about itself on oneline                                            |     ✅     |
|          RECSTART width height\r\n          |                         OK\r\n \|\| ERROR message\r\n                          |                                             Same command as START but with a rectangular map                                              |     ❌     |
|                 RESTART\r\n                 |                                     OK\r\n                                     |                           Clear board and restart a new match (communication continue as after a START command)                           |     ❌     |
|              TAKEBACK X,Y\r\n               |                                     OK\r\n                                     |                              This command is use to undo the last move (remove the stone at coordinate X, Y)                              |     ❌     |
|                PLAY X,Y\r\n                 |                                    X,Y\r\n                                     |                                       Command send by the manager as a response of SUGGEST command                                        |     ❌     |
|             SWAP2BOARD X,Y\r\n              |                                    X,Y\r\n                                     |                                                      Details TODO, very long command                                                      |     ❌     |
|                                             |                              UNKNOWN message\r\n                               |                             The AI send it as a respond of a command which is unknown or not yet implemented                              |     ✅     |
|                                             |                               ERROR message\r\n                                |                              The AI send it as a respond of a command which is implemented but can't be done                              |     ✅     |
|                                             |                              MESSAGE message\r\n                               |                  Message to send to the manager, which can be log in a console (it must not contain new line character)                   |     ✅     |
|                                             |                               DEBUG message\r\n                                |                          Same function as MESSAGE but it'll not be display during Gomocup (it help AI developer)                          |     ✅     |
|                                             |                                SUGGEST X,Y\r\n                                 | The AI can answer SUGGEST instead of X, Y,the manager can ignore AI suggestion and force another move.<br>Expected answer are PLAY or END |     ❌     |


> **Note:** The AI must be able to play on a board of size 20.