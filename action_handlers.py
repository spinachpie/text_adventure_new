
### THIS FILE CONTAINS ACTION HANDLERS FOR YOUR ACTIONS ###

# To add a new action handler, first create a function for your action
#  and then "bind" the handler to your action in the bottom section of the file.
# Unlike location or item handlers, note that if you define an action handler, you NEED
#  to handle every user input
#
# Different types of actions get different parameters:
#   * one-word actions (e.g. INVENTORY) just get passed context.
#   * two-word actions (e.g. OPEN) and three-word actions (e.g. TURN ON) get passed context and a single item object.
#   * four word actions (e.g. PUT ITEM IN ITEM) get passed context and two objects

# Ideally, these action handlers are generic and don't reference specific items or locations.
# But that's up to you...

# NOTES ON ACTIONS.JSON
#       "words" : a list containing all words for the action
#       "requires_object?" : true if the item needs an object (required for all 2-, 3-, and 4-word actions)
#       "prepositions" : list containing all prepositions associated with the action (required for 3- and 4-word actions)
#                   -- note that prepositions are key for disambiguating between actions with overlapping words
#                       (e.g. "PUT IN" vs "PUT ON").
#                   -- You can't have two actions with overlapping words AND overlapping prepositions
#       "no_second_item?" : set to true for items with prepositions but only one item (e.g. TURN ON ITEM)
#                   -- this distinguishes 3-word actions from 4-word actions
#       "is_move?" : true if this is a movement action (always one word)
#       "suports_all?" : true if the action supports the ALL object (e.g. TAKE ALL)
#       "suppress_in_actions_list?" : true if you don't want this action to show up when player types ACTIONS

def Get(context, item):
    if item["key"] == "ALL":
        context.items.GetAll()
    elif item["key"] in context.player.inventory:
        context.PrintItemInString("You're already carrying @.", item)
    elif (not item.get("takeable?")):
        context.Print("You can't pick that up!")
    else:
        context.items.GetItem(item["key"])

def GetFrom(context, item, second_item):
    if item["key"] == "ALL":
        context.items.GetAllFrom(second_item)
    else:
        contents = second_item.get("contents")
        if (not contents) or (not item["key"] in contents):
            context.PrintItemInString("@ isn't inside that.", item)
        elif (not item.get("takeable?")):
            context.Print("You can't pick that up!")
        else:
            context.items.GetItem(item["key"])

def Remove(context, item):
    for container_key in context.items.items_dictionary:
        if item["key"] in context.items[container_key]["contents"]:
            context.PrintItemInString("(from @)\n", context.items[container_key])
            GetFrom(context, item, context.items[container_key])
            return
    context.PrintItemInString("I don't understand how to do that.", item)

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

def Open(context, item):
  if item.get("openable?"):
    if not item.get("is_open?"):
      if item.get("is_locked?"):
        context.PrintItemInString("@ is locked.", item)
      elif (item.get("is_container?") and len(item["contents"])):
        context.Print("Opening the " + item["name"] + " reveals:")
        context.items.ListItems(item["contents"], indent=2)
      else:
        context.PrintItemInString("You open @.", item)
      item["is_open?"] = True
    else:
      context.PrintItemInString("@ is already open.", item)
  else:
    context.Print("You can't open that.")

def Eat(context, item):
    if item.get("is_food?"):
        if context.player.hunger_level >= 75:
            context.PrintItemInString("You eat @ and feel less hungry.", item)
            context.player.hunger_level -= 100
            context.items.RemoveItemFromGame(item)
        else:
            context.Print("You aren't hungry at the moment.")
    else:
        context.Print("Didn't your parents teach you not to put things in your mouth!?")

def Close(context, item):
  if item.get("openable?"):
    if item.get("is_open?"):
      context.PrintItemInString("You close @.", item)
      item["is_open?"] = False
    else:
      context.PrintItemInString("@ isn't open.", item)
  else:
    context.Print("You can't close that.")

def TurnOn(context, item):
    context.Print("You can't turn that on.")

def TurnOff(context, item):
    context.Print("You can't turn that off.")

def Inventory(context):
    context.Print("You are carrying:")
    context.items.ListItems(context.player.inventory, indent=2)    

def Help(context):
    context.Print("This is a text adventure game.")
    context.Print("Enter commands like \'NORTH\'(or 'N') or \'TAKE COIN\' to tell the computer what you would like to do.")
    context.Print("For a full list of commands, type \'ACTIONS\'.")

def PrintAction(context, action_key):
    print_string = "  " + context.actions[action_key]["words"][0]
    if context.actions[action_key].get("requires_object?"):
            print_string += " item"
    preps = context.actions[action_key].get("prepositions")
    if preps:
        print_string += " "
        for j in range(len(preps)):
            if (j>0):
                print_string += "/"
            print_string += preps[j]
        if not context.actions[action_key].get("no_second_item?"):
            print_string += " item"

    if len(context.actions[action_key]["words"]) > 1:
        print_string += " ... (or "
        for i in range(1,len(context.actions[action_key]["words"])):
            if i > 1:
                print_string += "/"
            print_string += context.actions[action_key]["words"][i]
        print_string += ")"
        
    context.Print(print_string)

