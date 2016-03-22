# start of a UI art class
class Art(object):
    def __init__(self):
        """Define some artistic constants"""
        ## Artistic structures
        self.title_len = 70
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
        pass
        
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