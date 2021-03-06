# This function is called as the game is starting. Use it to print introduction text.
def IntroText(context):
    context.Print(
        "context.print 'Welcome adventurer'\n{inserting items into convenient locations} \nplayer.set == return True \nloading...[Traveling through hyperspace]  \n \nGame created by Erik (with a little help) \n \nType ? for help \nSave game by typing 'SAVE' and restore a save by typing 'RESTORE'\n---------------------------------------------------------------------------")
    print()

# This function is called as the game is starting. Use it to initialize game settings
#  like the player's starting location.
def InitialSetup(context):
    context.player.SetPlayerLocation("PARK")
    context.player.hunger_level = 0
    context.actions.swear_words = ["SHIT", "DAMN", "FUCK"]
    context.actions.swear_response = "Let's keep this PG, folks. Next time there'll be consequences."
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
    context.Print("You die from hunger. Don't say we didn't warn you!")
    context.player.Kill()
