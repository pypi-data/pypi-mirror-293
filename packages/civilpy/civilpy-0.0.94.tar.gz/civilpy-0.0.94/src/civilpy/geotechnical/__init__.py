import math

def rankine_active_pressure(unit_weight, height, friction_angle):
    """
    Calculate active earth pressure against an abutment using the Rankine method.

    Parameters:
    unit_weight (float): Unit weight of the soil (kN/m³ or lb/ft³)
    height (float): Height of the abutment (meters or feet)
    friction_angle (float): Internal friction angle of the soil (degrees)

    Returns:
    float: Active earth pressure (kN/m or lb/ft)
    """

    # Convert the friction angle to radians
    friction_angle_rad = math.radians(friction_angle)

    # Calculate the active earth pressure coefficient (Ka)
    Ka = math.tan(math.radians(45) - friction_angle_rad / 2) ** 2

    # Calculate the active earth pressure (Pa)
    Pa = 0.5 * unit_weight * height ** 2 * Ka

    return Pa


def rankine_active_pressure_with_surcharge(unit_weight, height, friction_angle, surcharge_load):
    """
    Calculate active earth pressure against an abutment using the Rankine method with a surcharge load.

    Parameters:
    unit_weight (float): Unit weight of the soil (kN/m³ or lb/ft³)
    height (float): Height of the abutment (meters or feet)
    friction_angle (float): Internal friction angle of the soil (degrees)
    surcharge_load (float): Surcharge load at the surface (kN/m² or lb/ft²)

    Returns:
    float: Active earth pressure (kN/m² or lb/ft²)
    """

    # Convert the friction angle to radians
    friction_angle_rad = math.radians(friction_angle)

    # Calculate the active earth pressure coefficient (Ka)
    Ka = math.tan(math.radians(45) - friction_angle_rad / 2) ** 2

    # Calculate the active earth pressure due to soil (Pa_soil)
    Pa_soil = 0.5 * unit_weight * height ** 2 * Ka

    # Calculate the active earth pressure due to surcharge (Pa_surcharge)
    Pa_surcharge = surcharge_load * height * Ka

    # Total active earth pressure (Pa)
    Pa = Pa_soil + Pa_surcharge

    return Pa


def coulomb_active_pressure(unit_weight, height, friction_angle, wall_friction_angle, backfill_inclination,
                            wall_inclination):
    """
    Calculate active earth pressure against an abutment using the Coulomb method.

    Parameters:
    unit_weight (float): Unit weight of the soil (kN/m³ or lb/ft³)
    height (float): Height of the abutment (meters or feet)
    friction_angle (float): Internal friction angle of the soil (degrees)
    wall_friction_angle (float): Angle of wall friction (delta) (degrees)
    backfill_inclination (float): Angle of inclination of the backfill surface (theta) (degrees)
    wall_inclination (float): Inclination of the back side of the wall (beta) (degrees)

    Returns:
    float: Active earth pressure (kN/m² or lb/ft²)
    """

    # Convert angles to radians
    phi_rad = math.radians(friction_angle)
    delta_rad = math.radians(wall_friction_angle)
    theta_rad = math.radians(backfill_inclination)
    beta_rad = math.radians(wall_inclination)

    # Calculate the active earth pressure coefficient (Ka')
    numerator = math.cos(phi_rad - theta_rad) * math.cos(theta_rad)
    denominator_part1 = math.cos(delta_rad + theta_rad) * math.cos(delta_rad)
    denominator_part2 = math.sin(phi_rad + delta_rad) * math.sin(phi_rad - beta_rad - delta_rad)
    denominator = denominator_part1 * (1 + math.sqrt(denominator_part2 / (math.cos(delta_rad + theta_rad) ** 2)))
    Ka_prime = numerator / denominator

    # Calculate the active earth pressure (Pa)
    Pa = 0.5 * unit_weight * height ** 2 * Ka_prime

    return Pa


def coulomb_active_pressure_with_surcharge(unit_weight, height, friction_angle, wall_friction_angle,
                                           backfill_inclination, wall_inclination, surcharge_load):
    """
    Calculate active earth pressure against an abutment using the Coulomb method with a surcharge load.

    Parameters:
    unit_weight (float): Unit weight of the soil (kN/m³ or lb/ft³)
    height (float): Height of the abutment (meters or feet)
    friction_angle (float): Internal friction angle of the soil (degrees)
    wall_friction_angle (float): Angle of wall friction (delta) (degrees)
    backfill_inclination (float): Angle of inclination of the backfill surface (theta) (degrees)
    wall_inclination (float): Inclination of the back side of the wall (beta) (degrees)
    surcharge_load (float): Surcharge load at the surface (kN/m² or lb/ft²)

    Returns:
    float: Active earth pressure (kN/m² or lb/ft²)
    """

    # Convert angles to radians
    phi_rad = math.radians(friction_angle)
    delta_rad = math.radians(wall_friction_angle)
    theta_rad = math.radians(backfill_inclination)
    beta_rad = math.radians(wall_inclination)

    # Calculate the active earth pressure coefficient (Ka')
    numerator = math.cos(phi_rad - theta_rad) * math.cos(theta_rad)
    denominator_part1 = math.cos(delta_rad + theta_rad) * math.cos(delta_rad)
    denominator_part2 = math.sin(phi_rad + delta_rad) * math.sin(phi_rad - beta_rad - delta_rad)
    denominator = denominator_part1 * (1 + math.sqrt(denominator_part2 / (math.cos(delta_rad + theta_rad) ** 2)))
    Ka_prime = numerator / denominator

    # Calculate the active earth pressure (Pa) including the surcharge load
    soil_pressure = 0.5 * unit_weight * height ** 2 * Ka_prime
    surcharge_pressure = surcharge_load * height * Ka_prime
    Pa = soil_pressure + surcharge_pressure

    return Pa
