import os
import httpx
from pathlib import Path

from IPython import start_ipython

from datamodel_code_generator import InputFileType, generate
from datamodel_code_generator import DataModelType


def generate_response_models():
    response = httpx.get("http://localhost:2400/openapi.json")
    response.raise_for_status()
    output_directory = Path(__file__).parent
    output = Path(output_directory / "schemas.py")
    output.unlink(missing_ok=True)
    generate(
        response.text,
        input_file_type=InputFileType.OpenAPI,
        input_filename="openapi.json",
        output=output,
        # set up the output model types
        output_model_type=DataModelType.PydanticV2BaseModel,
    )

    model = output.read_text()
    print(model)


def run_ipython():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    startup_script = os.path.join(script_dir, 'ipython_init.py')
    
    ipython_args = [
        '--InteractiveShellApp.exec_files={}'.format(startup_script)
    ]
    
    start_ipython(argv=ipython_args)