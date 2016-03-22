# start of a UI art class
import subprocess

class Art(object):
    def __init__(self):
        """Define some artistic constants"""
        ## Artistic structures
        self.title_len = 72
        self.flare = "~"
        self.flare2 = ":"
        self.title_start = 10*self.flare
        self.underline = self.title_len*self.flare
        
        # buffers the index for main card display
        self.index_buffer = "    " 
        self.shop_options = \
        "Shop Options :: [#] Buy Card #   [S] = Buy Supplement  [E] = Exit Shop"
        self.card_options = \
        "Card Options :: [P] Play All     [#] = Play Card #     [B] :: Buy Cards"
        self.game_options = \
        "Game Actions :: [A] Attack!      [E] = End Turn        [Q] :: Quit Game"
        self.continue_game = \
        "Game Actions :: [..] Enter to proceed                  [Q] :: Quit Game"
        self.choose_action = self.make_title("Choose_Action").replace("_"," ")
        self.welcome2 = \
        """
                                                __                          
        - - /, /,   ,- _~, _-_-      ,- _~.   ,-||-,     /\\,/\\,   ,- _~,  
          )/ )/ )  (' /| /  /,      (' /|    ('|||  )   /| || ||   (' /| /  
          )__)__) ((  ||/=  ||     ((  ||   (( |||--))  || || ||  ((  ||/=  
         ~)__)__) ((  ||   ~||     ((  ||   (( |||--))  ||=|= ||  ((  ||    
          )  )  )  ( / |    ||      ( / |    ( / |  )  ~|| || ||   ( / |    
         /-_/-_/    -____- (  -__,   -____-   -____-    |, \\,\\,   -____-  
                                                       _-                   
                                                                            
        """
        self.shop=\
        """
                                  (    )                                    
                                    )  )                                    
                                   (  (                  /\                 
                                    (_)                 /  \  /\            
                            ________[_]________      /\/    \/  \           
                   /\      /\        ______    \    /   /\/\  /\/\          
                  /  \    //_\       \    /\    \  /\/\/    \/    \         
           /\    / /\/\  //___\       \__/  \    \/                         
          /  \  /\/    \//_____\       \ |[]|     \                         
         /\/\/\/       //_______\       \|__|      \        Welcome         
        /      \      /XXXXXXXXXX\                  \          to the       
                \    /_I_II  I__I_\__________________\            Shop      
                       I_I|  I__I_____[]_|_[]_____I                         
                       I_II  I__I_____[]_|_[]_____I                         
                       I II__I  I     XXXXXXX     I                         
                    ~~~~~"   "~~~~~~~~~~~~~~~~~~~~~~~~                      
        """
        
        self.welcome = \
        """
                                                                            
                 |ZZzz                 ;;                           ::      
           |Zzz  |     |Zzz       ; :: o :: ;                   :: `:;;`::  
          /_\ /\ | /\ /_\        o::\ :| ::o/::               ` ::;;\`::\/  
          |*|_||/_\||_|*|        :::o::o;::o:;                 :::\ ::::'`  
          |.....|*|.....|     __  o :\:::/:: ;                  :`::\://::  
        __~| .. !~! .. |~___ (~ \____ | |__ ; ____________      _____| |__  
        .*.|____|_|____|.*. ('    )   | |   o             )~~~~(     |^|    
                             ~~~~~   /' `\                ~) ~  ~(  / ^ \   
                                                          )~  o<  ~~(       
                                                       )~~  ~   ~   ~~~(    
                                                    )~~    0< ~   0<   ~~(  
        """
        
        self.goodbye = \
        """
                                  ,                                         
                                 / \          JL                            
                                /   \         TT                            
                               /_____\        LJ                            
                               L=====J       J==L                           
                               J #   L\      T: T                           
                                L===J  \     L==J                           
                          .     T   T--J   =J    L=                         
                         / \    | ::|==|    T  ::T                          
                        /---\   |===|  |    L====J                          
                        L===J   |   |  |H__H__H |                           
                        T  |H__H|__H|==|     /  |                           
                        J===\     /::  |====|H__H__H                        
                _--^I^--_ ..|| ..|   ::| :: |     /                         
               / /~~|~~\ \==||===|/\  /\____|====|                          
              / /   |   \ \ ||   /__\/__\ ___  ___                          
              | |   |   | |  |===|||  ||  | | :| |                          
        ~~~~~~~ |   |o  | ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~   
              | |   |   |                                                   
        ------- |   |   | -----------------------------------------------   
        ------- |   |   | -----------------------------------------------   
        ======= |===|===| ===============================================   
                                                                            
        """
        self.goodbye_mini = \
            """                         
                  /| ________________   
            O|===|* >________________>  
                  \|                    
            """
        pass
    def check_terminal_width(self):
        """Checks the terminal can fit the game"""
        rows, columns = subprocess.check_output(['stty', 'size']).split()
        check = (int(columns) >= 78 and rows >= 90)
        return check
    
    def make_title(self, title, center=False):
        """makes a pretty title"""
        if center:
            title = title.center( self.title_len, self.flare2)
        else:
            title = title.replace(" ","_")
            title = self.title_start + title
            title = title.ljust(self.title_len)
            title = title.replace(" ", self.flare)
            title = title.replace("_"," ")
        return title