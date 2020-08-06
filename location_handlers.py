### THIS FILE CONTAINS HANDLERS FOR YOUR LOCATIONS ###

# There are two types of location handlers:
#   * An "ENTER" HANDLER is called whenever the player enters that location.
#   * A "WHEN HERE" HANDLER is called whenever the player does anything at that location

# For either type of handler, return TRUE to bypass the other handler logic that would otherwise run
#  ...and return FALSE if you want the regular handler logic to do its thing.

# To add a new location handler, first create a function for your item
#  and then "bind" the handler to your item in the bottom section of the file.
# When you bind, make sure you choose the right Add function, depending on whether
#  you are adding an enter handler or when-here handler.
# ERIKWUZHERE


#FRONT DOOR door block
def FrontDoorHandler(context, action, item, second_item):
  if context.player.location == "OUTSIDE_MANOR":
    if (action["key"] in ["IN","NORTH"]) and not context.items["FRONT_DOOR"].get("is_open?"):
      context.Print("The front door is closed.")
      return True
  if context.player.location == "ENTRANCE_HALL":
    if (action["key"] in ["OUT","SOUTH"]) and not context.items["FRONT_DOOR"].get("is_open?"):
      context.Print("The front door is closed.")
      return True
  return False
  

#def EnterGarden(context, first_time):
 #   if first_time:
  #      context.events.PrintBelow("You hear an owl hooting from the shed.")
   #     context.events.PrintStringInNMoves("You hear that owl sound again.", 3)
    #return False

# Here is where you "bind" your item handler function to a specific item.
def Register(context):
    locations = context.locations
    #locations.AddEnterHandler("LOOKOUT_WALKWAY", EnterLookoutWalkway)
    locations.AddWhenHereHandler("OUTSIDE_MANOR", FrontDoorHandler)
    locations.AddWhenHereHandler("ENTRANCE_HALL", FrontDoorHandler)