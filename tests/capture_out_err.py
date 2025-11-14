# Enable detailed logging for failed tests
def test_complex_workflow():
    import logging
    logging.basicConfig(level=logging.DEBUG)
    
    # Your test code here
    
# Use pytest debugging
# Run with: pytest -vv --pdb --pdbcls=IPython.terminal.debugger:Pdb

# Capture stdout/stderr
def test_with_output(capsys):
    agent.run("test")
    captured = capsys.readouterr()
    print(f"Stdout: {captured.out}")
    print(f"Stderr: {captured.err}")