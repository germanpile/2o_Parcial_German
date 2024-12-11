import heapq
import json
from datetime import datetime

class TaskManager:
    def __init__(self, filename="tasks.json"):
        self.tasks = []
        self.completed_tasks = set()
        self.filename = filename
        self.load_tasks()

    def load_tasks(self):
        try:
            with open(self.filename, "r") as f:
                data = json.load(f)  # Intenta cargar el JSON como lista de tareas
            if isinstance(data, list):  # Verifica que sea una lista
                for task in data:
                    if isinstance(task, dict):  # Verifica que cada tarea sea un diccionario
                        heapq.heappush(self.tasks, (task["priority"], task["due_date"], task))
            else:
                print("El archivo JSON no contiene una lista válida de tareas.")
        except (FileNotFoundError, json.JSONDecodeError):
        # Si el archivo no existe o está corrupto, comienza con una lista vacía
            print("Archivo de tareas no encontrado o corrupto. Se creará uno nuevo al guardar tareas.")


    def save_tasks(self):
        """Guarda las tareas en el archivo JSON."""
        with open(self.filename, "w") as f:
            tasks_to_save = [task[2] for task in self.tasks]
            json.dump(tasks_to_save, f, indent=4)

    def add_task(self, name, priority, due_date, dependencies):
        """Añade una nueva tarea al sistema."""
        if not name.strip():
            print("El nombre de la tarea no puede estar vacío.")
            return

        if not isinstance(priority, int):
            print("La prioridad debe ser un número entero.")
            return

        for dependency in dependencies:
            if dependency not in [task[2]["name"] for task in self.tasks] and dependency not in self.completed_tasks:
                print(f"La dependencia '{dependency}' no existe.")
                return

        task = {
            "name": name,
            "priority": priority,
            "due_date": due_date,
            "dependencies": dependencies
        }
        heapq.heappush(self.tasks, (priority, due_date, task))
        self.save_tasks()
        print(f"Tarea '{name}' añadida correctamente.")

    def interactive_add_task(self):
        """Interfaz interactiva para añadir una tarea."""
        name = input("Introduce el nombre de la tarea: ").strip()
        try:
            priority = int(input("Introduce la prioridad de la tarea (entero): ").strip())
        except ValueError:
            print("La prioridad debe ser un número entero.")
            return

        due_date = input("Introduce la fecha de vencimiento (YYYY-MM-DD): ").strip()
        try:
            datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            print("La fecha debe tener el formato YYYY-MM-DD.")
            return

        dependencies = input("Introduce las dependencias separadas por comas (o deja vacío si no hay): ").strip().split(",")
        dependencies = [d.strip() for d in dependencies if d.strip()]

        self.add_task(name, priority, due_date, dependencies)

    def show_pending_tasks(self):
        """Muestra todas las tareas pendientes ordenadas por prioridad."""
        if not self.tasks:
            print("No hay tareas pendientes.")
            return

        print("Tareas pendientes:")
        for _, _, task in sorted(self.tasks):
            print(f"Tarea: {task['name']}, Prioridad: {task['priority']}, Fecha: {task['due_date']}, Dependencias: {task['dependencies']}")

    def complete_task(self, name):
        """Marca una tarea como completada y la elimina del sistema."""
        for i, (_, _, task) in enumerate(self.tasks):
            if task["name"] == name:
                if any(dep not in self.completed_tasks for dep in task["dependencies"]):
                    print(f"No se puede completar la tarea '{name}' porque tiene dependencias no completadas.")
                    return
                self.completed_tasks.add(name)
                del self.tasks[i]
                heapq.heapify(self.tasks)
                self.save_tasks()
                print(f"Tarea '{name}' completada.")
                return

        print(f"Tarea '{name}' no encontrada.")

    def get_next_task(self):
        """Obtiene la siguiente tarea de mayor prioridad que sea ejecutable."""
        for _, _, task in sorted(self.tasks):
            if all(dep in self.completed_tasks for dep in task["dependencies"]):
                print(f"Siguiente tarea ejecutable: {task['name']}")
                return task

        print("No hay tareas ejecutables en este momento.")
        return None

if __name__ == "__main__":
    manager = TaskManager()

    while True:
        print("\n--- Menú de Tareas ---")
        print("1. Añadir tarea")
        print("2. Mostrar tareas pendientes")
        print("3. Completar tarea")
        print("4. Obtener siguiente tarea ejecutable")
        print("5. Salir")

        option = input("Selecciona una opción: ").strip()

        if option == "1":
            manager.interactive_add_task()
        elif option == "2":
            manager.show_pending_tasks()
        elif option == "3":
            name = input("Introduce el nombre de la tarea a completar: ").strip()
            manager.complete_task(name)
        elif option == "4":
            manager.get_next_task()
        elif option == "5":
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida. Por favor, intenta de nuevo.")
