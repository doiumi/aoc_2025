"""
Day 1: Secret Entrance - Dial Safe Password Solver
This solution tracks a dial (0-99) and counts how many times it points at 0.

Part 1: Count times the dial lands on 0 after a rotation completes.
Part 2: Count times the dial passes through 0 during or after any rotation.
"""


def parse_rotations(filename):
    """
    Reads the puzzle input file and parses rotation commands.
    
    Args:
        filename (str): Path to the input file containing rotation commands
        
    Returns:
        list: List of tuples (direction, distance) where direction is 'L' or 'R'
              and distance is an integer
    """
    rotations = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                direction = line[0]  # 'L' or 'R'
                distance = int(line[1:])  # Remaining characters as integer
                rotations.append((direction, distance))
    return rotations


def apply_rotation(current_position, direction, distance):
    """
    Applies a single rotation to the dial and returns the new position.
    
    The dial is circular with values 0-99. Left rotation (L) moves toward lower
    numbers, and right rotation (R) moves toward higher numbers, wrapping around.
    
    Args:
        current_position (int): Current dial position (0-99)
        direction (str): 'L' for left or 'R' for right
        distance (int): Number of clicks to rotate
        
    Returns:
        int: New position after rotation (0-99)
    """
    if direction == 'L':
        # Left rotation subtracts from position
        new_position = (current_position - distance) % 100
    else:  # direction == 'R'
        # Right rotation adds to position
        new_position = (current_position + distance) % 100
    
    return new_position


def count_zeros_ending(rotations):
    """
    PART 1: Simulates all rotations and counts times the dial lands on 0.
    
    Only counts when the dial is pointing at 0 at the END of a rotation.
    Does not count intermediate clicks during rotation.
    
    Args:
        rotations (list): List of tuples (direction, distance) for each rotation
        
    Returns:
        int: Number of times the dial points at 0 after a rotation completes
    """
    current_position = 50  # Dial starts at 50
    zero_count = 0
    
    for direction, distance in rotations:
        current_position = apply_rotation(current_position, direction, distance)
        if current_position == 0:
            zero_count += 1
    
    return zero_count


def count_zeros_passing(rotations):
    """
    PART 2: Simulates all rotations and counts every time the dial passes 0.
    
    Counts both intermediate clicks that pass through 0 during rotation AND
    the end position if it lands on 0. This requires tracking each individual
    click during a rotation.
    
    For a rotation from position A to position B:
    - If direction is 'R' (right/increasing), count how many multiples of 100
      we cross when moving from A to B.
    - If direction is 'L' (left/decreasing), count how many multiples of 100
      we cross when moving from A backward to B.
    
    Args:
        rotations (list): List of tuples (direction, distance) for each rotation
        
    Returns:
        int: Number of times the dial points at 0 during or after any rotation
    """
    current_position = 50  # Dial starts at 50
    zero_count = 0
    
    for direction, distance in rotations:
        if direction == 'R':
            # Right rotation: moving from current_position to current_position + distance
            # Count how many times we cross 0 (which is every 100 clicks)
            # This is equivalent to: how many complete circles do we make?
            start = current_position
            end = (current_position + distance) % 100
            
            # If we're moving right and end < start, we wrapped around 0
            if end < start:
                # We definitely crossed 0 at least once
                # Calculate exact number of crossings
                zero_count += (current_position + distance) // 100
            elif end == 0:
                # We landed exactly on 0
                zero_count += ((current_position + distance) // 100)
            else:
                # We moved right but didn't cross 0
                zero_count += ((current_position + distance) // 100)
        else:  # direction == 'L'
            # Left rotation: moving from current_position to current_position - distance
            # We cross 0 if the rotation wraps around the bottom
            start = current_position
            end = (current_position - distance) % 100
            
            # If we're moving left and end > start, we wrapped around 0
            if end > start:
                # We wrapped around, so we crossed 0
                # Count how many times: it's the number of complete 100-unit distances
                zero_count += ((distance - current_position - 1) // 100 + 1)
            else:
                # We moved left but might have hit 0
                # Count crossings for left movement
                passes = distance // 100
                if current_position - (distance % 100) <= 0 < current_position:
                    passes += 1
                zero_count += passes
        
        current_position = apply_rotation(current_position, direction, distance)
    
    return zero_count


def count_zeros_passing_optimized(rotations):
    """
    PART 2: Count every time the dial REACHES position 0.
    
    Key insight: We count when the dial lands on 0, whether that's at the END
    of a rotation or DURING a rotation (when the dial passes through 0 multiple times).
    
    For RIGHT rotation from position A by distance D:
    - The dial reaches 0 each time it completes a full 100-click cycle
    - Count how many times we cross a "0 boundary" = floor((A + D) / 100)
    
    For LEFT rotation from position A by distance D:
    - If A > 0 and D > A: we go past 0 going backwards
      - Distance remaining after hitting 0: (D - A)
      - Count: 1 + floor((D - A) / 100)
    - If A == 0 and D >= 100: we're at 0 and rotate a full cycle or more
      - Count: floor(D / 100)
    - If A == 0 and D < 100: we're at 0 and rotate but don't complete a cycle
      - Count: 0 (we're just moving away from 0)
    
    Args:
        rotations (list): List of tuples (direction, distance) for each rotation
        
    Returns:
        int: Number of times the dial lands on or passes through 0
    """
    current_position = 50
    zero_count = 0
    
    for direction, distance in rotations:
        if direction == 'R':
            # Moving right - count how many boundaries of 100 we cross
            zero_count += (current_position + distance) // 100
            current_position = (current_position + distance) % 100
        else:  # direction == 'L'
            # Moving left
            if current_position > 0:
                # We're not at 0, check if we reach or pass it
                if distance >= current_position:
                    # We reach 0 at minimum, possibly pass through it
                    remaining = distance - current_position
                    zero_count += 1 + (remaining // 100)
            else:
                # We're already at position 0
                # Moving left only reaches 0 again if distance >= 100
                zero_count += distance // 100
            
            current_position = (current_position - distance) % 100
    
    return zero_count


def main():
    """
    Main function: reads input, processes rotations for both puzzles.
    """
    # Read and parse the rotation commands
    input_file = 'input.txt'
    rotations = parse_rotations(input_file)
    
    # Calculate Part 1: count times dial lands on 0 at end of rotation
    password_part1 = count_zeros_ending(rotations)
    print(f"Part 1 - Password (landing on 0): {password_part1}")
    
    # Calculate Part 2: count times dial passes through 0 during/after rotation
    password_part2 = count_zeros_passing_optimized(rotations)
    print(f"Part 2 - Password (passing through 0): {password_part2}")
    
    return password_part1, password_part2


if __name__ == "__main__":
    main()
