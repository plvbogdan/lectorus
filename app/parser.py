import json
import nbformat
from nbformat import from_dict
from fastapi import status, HTTPException

def notebook_parser(data: json) -> list:
    nb = from_dict(data)
    body_lecture = []
    for cell in nb.cells:
        if cell.cell_type == "markdown":
            if cell.source[0].startswith("#"):
                body_lecture.append({
                    "title": cell.source,
                    "content": []
                })
            else:
                if "title" not in body_lecture[-1]:
                    raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail='Неверный формат ноутбука')

                body_lecture[-1]["content"].append({
                    "type": cell.cell_type,
                    "source": cell.source
                })

        if cell.cell_type == "code":
            if "title" not in body_lecture[-1] or not body_lecture:
                    raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail='Неверный формат ноутбука')

            body_lecture[-1]["content"].append({
                "type": cell.cell_type,
                "source": cell.source
            })
            
            if cell["outputs"]:
                for output in cell["outputs"]:
                    if output.output_type == "stream":
                        body_lecture[-1]["content"].append({
                        "type": "output",
                        "source": output["text"]
                    })
                    else:
                        body_lecture[-1]["content"].append({
                        "type": "output",
                        "source": output["data"]
                    })
                
                
    return body_lecture
