import unittest
from pynance.myfunctions import (
    present_value, future_value, npv, npv_derivative, internal_rate_of_return,
    bond_price, yield_to_maturity, dividend_discount_model, black_scholes_call,
    sharpe_ratio, value_at_risk
)


class TestFinancialFunctions(unittest.TestCase):

    # Time Value of Money (TVM) Functions Tests
    def test_present_value(self):
        self.assertAlmostEqual(present_value(0.05, 1000, 10), 613.91, places=2)
        self.assertRaises(ValueError, present_value, -0.05, 1000, 10)
        self.assertRaises(ValueError, present_value, 0.05, 1000, -10)

    def test_future_value(self):
        self.assertAlmostEqual(future_value(0.05, 1000, 10), 1628.89, places=2)
        self.assertRaises(ValueError, future_value, -0.05, 1000, 10)
        self.assertRaises(ValueError, future_value, 0.05, 1000, -10)

    def test_npv(self):
        cash_flows = [-1000, 300, 400, 500, 600]
        self.assertAlmostEqual(npv(0.1, cash_flows), 388.77, places=2)
        self.assertRaises(ValueError, npv, -1.1, cash_flows)
        self.assertRaises(TypeError, npv, 0.1, "invalid input")

    def test_npv_derivative(self):
        cash_flows = [-1000, 300, 400, 500, 600]
        self.assertAlmostEqual(npv_derivative(0.1, cash_flows), -3363.72, places=2)
        self.assertRaises(ValueError, npv_derivative, -1.1, cash_flows)
        self.assertRaises(TypeError, npv_derivative, 0.1, "invalid input")

    def test_internal_rate_of_return(self):
        cash_flows = [-1000, 300, 400, 500, 600]
        self.assertAlmostEqual(internal_rate_of_return(cash_flows), 0.2489, places=4)
        self.assertRaises(TypeError, internal_rate_of_return, "invalid input")
        self.assertRaises(ValueError, internal_rate_of_return, cash_flows, initial_guess=-2)
        self.assertRaises(ValueError, internal_rate_of_return, cash_flows, tolerance=-0.01)
        self.assertRaises(ValueError, internal_rate_of_return, cash_flows, max_iterations=0)

    # Bond Pricing and Yield Calculations Tests
    def test_bond_price(self):
        self.assertAlmostEqual(bond_price(1000, 0.05, 10, 0.03), 1170.60, places=2)
        self.assertRaises(ValueError, bond_price, -1000, 0.05, 10, 0.03)
        self.assertRaises(ValueError, bond_price, 1000, -0.05, 10, 0.03)
        self.assertRaises(ValueError, bond_price, 1000, 0.05, -10, 0.03)
        self.assertRaises(ValueError, bond_price, 1000, 0.05, 10, -0.03)

    def test_yield_to_maturity(self):
        self.assertAlmostEqual(yield_to_maturity(1000, 0.05, 10, 900), 0.0638, places=4)
        self.assertRaises(ValueError, yield_to_maturity, -1000, 0.05, 10, 900)
        self.assertRaises(ValueError, yield_to_maturity, 1000, -0.05, 10, 900)
        self.assertRaises(ValueError, yield_to_maturity, 1000, 0.05, -10, 900)
        self.assertRaises(ValueError, yield_to_maturity, 1000, 0.05, 10, -900)

    # Stock Valuation Functions Tests
    def test_dividend_discount_model(self):
        self.assertAlmostEqual(dividend_discount_model(10, 0.02, 0.05), 333.33, places=2)
        self.assertRaises(ValueError, dividend_discount_model, -10, 0.02, 0.05)
        self.assertRaises(ValueError, dividend_discount_model, 10, -0.02, 0.05)
        self.assertRaises(ValueError, dividend_discount_model, 10, 0.05, 0.04)

    # Option Pricing Functions Tests
    def test_black_scholes_call(self):
        self.assertAlmostEqual(black_scholes_call(100, 100, 1, 0.05, 0.2), 10.45, places=2)
        self.assertRaises(ValueError, black_scholes_call, -100, 100, 1, 0.05, 0.2)
        self.assertRaises(ValueError, black_scholes_call, 100, -100, 1, 0.05, 0.2)
        self.assertRaises(ValueError, black_scholes_call, 100, 100, -1, 0.05, 0.2)
        self.assertRaises(ValueError, black_scholes_call, 100, 100, 1, -0.05, 0.2)
        self.assertRaises(ValueError, black_scholes_call, 100, 100, 1, 0.05, -0.2)

    # Risk and Performance Metrics Tests
    def test_sharpe_ratio(self):
        returns = [0.05, 0.1, 0.15, 0.1, 0.05]
        self.assertAlmostEqual(sharpe_ratio(returns, 0.02), 1.8708, places=4)
        self.assertRaises(TypeError, sharpe_ratio, "invalid input", 0.02)
        self.assertRaises(ValueError, sharpe_ratio, returns, -0.02)
        self.assertRaises(ValueError, sharpe_ratio, [], 0.02)

    def test_value_at_risk(self):
        returns = [-0.02, 0.05, -0.01, 0.04, 0.03]
        self.assertAlmostEqual(value_at_risk(returns, 0.95), 0.02, places=2)
        self.assertRaises(TypeError, value_at_risk, "invalid input", 0.95)
        self.assertRaises(ValueError, value_at_risk, returns, 1.5)
        self.assertRaises(ValueError, value_at_risk, [], 0.95)


if __name__ == '__main__':
    unittest.main()
