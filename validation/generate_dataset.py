import os
import json

from client.claude_client import add_user_message, add_assistant_message, chat

DATA_DIR = "validation/data"
OBJECTS_AMOUNT = 3

GENERATE_DATASET_SYSTEM_PROMPT = """
    Write all Spanish text in the output ("task", "task-name", and every string inside "lsp-script" -
    prompts, messages, comments) WITHOUT accented vowels (a, e, i, o, u only, no á/é/í/ó/ú) and WITHOUT
    "ñ" (use "n" instead, e.g. "diseno" not "diseño"). "task-name" must also be a valid AutoLISP symbol
    (letters, digits, "_" or "-" only) matching the function name defined in "lsp-script" (e.g.
    "crear_capa" for "(defun c:crear_capa ...)").
"""

GENERATE_DATASET_PROMPT = f"""
    Generate a evaluation dataset for a prompt evaluation.
    The dataset will be used to evaluate prompts that generates AutoLISP tasks with scripts to execute Architectural commands on Autocad software for Architects and Civil Engineers.
    Generate an array of each representing task that follows good and common Architect requirements to execute in their daily workday.

    Write each "task" the way a real architect would phrase their own request to an assistant - first
    person, informal, describing the business problem before the technical ask. The topic of each task is
    open (do not limit yourself to the topic of the examples below) - match only their tone, voice, and
    level of complexity (write new ones with the same spirit, do not copy them):

    1. "Quiero un comando que revise los modulos de fachada en el plano, los agrupe por material y tamano
       similar (con tolerancia definida), les asigne un tag consecutivo, y genere una tabla resumen en el
       plano con el conteo por tag, lista para mandar a proveedores como base de cotizacion."
    2. "Necesito un comando que detecte modulos casi-identicos por dimensiones dentro de un rango de
       tolerancia, los normalice bajo un mismo tag, y separe los modulos por fase de entrega (segun capa o
       atributo), generando un documento con una tabla por fase que incluya tag, material, dimensiones y
       cantidad."
    3. "Quiero un comando que clasifique los modulos por material (vidrio, madera, acero), les asigne
       color y tag por categoria, y genere tres documentos separados -uno por material- con las
       especificaciones tecnicas de cada grupo, listos para enviar a cada proveedor por separado."
    4. "Necesito un comando que taggee todos los modulos por categoria, coloque una leyenda con el conteo
       en una esquina del plano, y al mismo tiempo genere un documento externo tipo spec sheet con esa
       misma informacion detallada por modulo, para no transcribir manualmente del plano al documento."
    5. "Necesito convertir el conteo de modulos de acero de mi fachada en un documento formal de
       licitacion. Agrupa por perfil y acabado, lista dimensiones y cantidad por grupo, y agrega una tabla
       resumen al inicio con el total, para enviarlo directo a los fabricantes."
    6. "Tengo una fachada con modulos de vidrio, madera y acero, cada uno con proveedor distinto. Necesito
       un documento que agrupe por material, muestre dimensiones, acabado y cantidad de cada grupo, y una
       tabla resumen general con el porcentaje que representa cada material, para repartir entre los tres
       proveedores sin mezclar informacion."
    7. "Ya envie un pedido de modulos de vidrio a mi proveedor, pero el arquitecto cambio el espesor.
       Necesito un documento de solicitud de cambio que referencie los tags de los modulos originales,
       muestre la especificacion anterior versus la nueva, y marque cuales modulos quedaron afectados,
       para que el proveedor no re-cotice todo el pedido por error."
    8. "Tengo modulos de fachada dibujados como bloques distintos, pero muchos son geometricamente iguales
       y solo cambian en un atributo como el acabado o el grosor. Quiero un comando que identifique
       bloques con la misma geometria base, los agrupe bajo un mismo tag principal, y les agregue un
       subtag con la variacion especifica."
    9. "Necesito un comando que revise todos los modulos del plano, los clasifique por material, les
       asigne un color distinto por categoria, y les coloque un tag de texto con el nombre de la categoria
       y el numero consecutivo dentro de ese grupo (ej. 'ACERO-01')."
    10. "Quiero un comando que compare los modulos actuales del plano contra un tag anterior guardado en
        un atributo extendido (xdata), y resalte en un color distinto (por ejemplo rojo) unicamente los
        modulos cuyo tamano o material cambio desde la ultima vez que se taggearon, sin tocar los que
        siguen igual."

    Example output:
    ```json
    [
        {{
            "task": "Description of task, phrased as the architect's own first-person request",
            "task-name": "name of the task and defined function name",
            "format": "lsp",
            "lsp-script": ""
        }},
        ...additional
    ]
    ```

    lets generate {OBJECTS_AMOUNT} objects
"""


GENERATE_DATASET_MAX_TOKENS = 8000


def generate_dataset():
    messages = []
    add_user_message(messages, GENERATE_DATASET_PROMPT)
    answer = chat(
        messages,
        system=GENERATE_DATASET_SYSTEM_PROMPT,
        max_tokens=GENERATE_DATASET_MAX_TOKENS,
    )
    print("Answer:", answer)

    add_assistant_message(messages, "```json")
    json_text = chat(
        messages,
        system=GENERATE_DATASET_SYSTEM_PROMPT,
        stop_sequences=["```"],
        max_tokens=GENERATE_DATASET_MAX_TOKENS,
    )

    print("--- Generator")
    print(json_text)
    print("---")

    return json.loads(json_text)


def write_json_file(data, filename="dataset.json"):
    os.makedirs(DATA_DIR, exist_ok=True)
    path = os.path.join(DATA_DIR, filename)
    with open(path, "w") as file:
        json.dump(data, file, indent=2)


dataset = generate_dataset()
print("--- Dataset")
print(dataset)
write_json_file(dataset)
print("---")
