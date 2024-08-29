import numpy as np
from scipy.optimize import newton
from math import log, sqrt, exp
from scipy.stats import norm
def npv(rate, cash_flows):
    """
    Calculates the Net Present Value of a series of cash flows
    :param rate: The discount rate as a decimal
    :param cash_flows: A list/numpy array of cash flows.
    :return: Net present value of the cash flows.
    """
    if not isinstance(cash_flows, (list, np.ndarray)):
        raise TypeError("Cash flows must be a list or numpy array.")
    if rate < -1:
        raise ValueError("Rate must be greater than or equal to -1.")
    try:
        return sum(cf / (1 + rate) ** t for t, cf in enumerate(cash_flows))
    except ZeroDivisionError:
        raise ValueError("Rate cannot be -1.")


def npv_derivative(rate, cash_flows):
    """
    Calculate the derivative of the Net Present Value (NPV) with respect to the rate.

    Parameters:
    - rate: The discount rate (as a decimal).
    - cash_flows: A list or numpy array of cash flows.

    Returns:
    - Derivative of NPV with respect to the rate.
    """
    if not isinstance(cash_flows, (list, np.ndarray)):
        raise TypeError("Cash flows must be a list or numpy array.")
    if rate < -1:
        raise ValueError("Rate must be greater than or equal to -1.")
    try:
        return sum(-t * cf / (1 + rate) ** (t + 1) for t, cf in enumerate(cash_flows))
    except ZeroDivisionError:
        raise ValueError("Rate cannot be -1.")


def internal_rate_of_return(cash_flows, initial_guess=0.1, tolerance=1e-6, max_iterations=1000):
    """
    Calculate the Internal Rate of Return (IRR) for a series of cash flows using the Newton-Raphson method.

    Parameters:
    - cash_flows: A list or numpy array of cash flows.
    - initial_guess: The initial guess for the IRR (default is 0.1 or 10%).
    - tolerance: The tolerance level for stopping the iteration (default is 1e-6).
    - max_iterations: The maximum number of iterations to perform (default is 1000).

    Returns:
    - Internal Rate of Return (IRR).
    """
    if not isinstance(cash_flows, (list, np.ndarray)):
        raise TypeError("Cash flows must be a list or numpy array.")
    if initial_guess <= -1:
        raise ValueError("Initial guess must be greater than -1.")
    if tolerance <= 0:
        raise ValueError("Tolerance must be a positive number.")
    if max_iterations <= 0:
        raise ValueError("Maximum iterations must be a positive integer.")

    rate = initial_guess
    for i in range(max_iterations):
        npv_value = npv(rate, cash_flows)
        npv_deriv = npv_derivative(rate, cash_flows)

        if npv_deriv == 0:
            raise ZeroDivisionError("Derivative is zero; unable to continue iteration.")

        new_rate = rate - npv_value / npv_deriv

        if abs(new_rate - rate) < tolerance:
            return new_rate

        rate = new_rate

    raise ValueError(f"IRR did not converge after {max_iterations} iterations.")


def present_value(rate, future_value, periods):
    """
    Calculates present value of future asset.
    :param rate: Discount rate.
    :param future_value: Future value.
    :param periods: Number of periods of compounding
    :return: Present value of asset.
    """
    if periods < 0:
        raise ValueError("Periods cannot be negative.")
    if rate < 0:
        raise ValueError("Rate cannot be negative.")
    try:
        return future_value / (1 + rate) ** periods
    except ZeroDivisionError:
        raise ValueError("Rate cannot be -1.")

def future_value(rate, present_value, periods):
    """
    Calculates future value of an asset
    :param rate: Interest rate
    :param present_value: Current value of asset.
    :param periods: Periods of compounding
    :return: Future value of asset.
    """
    if periods < 0:
        raise ValueError("Periods cannot be negative.")
    if rate < 0:
        raise ValueError("Rate cannot be negative.")
    try:
        return present_value * ((1 + rate) ** periods)
    except OverflowError:
        raise ValueError("Result is too large to handle.")


def bond_price(face_value, coupon_rate, periods, discount_rate):
    """
    Calculate the price of a bond.
    :param face_value: Face value of the bond.
    :param coupon_rate: The annual coupon rate as a decimal.
    :param periods: # of periods until maturity.
    :param discount_rate: The discount rate as a decimal.
    :return: The bond price as a float.
    """
    if face_value <= 0:
        raise ValueError("Face value must be positive.")
    if coupon_rate < 0:
        raise ValueError("Coupon rate cannot be negative.")
    if periods <= 0:
        raise ValueError("Periods must be positive.")
    if discount_rate < 0:
        raise ValueError("Discount rate cannot be negative.")

    coupon = face_value * coupon_rate
    try:
        price = sum(coupon / (1 + discount_rate) ** t for t in range(1, periods + 1))
        price += face_value / (1 + discount_rate) ** periods
        return price
    except ZeroDivisionError:
        raise ValueError("Discount rate cannot be -1.")

