def greeting():
    print("Hey, hello Text editor tool.")


def calculate_pi(digits=5):
    """
    Calculate pi to the specified number of digits using the Machin formula.
    Machin's formula: pi/4 = 4*arctan(1/5) - arctan(1/239)
    
    Args:
        digits: Number of decimal digits to calculate (default: 5)
    
    Returns:
        float: Pi calculated to the specified precision
    """
    from decimal import Decimal, getcontext
    
    # Set precision high enough to get accurate results
    getcontext().prec = digits + 10
    
    def arctan(x, num_terms=100):
        """Calculate arctan using Taylor series expansion"""
        x = Decimal(x)
        power = x
        result = power
        for n in range(1, num_terms):
            power *= -x * x
            result += power / (2 * n + 1)
        return result
    
    # Machin's formula: pi/4 = 4*arctan(1/5) - arctan(1/239)
    pi = 4 * (4 * arctan(Decimal(1)/Decimal(5)) - arctan(Decimal(1)/Decimal(239)))
    
    return float(pi)