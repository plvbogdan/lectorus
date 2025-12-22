import json
import nbformat
from nbformat import from_dict
from fastapi import status, HTTPException

def notebook_parser(data: json) -> list:
    nb = from_dict(data)
    body_lection = []
    for cell in nb.cells:
        if cell.cell_type == "markdown":
            if cell.source[0].startswith("#"):
                body_lection.append({
                    "title": cell.source,
                    "content": []
                })
            else:
                if "title" not in body_lection[-1]:
                    raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail='Неверный формат ноутбука')

                body_lection[-1]["content"].append({
                    "type": cell.cell_type,
                    "source": cell.source
                })

        if cell.cell_type == "code":
            if "title" not in body_lection[-1]:
                    raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail='Неверный формат ноутбука')

            body_lection[-1]["content"].append({
                "type": cell.cell_type,
                "source": cell.source
            })
            
            if cell["outputs"]:
                for output in cell["outputs"]:
                    if output.output_type == "stream":
                        body_lection[-1]["content"].append({
                        "type": "output",
                        "source": output["text"]
                    })
                    else:
                        body_lection[-1]["content"].append({
                        "type": "output",
                        "source": output["data"]
                    })
                
                
    return body_lection
