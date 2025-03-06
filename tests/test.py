import random
from collections import defaultdict, deque

class Room:
    def __init__(self, id, name, description=None, x=0, y=0):
        self.id = id
        self.name = name
        self.description = description or f"Room {id}"
        self.x = x  # Coordinates for visualization
        self.y = y
        self.connections = {}  # direction: room_id
        
    def __repr__(self):
        return f"Room({self.id}, '{self.name}')"
        
    def add_connection(self, direction, room_id):
        self.connections[direction] = room_id
        
    def get_available_directions(self, valid_directions=None):
        """Return directions that don't have connections yet"""
        if valid_directions is None:
            valid_directions = ["north", "east", "south", "west"]
        return [d for d in valid_directions if d not in self.connections]

class DungeonMap:
    def __init__(self):
        self.rooms = {}  # id: Room
        self.max_room_id = 0
        
    def add_room(self, name, description=None, x=None, y=None):
        """Add a new room to the map"""
        self.max_room_id += 1
        if x is None or y is None:
            # Assign random coordinates if not provided
            x = random.randint(-10, 10)
            y = random.randint(-10, 10)
        
        room = Room(self.max_room_id, name, description, x, y)
        self.rooms[self.max_room_id] = room
        return room.id
        
    def connect_rooms(self, room1_id, room2_id, direction):
        """Connect two rooms in the given direction"""
        opposite_directions = {
            "north": "south", 
            "south": "north",
            "east": "west",
            "west": "east"
        }
        
        # Add the connection in both rooms
        if room1_id in self.rooms and room2_id in self.rooms:
            self.rooms[room1_id].add_connection(direction, room2_id)
            self.rooms[room2_id].add_connection(opposite_directions[direction], room1_id)
            return True
        return False
    
    def generate_connections(self, min_connections=1, max_connections=4):
        """Connect rooms to create a cohesive map"""
        if len(self.rooms) < 2:
            return False
            
        room_ids = list(self.rooms.keys())
        
        # Start with a minimum spanning tree to ensure all rooms are connected
        connected = {room_ids[0]}
        unconnected = set(room_ids[1:])
        
        # Create a connected graph (minimum spanning tree)
        while unconnected:
            best_connection = None
            best_distance = float('inf')
            
            for c_id in connected:
                c_room = self.rooms[c_id]
                
                for u_id in unconnected:
                    u_room = self.rooms[u_id]
                    
                    # Calculate Manhattan distance
                    distance = abs(c_room.x - u_room.x) + abs(c_room.y - u_room.y)
                    
                    if distance < best_distance:
                        best_distance = distance
                        best_connection = (c_id, u_id)
            
            if best_connection:
                room1_id, room2_id = best_connection
                room1 = self.rooms[room1_id]
                room2 = self.rooms[room2_id]
                
                # Determine direction based on relative positions
                if room1.x < room2.x:
                    direction = "east"
                elif room1.x > room2.x:
                    direction = "west"
                elif room1.y < room2.y:
                    direction = "north"
                else:
                    direction = "south"
                
                # Connect the rooms
                self.connect_rooms(room1_id, room2_id, direction)
                connected.add(room2_id)
                unconnected.remove(room2_id)
        
        # Add additional random connections for complexity
        additional_connections = random.randint(0, len(self.rooms) // 2)
        for _ in range(additional_connections):
            room1_id = random.choice(room_ids)
            room1 = self.rooms[room1_id]
            
            available_directions = room1.get_available_directions()
            if not available_directions:
                continue
                
            direction = random.choice(available_directions)
            
            # Find a suitable room for connection
            for room2_id in room_ids:
                if room1_id != room2_id:
                    room2 = self.rooms[room2_id]
                    
                    # Check if positions align with direction
                    if (direction == "north" and room1.x == room2.x and room1.y < room2.y) or \
                       (direction == "south" and room1.x == room2.x and room1.y > room2.y) or \
                       (direction == "east" and room1.y == room2.y and room1.x < room2.x) or \
                       (direction == "west" and room1.y == room2.y and room1.x > room2.x):
                        
                        # Check if room2 has the opposite direction available
                        opposite = {"north": "south", "south": "north", "east": "west", "west": "east"}
                        if opposite[direction] in room2.get_available_directions():
                            self.connect_rooms(room1_id, room2_id, direction)
                            break
        
        return True
    
    def print_map(self):
        """Print a text representation of the map"""
        print("\nMap Connections:")
        for room_id, room in self.rooms.items():
            print(f"Room {room_id} ({room.name}):")
            for direction, connected_id in room.connections.items():
                connected_room = self.rooms[connected_id]
                print(f"  {direction.capitalize()} -> Room {connected_id} ({connected_room.name})")
            print()
            
    def display_room(self, room_id):
        """Display detailed information about a room"""
        if room_id not in self.rooms:
            return f"Room {room_id} not found."
            
        room = self.rooms[room_id]
        output = f"\nRoom: {room.name} (ID: {room.id})\n"
        output += f"Description: {room.description}\n"
        output += "Exits:\n"
        
        if not room.connections:
            output += "  None (dead end)\n"
        else:
            for direction, connected_id in room.connections.items():
                connected_room = self.rooms[connected_id]
                output += f"  {direction.capitalize()}: {connected_room.name} (ID: {connected_id})\n"
                
        return output
        
    def validate_map(self):
        """Verify that all rooms are reachable and connections are valid"""
        if not self.rooms:
            return False
            
        # Check if all rooms are connected (BFS traversal)
        start_room_id = next(iter(self.rooms.keys()))
        visited = set()
        queue = deque([start_room_id])
        
        while queue:
            current_id = queue.popleft()
            if current_id in visited:
                continue
                
            visited.add(current_id)
            current_room = self.rooms[current_id]
            
            for connected_id in current_room.connections.values():
                if connected_id not in visited:
                    queue.append(connected_id)
        
        if len(visited) != len(self.rooms):
            return False
            
        # Check that all connections are bidirectional and valid
        opposite_directions = {
            "north": "south", 
            "south": "north",
            "east": "west", 
            "west": "east"
        }
        
        for room_id, room in self.rooms.items():
            for direction, connected_id in room.connections.items():
                if connected_id not in self.rooms:
                    return False
                    
                connected_room = self.rooms[connected_id]
                opposite = opposite_directions[direction]
                
                if opposite not in connected_room.connections or connected_room.connections[opposite] != room_id:
                    return False
        
        return True


# Example usage
def create_sample_dungeon():
    dungeon = DungeonMap()
    
    # Add some pre-existing rooms
    entrance = dungeon.add_room("Entrance Hall", "A grand entrance with marble floors")
    hallway = dungeon.add_room("Long Hallway", "A dimly lit corridor", x=0, y=1)
    chamber = dungeon.add_room("Ritual Chamber", "A circular room with strange symbols", x=1, y=1)
    library = dungeon.add_room("Ancient Library", "Shelves of dusty tomes line the walls", x=2, y=1)
    crypt = dungeon.add_room("Crypt", "A cold room with stone sarcophagi", x=0, y=2)
    treasury = dungeon.add_room("Treasury", "Glittering gold and jewels", x=1, y=2)
    
    # Generate connections between rooms
    dungeon.generate_connections()
    
    # Validate the map
    is_valid = dungeon.validate_map()
    print(f"Map validation: {'Success' if is_valid else 'Failed'}")
    
    # Print the map
    dungeon.print_map()
    
    # Show individual room details
    print(dungeon.display_room(entrance))
    
    return dungeon

# Run the example
if __name__ == "__main__":
    dungeon = create_sample_dungeon()