def Actions(context):
    print("Movement:")
    for action_key in context.actions.actions_dictionary:
        if context.actions[action_key].get("suppress_in_actions_list?"):
            continue
        if not context.actions[action_key].get("is_move?"):
            continue

        PrintAction(context, action_key)
    #insert witty remark here
    print("\nOther actions:")
    for action_key in sorted(context.actions.actions_dictionary):
        if context.actions[action_key].get("suppress_in_actions_list?"):
            continue
        if context.actions[action_key].get("is_move?"):
            continue

        PrintAction(context, action_key)

def Save(context):
    context.SaveGame()

def Restore(context):
    context.state.restore_requested = True

def Quit(context):
    context.state.quit_pending = True
    context.Print("Are you sure you want to quit (Y/N)?")

def Restart(context):
    context.state.restart_pending = True
    context.Print("Are you sure you want to restart (Y/N)?")

def Yes(context):
    context.Print("I agree!")

def No(context):
    context.Print("I know, it's so unfair.")

def Wait(context):
    context.Print("Time passes...")

def Insert(context, item):
    context.Print("You can't insert that.")    

def PutIn(context, item, second_item):
    if (item["key"] == "ALL") and (not second_item == None) and second_item.get("is_container?"):
        context.items.PutAllIn(second_item)
    elif not item["key"] in context.player.inventory:
        context.PrintItemInString("You're not holding the @.", item)
    elif (not second_item == None) and second_item.get("is_container?"):
        if (item["key"] == second_item["key"]) or context.items.TestIfItemIsIn(second_item, item):
            context.Print("That's impossible!")
        elif second_item.get("openable?") and not second_item.get("is_open?"):
            context.PrintItemInString("The @ is closed.", second_item)
        else:
            context.Print("Done.")
            context.player.inventory.remove(item["key"])
            second_item["contents"].append(item["key"])
    else:
      context.Print("You can't do that.")

def Type(context, item):
    context.Print("You can't type that.")

def TypeOn(context, item, second_item):
    context.Print("You can't do that.")

def Attack(context, item):
    context.Print("You should try to relax.")

def Debug(context):
    context.state.debug = not context.state.debug
    context.Print("Debugging toggled.")

def Twiggy2(context):
    context.locations.EnterRoom("THE_VOID") 

def Chicken(context):
    context.Print("ERROR 404: Chicken Egg does not compute ... Chicken Egg does not compute ... Ch101e0 E1g d001 n01 c0mpu10 ... 1101001 001 1010 000 1101011 ... REACTOR MELTDOWN IN 3 ... 2 ... 1 ... ")
    context.player.Kill()

def Credits(context):
    context.Print("\n Thank you for playing 'ERIK_GAME'\n\nStory: Erik\nCharacters: Erik\nAll the hard coding stuff: All Erik\nSound Design: Erik \nThat cool map: Erik (It was actually Erik and it took forever)\nSpecial FX: Erik\nPublishing: Erik Inc\n\nProud Sponsors: \nAir Erik\nMicrosoft \nThe Daily Bok\nThe Belgian Department of Agriculture\n\nSpecial Thanks To:\nErik\nFinn\nErik's hour and a half of \"PE\" class\nTomas (He helped a tiny bit)")

# Here is where you "bind" your action handler function to a specific action.
def Register(context):
    actions = context.actions
    actions.AddActionHandler("GET", Get)
    actions.AddActionHandler("GET_FROM", GetFrom)
    actions.AddActionHandler("REMOVE", Remove)
    actions.AddActionHandler("DROP", Drop)
    actions.AddActionHandler("EXAMINE", Examine)
    actions.AddActionHandler("OPEN", Open)
    actions.AddActionHandler("CLOSE", Close)
    actions.AddActionHandler("INSERT", Insert)
    actions.AddActionHandler("PUT_INTO", PutIn)
    actions.AddActionHandler("INVENTORY", Inventory)
    actions.AddActionHandler("HELP", Help)
    actions.AddActionHandler("ACTIONS", Actions)
    actions.AddActionHandler("QUIT", Quit)
    actions.AddActionHandler("RESTART", Restart)
    actions.AddActionHandler("SAVE", Save)
    actions.AddActionHandler("RESTORE", Restore)
    actions.AddActionHandler("YES", Yes)
    actions.AddActionHandler("NO", No)
    actions.AddActionHandler("WAIT", Wait)
    actions.AddActionHandler("TYPE", Type)
    actions.AddActionHandler("TYPE_ON", TypeOn)
    actions.AddActionHandler("ATTACK", Attack)
    actions.AddActionHandler("DEBUG", Debug)
    actions.AddActionHandler("TURN_ON", TurnOn)
    actions.AddActionHandler("TURN_OFF", TurnOff)
    actions.AddActionHandler("TWIGGY2", Twiggy2)
    actions.AddActionHandler("EAT", Eat)
    actions.AddActionHandler("CHICKEN", Chicken)
    actions.AddActionHandler("CREDITS", Credits)