import importlib.util
import os
import tempfile


def execute_python_code(code: str, execution_context: dict):
    # We need to write the code to a file to allow debugging.
    tmp_dir = os.path.join(tempfile.gettempdir(), 'browserstream')
    os.makedirs(tmp_dir, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=tmp_dir, mode='w', suffix='.py') as temp_file:
        temp_file.write(code)
        temp_file.flush()

        spec = importlib.util.spec_from_file_location("temp_module", temp_file.name)
        module = importlib.util.module_from_spec(spec)

        for k, v in execution_context.items():
            setattr(module, k, v)
        spec.loader.exec_module(module)
