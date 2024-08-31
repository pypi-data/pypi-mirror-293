import time

class MangoTest:
    def __init__(self):
        self.test_count = 0
        self.passed_count = 0
        self.failed_count = 0

    def mangostart(self):
        self.test_count += 1
        print(f"Running test {self.test_count}...", end=" ")

    def mangoend(self, code):
        try:
            # Define a function to encapsulate the code execution
            def test_code():
                exec(code, {})

            # Run the encapsulated code
            test_code()
            self.passed_count += 1
            print("\033[92mpassed ✔\033[0m")  # Green checkmark and passed text
        except AssertionError as e:
            self.failed_count += 1
            print(f"\033[91mFAILED with error: {e}\033[0m")
        except BaseException as e:
            self.failed_count += 1
            print(f"\033[91mFAILED with error: {e}\033[0m")  # Red error text
        time.sleep(1.25)  # Introduce a delay between tests

    def summary(self):
        print("\nSummary:")
        print(f"Total tests: {self.test_count}")
        print(f"\033[92mPassed: {self.passed_count}\033[0m")  # Green passed count
        print(f"\033[91mFailed: {self.failed_count}\033[0m")  # Red failed count

# Instantiate a global MangoTest object
mango_test = MangoTest()

def mangostart():
    mango_test.mangostart()

def mangoend(code):
    mango_test.mangoend(code)

def summary():
    mango_test.summary()