import random
from collections import defaultdict, deque
import matplotlib.pyplot as plt
import numpy as np

class Room:
    def __init__(self, id, name, description=None, x=0, y=0):
        self.id = id
        self.name = name
        self.description = description or f"Room {id}"
        self.x = x  # Coordinates for visualization
        self.y = y
        self.connections = {}  # direction: room_id
        self.room_type = random.choice(['common', 'treasure', 'monster', 'trap', 'boss', 'entrance', 'exit'])
        
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
        
    def add_room(self, name, description=None, x=None, y=None, room_type=None):
        """Add a new room to the map"""
        self.max_room_id += 1
        if x is None or y is None:
            # Assign random coordinates if not provided
            x = random.randint(-10, 10)
            y = random.randint(-10, 10)
        
        room = Room(self.max_room_id, name, description, x, y)
        if room_type:
            room.room_type = room_type
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
        output += f"Type: {room.room_type.capitalize()}\n"
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
    
    def visualize_map(self, title="Dungeon Map Visualization", save_path=None):
        """Create a visual representation of the map using matplotlib"""
        if not self.rooms:
            print("No rooms to visualize.")
            return
        
        plt.figure(figsize=(12, 10))
        
        # Room type to color mapping
        room_colors = {
            'common': 'lightgray',
            'treasure': 'gold',
            'monster': 'indianred',
            'trap': 'darkred',
            'boss': 'crimson',
            'entrance': 'forestgreen',
            'exit': 'royalblue'
        }
        
        # Extract coordinates for all rooms
        x_coords = [room.x for room in self.rooms.values()]
        y_coords = [room.y for room in self.rooms.values()]
        
        # Draw connections between rooms
        for room_id, room in self.rooms.items():
            for direction, connected_id in room.connections.items():
                connected_room = self.rooms[connected_id]
                
                # Draw connection line
                plt.plot([room.x, connected_room.x], [room.y, connected_room.y], 'k-', alpha=0.6)
                
                # Add direction indicator (small arrow) at midpoint
                mid_x = (room.x + connected_room.x) / 2
                mid_y = (room.y + connected_room.y) / 2
                
                # Arrow direction
                dx, dy = 0, 0
                if direction == "north":
                    dx, dy = 0, 0.2
                elif direction == "south":
                    dx, dy = 0, -0.2
                elif direction == "east":
                    dx, dy = 0.2, 0
                elif direction == "west":
                    dx, dy = -0.2, 0
                
                # Add small arrow
                plt.arrow(mid_x - dx/2, mid_y - dy/2, dx, dy, head_width=0.1, 
                          head_length=0.1, fc='blue', ec='blue', alpha=0.7)
        
        # Plot rooms as circles with different colors based on type
        for room_id, room in self.rooms.items():
            color = room_colors.get(room.room_type, 'lightgray')
            circle = plt.Circle((room.x, room.y), 0.3, color=color, alpha=0.7)
            plt.gca().add_patch(circle)
            
            # Add room ID and name
            plt.text(room.x, room.y, str(room.id), 
                     horizontalalignment='center', verticalalignment='center',
                     fontweight='bold')
            
            # Add room name slightly below
            plt.text(room.x, room.y - 0.4, room.name, 
                     horizontalalignment='center', verticalalignment='center',
                     fontsize=8)
        
        # Create a legend for room types
        legend_elements = [plt.Line2D([0], [0], marker='o', color='w', 
                           markerfacecolor=color, markersize=10, label=room_type.capitalize())
                           for room_type, color in room_colors.items()]
        
        plt.legend(handles=legend_elements, loc='upper right')
        
        # Set up the plot
        plt.title(title)
        plt.grid(True, linestyle='--', alpha=0.7)
        
        # Set axis limits with some padding
        x_min, x_max = min(x_coords) - 1, max(x_coords) + 1
        y_min, y_max = min(y_coords) - 1, max(y_coords) + 1
        
        plt.xlim(x_min, x_max)
        plt.ylim(y_min, y_max)
        
        # Set equal aspect ratio
        plt.gca().set_aspect('equal')
        
        # Remove axis ticks for cleaner look
        plt.xticks([])
        plt.yticks([])
        
        # Save the figure if a path is provided
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Map visualization saved to {save_path}")
        
        # Display the plot
        plt.tight_layout()
        plt.show()
    
    def generate_map_as_grid(self, grid_size=None):
        """Generate room coordinates in a grid pattern"""
        if not self.rooms:
            return
            
        room_ids = list(self.rooms.keys())
        num_rooms = len(room_ids)
        
        # Determine grid dimensions if not provided
        if grid_size is None:
            grid_side = int(np.ceil(np.sqrt(num_rooms)))
            grid_size = (grid_side, grid_side)
            
        max_x, max_y = grid_size
        
        # Assign grid coordinates to rooms
        positions = []
        for y in range(max_y):
            for x in range(max_x):
                positions.append((x, y))
                
        # Shuffle positions for random assignment
        random.shuffle(positions)
        
        # Assign positions to rooms
        for i, room_id in enumerate(room_ids):
            if i < len(positions):
                x, y = positions[i]
                self.rooms[room_id].x = x
                self.rooms[room_id].y = y


