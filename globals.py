# This function is called as the game is starting. Use it to print introduction text.
def IntroText(context):
    context.Print("context.print 'Welcome adventurer'\n{inserting items into useful locations} \nplayer.set == return True \ndef;loading_startup [remove.'binary'code = true] \nIntoText(context): OUTSIDE_MANOR")
    print()

# This function is called as the game is starting. Use it to initialize game settings
#  like the player's starting location.
def InitialSetup(context):
    context.player.SetPlayerLocation("OUTSIDE_MANOR")
    context.actions.swear_words = {"SHIT", "DAMN"}
    context.actions.swear_response = "Hey, watch your language!"