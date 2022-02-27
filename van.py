import pyvan


OPTIONS = {
    "main_file_name": "main.py",
    "show_console": False,
    "use_pipreqs": True,
    "use_existing_requirements": True,
}


pyvan.build(**OPTIONS)
