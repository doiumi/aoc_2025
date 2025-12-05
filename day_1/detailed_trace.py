"""Detailed trace of the algorithm to verify correctness."""

from solution import parse_rotations

rotations = parse_rotations('input.txt')

# Test with the example first
example_rotations = [('L', 68), ('L', 30), ('R', 48), ('L', 5), ('R', 60), ('L', 55), ('L', 1), ('L', 99), ('R', 14), ('L', 82)]

print("=" * 80)
print("EXAMPLE TRACE")
print("=" * 80)

pos = 50
zero_count = 0

for i, (direction, distance) in enumerate(example_rotations, 1):
    old_pos = pos
    crosses = 0
    
    if direction == 'R':
        # Right rotation
        total = pos + distance
        crosses = total // 100
        zero_count += crosses
        pos = total % 100
        print(f"Step {i}: R{distance}")
        print(f"  Move right from {old_pos}")
        print(f"  Total distance: {total}, Crosses: {crosses} (total // 100 = {total // 100})")
        print(f"  Final position: {pos}")
    else:
        # Left rotation
        if distance >= pos:
            crosses = 1 + ((distance - pos) // 100)
            zero_count += crosses
        pos = (pos - distance) % 100
        print(f"Step {i}: L{distance}")
        print(f"  Move left from {old_pos}")
        if distance >= old_pos:
            print(f"  Goes past 0: yes")
            print(f"  Remaining after hitting 0: {distance - old_pos}")
            print(f"  Crosses: 1 + {(distance - old_pos) // 100} = {crosses}")
        else:
            print(f"  Goes past 0: no")
            print(f"  Crosses: {crosses}")
        print(f"  Final position: {pos}")
    
    print(f"  Running total: {zero_count}")
    print()

print(f"Example total: {zero_count} (expected: 8)")
print()

# Now trace the actual input
print("=" * 80)
print("ACTUAL INPUT TRACE (first 20 rotations)")
print("=" * 80)

pos = 50
zero_count = 0

for i, (direction, distance) in enumerate(rotations[:20], 1):
    old_pos = pos
    crosses = 0
    
    if direction == 'R':
        total = pos + distance
        crosses = total // 100
        zero_count += crosses
        pos = total % 100
    else:
        if distance >= pos:
            crosses = 1 + ((distance - pos) // 100)
            zero_count += crosses
        pos = (pos - distance) % 100
    
    print(f"{i:2d}. {direction}{distance:4d}: {old_pos:2d} -> {pos:2d}, +{crosses}, total={zero_count}")

print()
print(f"Total after 20 rotations: {zero_count}")
print()

# Full trace for actual input
pos = 50
zero_count = 0

for direction, distance in rotations:
    if direction == 'R':
        total = pos + distance
        crosses = total // 100
        zero_count += crosses
        pos = total % 100
    else:
        if distance >= pos:
            crosses = 1 + ((distance - pos) // 100)
            zero_count += crosses
        pos = (pos - distance) % 100

print(f"FINAL ANSWER FOR PART 2: {zero_count}")
