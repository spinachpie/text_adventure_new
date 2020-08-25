# This function is called as the game is starting. Use it to print introduction text.
def IntroText(context):
    context.Print("context.print 'Welcome adventurer'\n{inserting items into convenient locations} \nplayer.set == return True \nlist.run <milk, 2 dozen eggs, butter, 4 lbs chicken, anchovies>\ndef;loading_startup [remove.'binary'code] \nloading...{Traveling through hyperspace} \nIntroText(context): OUTSIDE_BUILDING \n \nGame created by Erik (with a little help) \n \nType ? for help")
    print()

# This function is called as the game is starting. Use it to initialize game settings
#  like the player's starting location.
def InitialSetup(context):
    context.player.SetPlayerLocation("OUTSIDE_MANOR")
    context.player.hunger_level = 0
    context.actions.swear_words = {"SHIT", "DAMN", "FUCK"}
    context.actions.swear_response = "A bird dropping hits you in the face for swearing!"
    context.events.CreateEventInNMoves(CheckHunger, 0)

def CheckHunger(context):
  context.events.CreateEventInNMoves(CheckHunger, 1)
  if context.state.debug:
    context.Print("Hunger: " + str(context.player.hunger_level))
  context.player.hunger_level += 1
  if context.player.hunger_level == 101:
    context.Print("You're starting to feel a little hungry.")
  if context.player.hunger_level == 130:
    context.Print("You are getting pretty hungry. It might be time to find a sandwich.")
  if context.player.hunger_level == 165:
    context.Print("If you don't eat soon, you will probably die. Yeah, I know it's extreme.")
  if context.player.hunger_level == 190:
    context.Print("Gandhi survived without food for 21 days. You're not Gandhi. You're about to starve.")
  if context.player.hunger_level == 200:
    context.Print("You die from hunger. Better luck next time.")
