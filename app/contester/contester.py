import subprocess
import sys

tests = {
    '1 2': '3 4',
    '1 5': '3 7',
    '2 5': '4 7',
    '5 6': '7 8',
}

for index, (input_value, output_value) in enumerate(tests.items()):
    try:
        result = subprocess.run([sys.executable, "program.py"], input=input_value, capture_output=True, text=True)
        answer = result.stdout.strip()
        error = result.stderr

        print(answer, output_value)

        assert answer == output_value

        print(f'Passed test number {index}')

    except AssertionError:
        print(f'Failed test number {index}, incorrect answer')
