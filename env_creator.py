import ast
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ClassInfo:
    classname: str
    doc: str
    env_prefix: str
    properties: dict[str, str]


def analyze_class_properties_with_ast(file_path, class_name: str) -> ClassInfo:
    """
    Анализирует указанный класс в файле с помощью AST
    и возвращает словарь свойств, типов и docstrings.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        source_code = f.read()

    # Парсим исходный код в AST-дерево
    tree = ast.parse(source_code)

    class_info: ClassInfo = ClassInfo(
        classname=class_name,
        doc="N/A",
        env_prefix="",
        properties={}
    )

    # Используем NodeVisitor для обхода дерева и поиска нужного класса
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            # Нашли нужный класс. Теперь ищем аннотации и docstrings атрибутов
            
            # Словарь для временного хранения docstrings
            attr_docs = {}
            
            # Просматриваем тело класса на наличие выражений с docstrings
            for i, body_node in enumerate(node.body):
                # получаем env_prefix из свойства model_config
                if isinstance(body_node, ast.Assign):
                    if body_node.targets[0].id == 'model_config':
                        env_prefix = [keyword.value.value for keyword in body_node.value.keywords if keyword.arg == 'env_prefix'][0]
                        class_info.env_prefix = env_prefix

                if isinstance(body_node, ast.Expr) and isinstance(body_node.value, ast.Constant):
                    # Если это просто строка (docstring)
                    doc_string_value: str = body_node.value.value.strip()

                    # doctstring самого класса
                    if i == 0:
                        class_info.doc = doc_string_value

                    # Ищем предыдущий узел, который был аннотацией
                    if i > 0 and isinstance(node.body[i-1], ast.AnnAssign):
                        prev_assign_node = node.body[i-1]
                        attr_name = prev_assign_node.target.id
                        attr_docs[attr_name] = doc_string_value

            # Теперь извлекаем сами аннотации (имя и тип)
            for body_node in node.body:
                if isinstance(body_node, ast.AnnAssign):
                    # target.id - это имя свойства (e.g., 'user', 'port')
                    prop_name = body_node.target.id
                    prop_value = body_node.value.value if isinstance(body_node.value, ast.Constant) else None

                    # annotation - это выражение типа (e.g., ast.Subscript для str | None)
                    # Преобразовать это обратно в строку типа сложно, но можно извлечь
                    prop_type_node = body_node.annotation
                    # Это упрощенный способ получить строковое представление типа из AST-узла
                    prop_type_str = ast.get_source_segment(source_code, prop_type_node)
                    
                    class_info.properties[prop_name] = {
                        'type_str': prop_type_str,
                        'docstring': attr_docs.get(prop_name, "N/A"),
                        'value': prop_value
                    }

    return class_info


def get_path_and_classname() -> dict[str, str]:
    # ищем папку settings
    search_result = Path.cwd().rglob('settings')
    found_directories = [path for path in search_result if path.is_dir()]
    settings_dir: Path | None = found_directories[0] if len(found_directories) > 0 else None

    if settings_dir:
        # ищем файл __init__.py внутри папки settings
        if init_file := list(settings_dir.rglob('__init__.py')):
            # получаем содержание файла
            with open(str(init_file[0]), 'r', encoding='utf-8') as f:
                source_code = f.read()

            # парсим исходный код файла
            tree = ast.parse(source_code)
            data: dict[str, str] = {}

            # обрабатываем каждый импорт
            for node in ast.walk(tree):
                if isinstance(node, ast.ImportFrom):
                    if node.module:
                        data[node.module] = node.names[0].name

            return data
    return {}


def main():
    data = get_path_and_classname()

    env_lines: list[str] = []

    for key, value in data.items():
        # заменяем точки на слеш и добавляем расширение в конец пути
        file_path = key.replace(".", "/") + ".py"
        # анализируем файл 
        info = analyze_class_properties_with_ast(file_path, value)

        header = f"# ---+ {info.classname} +---"
        doc = f"# {info.doc}"
        header_end = f"# {"-" * (len(header) - 2)}"

        env_lines.append(f"{header}\n")
        env_lines.append(f"{doc}" + "\n")
        env_lines.append(f"{header_end}\n")

        for name, details in info.properties.items():
            fake_value = None
            actual_value = details['value']
            param_type = details['type_str']
            indent = "\t"
            
            if param_type == 'bool' or param_type == 'bool | None':
                fake_value = '"false"'
            if param_type == 'int' or param_type == 'int | None':
                fake_value = "0"
            if param_type == 'str' or param_type == 'str | None':
                fake_value = '"<какая-то строка>"'
            if param_type == 'Path' or param_type == 'Path | None':
                fake_value = '"<путь>"'

            if fake_value:
                comment_line = f"{indent}# {details['docstring']}."
                if actual_value:
                    comment_line += f" По умолчанию: '{actual_value}'"
                comment_line += f"\n{indent}# [{param_type}]"

                param_name = f"{info.env_prefix.upper()}{name.upper()}"

                env_lines.append(comment_line + "\n")
                env_lines.append(f"{indent}{param_name} = {fake_value}" + "\n")

        env_lines.append("\n")
            
    with open(".env.example", 'w' ,encoding='utf-8') as f:
        f.writelines(env_lines)

    print("✅ файл .env.example создан")

if __name__ == '__main__':
    main()