import sys

def main():
    try:
        with open("script.py", "r") as f:
            code = f.read()
        exec(code, {})
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()