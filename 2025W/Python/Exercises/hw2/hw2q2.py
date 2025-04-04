side1 = int(input())
side2 = int(input())
side3 = int(input())

side1_squared = side1 ** 2
side2_squared = side2 ** 2
side3_squared = side3 ** 2

right_angle_triangle = side1_squared + side2_squared == side3_squared
area = str((side1 * side2) / 2)
acute_angle_triangle = side1_squared + side2_squared > side3_squared
obtuse_angle_triangle = side1_squared + side2_squared < side3_squared

right_angle_triangle_print = right_angle_triangle and area
acute_angle_triangle_print = acute_angle_triangle and "Acute Angle Triangle"
obtuse_angle_triangle_print = obtuse_angle_triangle and "Obtuse Angle Triangle"
print(right_angle_triangle_print or acute_angle_triangle_print or obtuse_angle_triangle_print)
