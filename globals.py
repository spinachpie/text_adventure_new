# This function is called as the game is starting. Use it to print introduction text.
def IntroText(context):
    context.Print("context.print 'Welcome adventurer'\n{inserting items into convenient locations} \nplayer.set == return True \ndef;loading_startup [remove.'binary'code] \nloading...{Traveling through hyperspace} \nIntroText(context): OUTSIDE_BUILDING \n \nType ? if you are confused")
    print()

# This function is called as the game is starting. Use it to initialize game settings
#  like the player's starting location.
def InitialSetup(context):
    context.player.SetPlayerLocation("OUTSIDE_MANOR")
    context.actions.swear_words = {"SHIT", "DAMN", "FUCK"}
    context.actions.swear_response = "A bird dropping hits you in the face for swearing!"