# Example usage
def create_sample_dungeon(num_rooms=12, visualize=True):
    dungeon = DungeonMap()
    
    # Room descriptions
    room_templates = [
        ("Entrance Hall", "A grand entrance with marble floors", "entrance"),
        ("Long Hallway", "A dimly lit corridor", "common"),
        ("Ritual Chamber", "A circular room with strange symbols", "boss"),
        ("Ancient Library", "Shelves of dusty tomes line the walls", "common"),
        ("Crypt", "A cold room with stone sarcophagi", "monster"),
        ("Treasury", "Glittering gold and jewels", "treasure"),
        ("Guard Room", "Weapons hang on the walls", "monster"),
        ("Torture Chamber", "Rusty implements and dried blood", "trap"),
        ("Dining Hall", "A long table with rotting food", "common"),
        ("Kitchen", "Rusted utensils and a cold hearth", "common"),
        ("Throne Room", "A magnificent chair sits atop a dais", "boss"),
        ("Secret Passage", "A narrow, hidden corridor", "treasure"),
        ("Armory", "Racks of weapons line the walls", "treasure"),
        ("Barracks", "Rows of simple beds", "monster"),
        ("Prison Cell", "Iron bars and chains", "trap"),
        ("Alchemy Lab", "Strange liquids bubble in vials", "trap"),
        ("Chapel", "An altar to forgotten gods", "common"),
        ("Well Room", "A deep well in the center", "trap"),
        ("Storage Room", "Crates and barrels fill the space", "common"),
        ("Exit Passage", "A tunnel leading out", "exit")
    ]
    
    # Add rooms
    room_count = min(num_rooms, len(room_templates))
    selected_rooms = random.sample(room_templates, room_count)
    
    for name, desc, room_type in selected_rooms:
        dungeon.add_room(name, desc, room_type=room_type)
    
    # Arrange rooms in a grid for better visualization
    grid_side = int(np.ceil(np.sqrt(room_count)))
    dungeon.generate_map_as_grid((grid_side, grid_side))
    
    # Generate connections between rooms
    dungeon.generate_connections()
    
    # Validate the map
    is_valid = dungeon.validate_map()
    print(f"Map validation: {'Success' if is_valid else 'Failed'}")
    
    # Print the text map
    dungeon.print_map()
    
    # Show individual room details
    entrance_id = next(iter(dungeon.rooms.keys()))
    print(dungeon.display_room(entrance_id))
    
    # Create visual representation
    if visualize:
        dungeon.visualize_map(title=f"Random Dungeon Map ({room_count} Rooms)")
    
    return dungeon

# Run the example
if __name__ == "__main__":
    dungeon = create_sample_dungeon(num_rooms=50)