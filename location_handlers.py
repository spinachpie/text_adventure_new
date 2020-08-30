
### THIS FILE CONTAINS HANDLERS FOR YOUR LOCATIONS ###

# There are three types of location handlers:
#   * An "ENTER" HANDLER is called whenever the player enters that location.
#          The handler will be passed the context plus a flag which is true if this is the first
#           time the player has been here.
#   * A "WHEN HERE" HANDLER is called whenever the player does anything at that location
#          The handler will take four arguments: context, action, item1, and item2.
#          Note that some of these arguments may be None if the command is just an action
#            or an action with a single item
#   * A "LOOK" HANDLER is called whenever the player does a look at that location
#          The only parameter passed is context.

# For all types of location handlers, return TRUE to bypass the other handler logic that would otherwise run
#  ...and return FALSE if you want the regular handler logic to do its thing.

# To add a new location handler, first create a function for your item
#  and then "bind" the handler to your item in the bottom section of the file.
# When you bind, make sure you choose the right Add function, depending on whether
#  you are adding an enter handler, look handler, or when-here handler.

# NOTES ON LOCATIONS.JSON
#   * "brief_desc" = room title ("West of House")
#   * "long_desc" is the full description of the location that prints when you do a LOOK
#       -- note that you can create a LOOK handler for a more complicated description
#   * every direction (incl up/down and in/out) have optional string arguments, which can be...
#       - a location key (for simple movement) e.g. "FOREST_PATH"
#       - <location key>|<item key> (allows movement only if the item's "is_open?" flag = true)
#                                e.g. "KITCHEN|SIDE_WINDOW"
#       - a string description explaining why you can't go in that direction
#       [and you can always use a WHEN_HERE location handler to manage more complex moves]
#   * "dark?" = True if the room has no natural light source. (Can omit if false.)
#   * "touched?" = True if the player has seen the look description in this room (with light source)
#       - It's fine to check it, but PLEASE DON'T SET "touched?"!

def EnterGarden(context, first_time):
  if first_time:
    context.events.PrintBelow("You hear an owl hooting from the shed.")
    context.events.PrintStringInNMoves("You hear that owl sound again.", 3)
  return False

def JukeboxSound(context):
    if not context.items["JUKEBOX"].get("song_choice"):
        if context.player.location == "DINER_INTERIOR":
            context.Print("\nSuddenly the jukebox comes to life, plays a loud chord amid a dazzle of lights, and then goes silent again.")
        else:
            context.Print("\nFrom inside the diner, you hear the jukebox come to life, play a loud chord, and then go silent again.")

def DinerEnter(context, first_time):
    if first_time:
        context.events.CreateEventInNMoves(JukeboxSound, 5)
        context.events.PrintBelow("As you enter, you notice flashing lights on the jukebox, as if it's trying to get your attention.")
    return False

def Elevator1WhenHere(context, action, item1, item2):
    if action["key"] == "OUT":
        if context.items["ELEVATOR_DOOR"].get("is_open?"):
            if context.locations["ELEVATOR1"]["elevator_level"] == 5:
                context.locations.EnterRoom("ELEVATOR_TOP")
            elif context.locations["ELEVATOR1"]["elevator_level"] == 3:
                context.locations.EnterRoom("ELEVATOR_MIDDLE")
            elif context.locations["ELEVATOR1"]["elevator_level"] == 1:
                context.locations.EnterRoom("ELEVATOR_BOTTOM")
        else:
            context.Print("The elevator door is closed.")
        return True
    return False

def ElevatorTopWhenHere(context, action, item1, item2):
    if action["key"] in ["IN", "EAST"]:
        if context.items["ELEVATOR_DOOR"].get("is_open?") and (context.locations["ELEVATOR1"]["elevator_level"] == 5):
            context.locations.EnterRoom("ELEVATOR1")
        else:
            context.Print("The elevator door is closed.")
        return True
    return False

