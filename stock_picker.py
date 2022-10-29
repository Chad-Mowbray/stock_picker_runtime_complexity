from random import randint
from time import time_ns
import csv
import matplotlib.pyplot as plt
import os


def timer(func):
    def inner(iterations):
        start = time_ns()
        for _ in range(10):
            inp = [randint(1, 10000) for _ in range(iterations)]
            func(inp)
        end = time_ns()
        with open(f"{func.__name__}_results", "a") as f:
            writer = csv.writer(f)
            writer.writerow([(end - start) / 1000])

    return inner


@timer
def stock_picker_1(prices):
    left, max_profit = 0, 0
    ans = []
    for right in range(1, len(prices)):
        if prices[left] < prices[right]:

            current = prices[right] - prices[left]
            max_profit = max(max_profit, current)

            if current == max_profit:
                ans = [left, right]
        else:
            left = right

    return ans


@timer
def stock_picker_2(prices):
    max_profit = 0
    low_day = 0
    high_day = 0

    for i in range(len(prices)):
        for price in range(i + 1, len(prices)):
            if (lambda x, y: x - y)(prices[price], prices[i]) > max_profit:
                max_profit = (lambda x, y: x - y)(prices[price], prices[i])
                low_day = i
                high_day = price

    return [low_day, high_day]


def run(f, max_iterations, num=1):
    if num >= max_iterations:
        return
    else:
        f(num)
        run(f, max_iterations, num * 2)


max_iterations = 4000
run(stock_picker_1, max_iterations)
print()
run(stock_picker_2, max_iterations)


def plot_results():
    with open("stock_picker_1_results", "r") as f1, open(
        "stock_picker_2_results", "r"
    ) as f2:
        res_1 = [float(time.strip()) for time in f1.readlines()]
        res_2 = [float(time.strip()) for time in f2.readlines()]
        plt.plot([x + 1 for x in range(len(res_1))], res_1)
        plt.plot([x + 1 for x in range(len(res_2))], res_2)
        plt.show()


plot_results()
os.remove("stock_picker_1_results")
os.remove("stock_picker_2_results")
