# readme_gen/generator.py

def generate_readme(project_name, description, installation_instructions, usage_instructions, license_info):
    content = f"""
    # {project_name}

    ## Description
    {description}

    ## Installation
    ```
    {installation_instructions}
    ```

    ## Usage
    ```
    {usage_instructions}
    ```

    ## License
    {license_info}
    """
    
    with open("README.md", "w") as file:
        file.write(content.strip())
    print(f"README.md generated successfully for {project_name}!")
