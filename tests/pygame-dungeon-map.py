import random
from collections import defaultdict, deque
import pygame
import sys
import math

# Initialize pygame
pygame.init()

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
        self.selected_room = None
        
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
        """Return detailed information about a room"""
        if room_id not in self.rooms:
            return f"Room {room_id} not found."
            
        room = self.rooms[room_id]
        output = f"Room: {room.name} (ID: {room.id})\n"
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
    
    def generate_map_as_grid(self, grid_size=None):
        """Generate room coordinates in a grid pattern"""
        if not self.rooms:
            return
            
        room_ids = list(self.rooms.keys())
        num_rooms = len(room_ids)
        
        # Determine grid dimensions if not provided
        if grid_size is None:
            grid_side = math.ceil(math.sqrt(num_rooms))
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
    
    def visualize_with_pygame(self, scale=100, room_radius=30):
        """Create an interactive visualization using Pygame"""
        if not self.rooms:
            print("No rooms to visualize.")
            return
        
        # Find map dimensions
        x_coords = [room.x for room in self.rooms.values()]
        y_coords = [room.y for room in self.rooms.values()]
        
        min_x, max_x = min(x_coords), max(x_coords)
        min_y, max_y = min(y_coords), max(y_coords)
        
        # Add padding
        width = (max_x - min_x + 2) * scale
        height = (max_y - min_y + 2) * scale
        
        # Ensure minimum size
        width = max(width, 800)
        height = max(height, 600)
        
        # Set up the display
        screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Dungeon Map Visualization")
        
        # Room type to color mapping
        room_colors = {
            'common': (200, 200, 200),     # Light gray
            'treasure': (255, 215, 0),     # Gold
            'monster': (205, 92, 92),      # Indian Red
            'trap': (139, 0, 0),           # Dark Red
            'boss': (220, 20, 60),         # Crimson
            'entrance': (34, 139, 34),     # Forest Green
            'exit': (65, 105, 225)         # Royal Blue
        }
        
        # Font setup
        pygame.font.init()
        font = pygame.font.SysFont('Arial', 12)
        large_font = pygame.font.SysFont('Arial', 14, bold=True)
        info_font = pygame.font.SysFont('Arial', 16)
        
        # Function to convert room coordinates to screen coordinates
        def room_to_screen(room_x, room_y):
            screen_x = (room_x - min_x + 1) * scale
            screen_y = (room_y - min_y + 1) * scale
            return screen_x, screen_y
        
        # Main visualization loop
        clock = pygame.time.Clock()
        running = True
        room_info = ""
        
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Check if a room was clicked
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    for room_id, room in self.rooms.items():
                        screen_x, screen_y = room_to_screen(room.x, room.y)
                        distance = math.sqrt((mouse_x - screen_x)**2 + (mouse_y - screen_y)**2)
                        if distance <= room_radius:
                            self.selected_room = room_id
                            room_info = self.display_room(room_id)
                            break
                
            # Clear screen
            screen.fill((30, 30, 30))  # Dark background
            
            # Draw connections between rooms
            for room_id, room in self.rooms.items():
                room_x, room_y = room_to_screen(room.x, room.y)
                
                for direction, connected_id in room.connections.items():
                    connected_room = self.rooms[connected_id]
                    connected_x, connected_y = room_to_screen(connected_room.x, connected_room.y)
                    
                    # Draw corridor
                    pygame.draw.line(screen, (150, 150, 150), (room_x, room_y), 
                                     (connected_x, connected_y), 5)
                    
                    # Draw direction indicator
                    mid_x = (room_x + connected_x) / 2
                    mid_y = (room_y + connected_y) / 2
                    
                    # Draw little rectangle at midpoint to indicate doorway
                    pygame.draw.rect(screen, (100, 100, 100), 
                                     (mid_x - 5, mid_y - 5, 10, 10))
            
            # Draw rooms
            for room_id, room in self.rooms.items():
                screen_x, screen_y = room_to_screen(room.x, room.y)
                color = room_colors.get(room.room_type, (200, 200, 200))
                
                # Draw highlighted circle if selected
                if room_id == self.selected_room:
                    pygame.draw.circle(screen, (255, 255, 255), (screen_x, screen_y), room_radius + 5)
                
                # Draw room circle
                pygame.draw.circle(screen, color, (screen_x, screen_y), room_radius)
                
                # Draw room ID
                id_text = large_font.render(str(room_id), True, (0, 0, 0))
                id_rect = id_text.get_rect(center=(screen_x, screen_y))
                screen.blit(id_text, id_rect)
                
                # Draw room name below
                name_text = font.render(room.name, True, (255, 255, 255))
                name_rect = name_text.get_rect(center=(screen_x, screen_y + room_radius + 10))
                screen.blit(name_text, name_rect)
            
            # Display room information if a room is selected
            if self.selected_room is not None and room_info:
                # Create a semi-transparent info panel
                info_surface = pygame.Surface((350, 200))
                info_surface.set_alpha(230)
                info_surface.fill((50, 50, 50))
                screen.blit(info_surface, (20, 20))
                
                # Render and display room information
                lines = room_info.strip().split('\n')
                line_height = 24
                for i, line in enumerate(lines):
                    info_text = info_font.render(line, True, (255, 255, 255))
                    screen.blit(info_text, (30, 30 + i * line_height))
            
            # Draw legend
            legend_x, legend_y = width - 160, 20
            legend_surface = pygame.Surface((140, 200))
            legend_surface.set_alpha(230)
            legend_surface.fill((50, 50, 50))
            screen.blit(legend_surface, (legend_x, legend_y))
            
            legend_title = info_font.render("Room Types", True, (255, 255, 255))
            screen.blit(legend_title, (legend_x + 10, legend_y + 10))
            
            for i, (room_type, color) in enumerate(room_colors.items()):
                y_pos = legend_y + 40 + i * 20
                pygame.draw.circle(screen, color, (legend_x + 20, y_pos), 8)
                type_text = font.render(room_type.capitalize(), True, (255, 255, 255))
                screen.blit(type_text, (legend_x + 35, y_pos - 7))
            
            pygame.display.flip()
            clock.tick(30)
        
        pygame.quit()


# Example usage
def create_sample_dungeon(num_rooms=12):
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
    grid_side = math.ceil(math.sqrt(room_count))
    dungeon.generate_map_as_grid((grid_side, grid_side))
    
    # Generate connections between rooms
    dungeon.generate_connections()
    
    # Validate the map
    is_valid = dungeon.validate_map()
    print(f"Map validation: {'Success' if is_valid else 'Failed'}")
    
    # Print the text map
    dungeon.print_map()
    
    return dungeon

# Run the example
if __name__ == "__main__":
    dungeon = create_sample_dungeon(num_rooms=500)
    dungeon.visualize_with_pygame()
