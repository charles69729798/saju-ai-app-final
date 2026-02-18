try:
    from notebooklm_tools.core.client import NotebookLMClient
    print("Successfully imported NotebookLMClient")
    client = NotebookLMClient()
    print("Successfully instantiated NotebookLMClient")
except Exception as e:
    print(f"Failed to import or instantiate: {e}")
