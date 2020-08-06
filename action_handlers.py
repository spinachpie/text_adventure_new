### THIS FILE CONTAINS ACTION HANDLERS FOR YOUR ACTIONS ###

# To add a new action handler, first create a function for your action
#  and then "bind" the handler to your action in the bottom section of the file.
# Unlike location or item handlers, note that if you define an action handler, you NEED
#  to handle every user input

def Get(context, item):
    if item["key"] == "ALL":
        context.items.GetAll()
    elif item["key"] in context.player.inventory:
        context.PrintItemInString("You're already carrying @.", item)
    elif (not item.get("takeable?")):
        context.Print("You can't pick that up!")
    else:
        context.items.GetItem(item["key"])

def Drop(context, item):
    if item["key"] == "ALL":
        context.items.DropAll()
    elif not (item["key"] in context.player.inventory):
        context.PrintItemInString("You're not carrying @.", item)
    else:
        context.items.DropItem(item["key"])

def Examine(context, item):
    examine_string = item.get("examine_string")
    if (not examine_string == None) and (len(examine_string) > 0):
        context.Print(examine_string)
    else:
        context.PrintItemInString("You see nothing special about @.", item)

def Inventory(context):
    context.Print("You are carrying:")
    if len(context.player.inventory) == 0:
        context.Print("  Nothing")
    else:
        for item_key in context.player.inventory:
            context.Print("  a " + context.items.GetLongDescription(item_key))

def Help(context):
    context.Print("This is a text adventure game.")
    context.Print("Enter commands like \'NORTH\' or \'TAKE ROCK\' to tell the computer what you would like to do.")
    context.Print("Most commands are either one or two words.")
    context.Print("For a full list of commands, type \'ACTIONS\'.")

def Actions(context):
    print("Available actions:")
    for action_key in sorted(context.actions.actions_dictionary):
        if context.actions[action_key].get("suppress_in_actions_list?"):
            continue

        print_string = "  "
        i = 0
        for word in context.actions.actions_dictionary[action_key]["words"]:
            if i > 0:
                print_string += " / "
            print_string += word
            i += 1
        context.Print(print_string)

def Quit(context):
    context.state.quit_pending = True
    context.Print("Are you sure you want to quit (Y/N)?")

def Yes(context):
    context.Print("You sound really positive!")

def No(context):
    context.Print("You sound awfully negative!")

def Wait(context):
    context.Print("Time passes...")

def Type(context, item):
  if context.player.location == "DINER_INTERIOR":
    context.Print("(on the jukebox keyboard)")
    context.Print("")
    TypeOn(context, item, context.items["KEYPAD"])
  else:
    context.Print("You can't see any way to type things here.")

def TypeOn(context, item, second_item):
  if not second_item["key"] == "KEYPAD":
    context.Print("You can't type things on that!")
  elif not second_item["awaiting_input?"]:
    context.Print("Nothing happens.")
  elif not item["key"] == "NUMBER":
    context.Print("You can't type that.")
  elif item["user_value"] == None:
    context.Print("To type a number, just say something like 'type 12345'.")
  else:
    if item["user_value"] in ["001","002"]:
      context.Print("The keypad flashes three times, and then the jukebox bounces to life.")
      context.items["JUKEBOX"]["song_choice"] = item["user_value"]
      context.items["JUKEBOX"]["timer"] = 0
      context.events.CreateEventInNMoves(PlayJukebox, 0)
    else:
      context.Print("Nothing happens.")

def PlayJukebox(context):
  aha = ["We're talking away ... I don't know what ... I'm to say ...", "...TAAAAAAKE OOOOON MEEEEE (Take On Me)...", "...It's no better to be safe than sorry...", "... I'LL BEEEEEE GOOOOOOOOONE ...", "...Slowly learning that life is okay ..."]

  nas = ["Yeah, I'm gonna take my horse to the old town road...", "...Got the boots that's black to match...", "...I been in the valley ... You ain't been up off that porch, now...", "...Can't nobody tell me nothin'...", "...Cowboy hat from Gucci ... Wrangler on my booty..."]

  if context.player.location == "DINER_INTERIOR":
    printstr = "\nThe jukebox"
    if context.items["JUKEBOX"]["timer"] == 0:
      printstr += " begins playing a song slightly too loud for comfort"
    else:
      printstr += " is playing a loud song"
    printstr += ": \""
    if context.items["JUKEBOX"]["song_choice"] == "001":
      printstr += aha[context.items["JUKEBOX"]["timer"]]
    elif context.items["JUKEBOX"]["song_choice"] == "002":
      printstr += nas[context.items["JUKEBOX"]["timer"]]
    printstr += "\""
    if context.items["JUKEBOX"]["timer"] == 4:
      printstr += "\n\nThe song fades in its closing moments, and the jukebox once again is silent."
    context.Print(printstr)
  elif context.player.location == "OUTSIDE_DINER":
    context.Print("\nYou can hear the jukebox playing from inside the diner.")
  context.items["JUKEBOX"]["timer"] = context.items["JUKEBOX"]["timer"] + 1
  if context.items["JUKEBOX"]["timer"] < 5:
    context.events.CreateEventInNMoves(PlayJukebox, 1)

def Attack(context, item):
  if item["key"] == "PUNCHING_BAG":
    context.Print("You take some whacks at the punching bag. Ouch, that kind of hurt!")
  else:
    context.Print("You should try to relax.")

def Open(context, item):
  if item.get("is_door?"):
    if not item.get("is_open?"):
      context.Print("You open the door.")
      item["is_open?"] = True
    else:
      context.Print("The door is already open, you dimwit!")
  else:
    context.Print("You can't open that.")

def Close(context, item):
  if item.get("is_door?"):
    if item.get("is_open?"):
      context.Print("You close the door.")
      item["is_open?"] = False
    else:
      context.Print("The door is already closed, you dweeb!")
  else:
    context.Print("You can't close that.")

# Here is where you "bind" your action handler function to a specific action.
def Register(context):
    actions = context.actions
    actions.AddActionHandler("GET", Get)
    actions.AddActionHandler("DROP", Drop)
    actions.AddActionHandler("EXAMINE", Examine)
    actions.AddActionHandler("INVENTORY", Inventory)
    actions.AddActionHandler("HELP", Help)
    actions.AddActionHandler("ACTIONS", Actions)
    actions.AddActionHandler("QUIT", Quit)
    actions.AddActionHandler("YES", Yes)
    actions.AddActionHandler("NO", No)
    actions.AddActionHandler("WAIT", Wait)
    actions.AddActionHandler("TYPE", Type)
    actions.AddActionHandler("TYPE_ON", TypeOn)
    actions.AddActionHandler("ATTACK", Attack)   
    actions.AddActionHandler("OPEN", Open)
    actions.AddActionHandler("CLOSE", Close)