def ElevatorMiddleWhenHere(context, action, item1, item2):
    if action["key"] in ["IN", "EAST"]:
        if context.items["ELEVATOR_DOOR"].get("is_open?") and (context.locations["ELEVATOR1"]["elevator_level"] == 3):
            context.locations.EnterRoom("ELEVATOR1")
        else:
            context.Print("The elevator door is closed.")
        return True
    return False

def ElevatorBottomWhenHere(context, action, item1, item2):
    if action["key"] in ["IN", "EAST"]:
        if context.items["ELEVATOR_DOOR"].get("is_open?") and (context.locations["ELEVATOR1"]["elevator_level"] == 1):
            context.locations.EnterRoom("ELEVATOR1")
        else:
            context.Print("The elevator door is closed.")
        return True
    return False

def Elevator1Look(context):
    look_string = "This is a metal elevator, which is about as boring as an elevator can get. On the wall are buttons labeled 1, 2, and 3. The elevator door is "
    if context.items["ELEVATOR_DOOR"].get("is_open?"):
        look_string += "open."
    else:
        look_string += "closed."
    dest = context.locations["ELEVATOR1"].get("elevator_destination")
    if dest:
        look_string += " The button labeled "
        if dest == 1:
            look_string += "1"
        if dest == 3:
            look_string += "2"
        if dest == 5:
            look_string += "3"
        look_string += " is glowing."
    context.Print(look_string)

def ElevatorTopLook(context):
    look_string = "This room is surprisingly fancy, with a lovely tiled floor and an equally lovely chandelier. A fancy spiral staircase leads upwards. To the east is an elevator door, and a call button sits next to it. The elevator door is "
    if (context.items["ELEVATOR_DOOR"].get("is_open?")) and (context.locations["ELEVATOR1"]["elevator_level"] == 5):
        look_string += "open."
    else:
        look_string += "closed."
    dest = context.locations["ELEVATOR1"].get("elevator_destination")
    if dest:
        if dest == 5:
            look_string += " The button is glowing."
    context.Print(look_string)

def ElevatorMiddleLook(context):
    look_string = "This room isn't actually a room, but a balcony. Metal stairs lead downwards, where you can see machinery. A metal walkway continues to the northeast. To the east is an elevator door, and a call button sits next to it. The elevator door is "
    if (context.items["ELEVATOR_DOOR"].get("is_open?")) and (context.locations["ELEVATOR1"]["elevator_level"] == 3):
        look_string += "open."
    else:
        look_string += "closed."
    dest = context.locations["ELEVATOR1"].get("elevator_destination")
    if dest:
        if dest == 3:
            look_string += " The button is glowing."
    context.Print(look_string)

def ElevatorBottomLook(context):
    look_string = "This hallway is full of pipes that stick out of the walls and ceilings and continue down the passageway to the north. A bad smell comes out of room that sits to the south. To the east is an elevator door, and a call button sits next to it. The elevator door is "
    if (context.items["ELEVATOR_DOOR"].get("is_open?")) and (context.locations["ELEVATOR1"]["elevator_level"] == 1):
        look_string += "open."
    else:
        look_string += "closed."
    dest = context.locations["ELEVATOR1"].get("elevator_destination")
    if dest:
        if dest == 1:
            look_string += " The button is glowing."
    context.Print(look_string)

# Here is where you "bind" your item handler function to a specific item.
def Register(context):
    locations = context.locations
    # locations.AddEnterHandler("DINER_INTERIOR", DinerEnter)
    locations.AddWhenHereHandler("ELEVATOR1", Elevator1WhenHere)
    locations.AddWhenHereHandler("ELEVATOR_TOP", ElevatorTopWhenHere)
    locations.AddWhenHereHandler("ELEVATOR_MIDDLE", ElevatorMiddleWhenHere)
    locations.AddWhenHereHandler("ELEVATOR_BOTTOM", ElevatorBottomWhenHere)
    locations.AddLookHandler("ELEVATOR1", Elevator1Look)
    locations.AddLookHandler("ELEVATOR_TOP", ElevatorTopLook)
    locations.AddLookHandler("ELEVATOR_MIDDLE", ElevatorMiddleLook)
    locations.AddLookHandler("ELEVATOR_BOTTOM", ElevatorBottomLook)
