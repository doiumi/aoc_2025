"""Debug script to trace through the example manually."""

rotations = [('L', 68), ('L', 30), ('R', 48), ('L', 5), ('R', 60), ('L', 55), ('L', 1), ('L', 99), ('R', 14), ('L', 82)]

pos = 50
zero_count = 0

print(f"Start: pos={pos}")
print()

for i, (direction, distance) in enumerate(rotations, 1):
    old_pos = pos
    crosses = 0
    
    if direction == 'R':
        total = pos + distance
        crosses = total // 100
        zero_count += crosses
        pos = total % 100
    else:  # L
        if distance >= pos:
            crosses = 1 + ((distance - pos) // 100)
            zero_count += crosses
        pos = (pos - distance) % 100
    
    print(f"Step {i}: {direction}{distance}")
    print(f"  Old pos: {old_pos}, New pos: {pos}, Crosses: {crosses}, Total: {zero_count}")
    print()

print(f"Final zero_count: {zero_count}")
