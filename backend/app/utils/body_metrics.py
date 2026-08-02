"""Reusable body metric calculations."""

from decimal import Decimal


def calculate_bmi(weight, height) -> float:
    # Convert Decimal/int/float to float
    weight = float(weight)
    height = float(height)

    if height <= 0:
        raise ValueError("Height must be greater than zero")

    bmi = weight / ((height / 100) ** 2)
    return round(bmi, 2)


def calculate_body_fat_percentage(bmi, age, gender) -> float:
    bmi = float(bmi)

    if age is None or gender is None:
        raise ValueError("Age and gender are required to estimate body fat percentage")

    age = float(age)

    gender_factor = 1 if gender.lower() == "male" else 0

    body_fat = (
        1.20 * bmi
        + 0.23 * age
        - 10.8 * gender_factor
        - 5.4
    )

    return round(body_fat, 2)