def yield_to_maturity(face_value, coupon_rate, periods, price):
    """
    Calculate the Yield to Maturity (YTM) of a bond.
    :param face_value: Face value of the bond.
    :param coupon_rate: Annual coupon rate as a decimal.
    :param periods: Periods until maturity.
    :param price: Current price of the bond.
    :return: The Yield to Maturity.
    """
    if face_value <= 0:
        raise ValueError("Face value must be positive.")
    if coupon_rate < 0:
        raise ValueError("Coupon rate cannot be negative.")
    if periods <= 0:
        raise ValueError("Periods must be positive.")
    if price <= 0:
        raise ValueError("Price must be positive.")

    def bond_price_diff(rate):
        return bond_price(face_value, coupon_rate, periods, rate) - price

    try:
        return newton(bond_price_diff, x0=0.05)
    except RuntimeError:
        raise ValueError("Newton-Raphson method failed to converge.")


def dividend_discount_model(dividend, growth_rate, discount_rate):
    """
    Calculate the price of a stock using the Divident Discount Model.
    :param dividend: Expected dividend next year.
    :param growth_rate: Growth rate of the dividends as a decimal.
    :param discount_rate: Required rate of return as a decimal.
    :return: The stock price.
    """
    if dividend <= 0:
        raise ValueError("Dividend must be positive.")
    if growth_rate < 0 or growth_rate >= discount_rate:
        raise ValueError("Growth rate must be non-negative and less than the discount rate.")
    if discount_rate <= 0:
        raise ValueError("Discount rate must be positive.")

    try:
        return dividend / (discount_rate - growth_rate)
    except ZeroDivisionError:
        raise ValueError("Discount rate must be greater than the growth rate.")


def black_scholes_call(S, K, T, r, sigma):
    """
    Calculate the call option price using the Black-Scholes model.
    :param S: Current stock price.
    :param K: Option stock price.
    :param T: Time to maturity.
    :param r: Risk-free interest rate as a decimal.
    :param sigma: Volatility of the underlying stock.
    :return: The call option price.
    """
    if S <= 0 or K <= 0:
        raise ValueError("Stock price and strike price must be positive.")
    if T <= 0:
        raise ValueError("Time to maturity must be positive.")
    if r < 0:
        raise ValueError("Risk-free rate cannot be negative.")
    if sigma <= 0:
        raise ValueError("Volatility must be positive.")

    d1 = (log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * sqrt(T))
    d2 = d1 - sigma * sqrt(T)
    call_price = S * norm.cdf(d1) - K * exp(-r * T) * norm.cdf(d2)
    return call_price


def sharpe_ratio(returns, risk_free_rate):
    """
    Calculate the Sharpe Ratio for a series of returns.
    :param returns: a list of ndarray of returns.
    :param risk_free_rate: The risk-free interest rate as a decimal.
    :return: The Sharpe ratio.
    """
    if not isinstance(returns, (list, np.ndarray)):
        raise TypeError("Returns must be a list or numpy array.")
    if risk_free_rate < 0:
        raise ValueError("Risk-free rate cannot be negative.")
    if len(returns) == 0:
        raise ValueError("Returns list cannot be empty.")

    mean_return = np.mean(returns)
    std_dev = np.std(returns)
    if std_dev == 0:
        raise ValueError("Standard deviation of returns is zero; Sharpe ratio is undefined.")

    return (mean_return - risk_free_rate) / std_dev


def value_at_risk(returns, confidence_level):
    """
    Calculate the Value at Risk of a series of returns.
    :param returns: A list or ndarray of returns.
    :param confidence_level: The confidence level for VaR (like .95 for 95%)
    :return: The Value at Risk.
    """
    if not isinstance(returns, (list, np.ndarray)):
        raise TypeError("Returns must be a list or numpy array.")
    if len(returns) == 0:
        raise ValueError("Returns list cannot be empty.")
    if not 0 < confidence_level < 1:
        raise ValueError("Confidence level must be between 0 and 1.")

    sorted_returns = np.sort(returns)
    index = int((1 - confidence_level) * len(sorted_returns))
    return abs(sorted_returns[index])