from BattleZone.models import Player

def addPlayer(player, room):
    new_player = Player(player=player, next=None, prev=None, in_room=room.room_code)
    new_player.save()

    new_player.prev = room.tail
    new_player.save()
    room.tail.next = new_player
    room.tail.save()
    room.tail = new_player
    room.tail.save()
    room.currentPlayersCount+=1
    room.save()

def removePlayer(room, player):
    node = room.head
    node.save()
    while node is not None:
        if node.player == player:
            prev_node = node.prev
            next_node = node.next
            if prev_node is not None:
                prev_node.next = node.next
                prev_node.save()
            if next_node is not None:
                next_node.prev = node.prev
                next_node.save()
            
            room.currentPlayersCount = room.currentPlayersCount - 1
            room.save()
            node.delete()
            node = None
        else:
            node = node.next
            node.save()