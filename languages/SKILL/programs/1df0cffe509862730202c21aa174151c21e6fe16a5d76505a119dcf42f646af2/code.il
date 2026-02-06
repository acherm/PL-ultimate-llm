; SKILL function to create a circle and calculate its area
procedure( createCircleWithArea(radius "n")
  let( (area circumference)
    ; Calculate area and circumference
    area = pi() * radius * radius
    circumference = 2.0 * pi() * radius

    ; Print results
    printf("Circle with radius %f:\n" radius)
    printf("  Area: %f\n" area)
    printf("  Circumference: %f\n" circumference)

    ; Return a list with the calculated values
    list(area circumference)
  )
)

; Example usage
createCircleWithArea(5.0)
