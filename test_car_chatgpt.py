import unittest
from unittest.mock import patch
from io import StringIO
from Car import Car

class CarTestCase(unittest.TestCase):
    def setUp(self):
        self.car = Car()

    def tearDown(self):
        self.car = None

    def test_initial_state(self):
        self.assertEqual(self.car.speed, 0)
        self.assertEqual(self.car.odometer, 0)
        self.assertEqual(self.car.time, 0)

    def test_accelerate(self):
        self.car.accelerate()
        self.assertEqual(self.car.speed, 5)

    def test_brake_when_speed_less_than_5(self):
        self.car.brake()
        self.assertEqual(self.car.speed, 0)

    def test_brake_when_speed_greater_than_5(self):
        self.car.speed = 10
        self.car.brake()
        self.assertEqual(self.car.speed, 5)

    def test_step_increments_odometer_and_time(self):
        self.car.speed = 10
        self.car.step()
        self.assertEqual(self.car.odometer, 10)
        self.assertEqual(self.car.time, 1)

    def test_average_speed(self):
        self.car.speed = 30
        self.car.time = 3
        self.assertEqual(self.car.average_speed(), 10)

    @patch('builtins.input', side_effect=['A', 'B', 'O', 'S', 'X'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_interaction(self, mock_stdout, mock_input):
        expected_output = "I'm a car!\n" \
                          "I'm going 5 kph!\n" \
                          "I'm going 0 kph!\n" \
                          "The car has driven 0 kilometers\n" \
                          "The car's average speed was None kph\n" \
                          "I don't know how to do that\n"
        my_car = Car()
        my_car.say_state()
        while True:
            action = input("What should I do? [A]ccelerate, [B]rake, "
                           "show [O]dometer, or show average [S]peed?").upper()
            if action not in "ABOS" or len(action) != 1:
                print("I don't know how to do that")
                continue
            if action == 'A':
                my_car.accelerate()
            elif action == 'B':
                my_car.brake()
            elif action == 'O':
                print("The car has driven {} kilometers".format(my_car.odometer))
            elif action == 'S':
                print("The car's average speed was {} kph".format(my_car.average_speed()))
            my_car.step()
            my_car.say_state()

        self.assertEqual(mock_stdout.getvalue(), expected_output)

if __name__ == '__main__':
    unittest.main()
