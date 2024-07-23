import math

# Calculates number of headings and subheadings in Body. Need to provide max headings and max subheadings as well as "products".
# Products can be 0 or if you need to list something, just provide the number of items to list.
def heading_calculator(min_headings, max_headings, products):
    print("Calculating headings and subheadings in body 🖥️")
    # Assuming introductory and concluding sections are required and counted separately
    min_required_main_headings = products
    max_possible_headings = max_headings - 2  # Assuming the intro and conclusion are separate

    # Start with a number of main headings equal to the number of products
    main_headings = min_required_main_headings

    # Increase main headings if possible and necessary to fit within the total range
    while main_headings <= max_possible_headings:
        # Calculate available headings for subheadings
        available_for_subheadings = max_possible_headings - main_headings
        
        # Calculate how many subheadings we can have per main heading
        if main_headings > 0:
            subheadings_per_heading = math.floor(available_for_subheadings / main_headings)
        else:
            subheadings_per_heading = 0
        
        # Check if we're within the total headings range
        total_headings = main_headings + subheadings_per_heading * main_headings
        if total_headings >= min_headings and total_headings <= max_headings:
            return main_headings, subheadings_per_heading
        
        # Increase main headings to try and find a valid configuration
        main_headings += 1
    print("Headings and subheadings in body calculated ✅")
    # If no valid configuration found, try best possible under max constraint
    return main_headings - 1, subheadings_per_heading