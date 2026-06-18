import os
import time
import subprocess
import webbrowser

def check_docker():
    try:
        result = subprocess.run(["docker", "info"], capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ Docker no parece estar en ejecución. Intenta iniciar Docker Desktop.")
            return False
        return True
    except FileNotFoundError:
        print("❌ El comando 'docker' no fue encontrado. Instala Docker o agrégalo al PATH.")
        return False

def start_docker_compose(dir_path):
    print("⏳ Levantando los contenedores de Docker (docker-compose up -d)...")
    try:
        subprocess.run(["docker", "compose", "up", "-d"], cwd=dir_path, check=True)
        print("✅ Servicios levantados exitosamente.")
    except Exception as e:
        print(f"❌ Error al levantar Docker Compose: {e}")
        return False
    return True

def wait_for_services():
    print("⏳ Esperando a que el Dashboard de Streamlit esté listo (aprox. 10s)...")
    # Streamlit y Postgres tardan unos segundos en arrancar completamente
    time.sleep(10)
    print("✅ Servicios listos.")

def main():
    print("========================================")
    print("   Lanzador del Sistema Shelly Energy   ")
    print("========================================")
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))

    if not check_docker():
        input("Presiona Enter para salir...")
        return

    if not start_docker_compose(project_root):
        input("Presiona Enter para salir...")
        return
    
    wait_for_services()

    dashboard_url = "http://localhost:8501"
    print(f"🌍 Abriendo el Dashboard energético en el navegador: {dashboard_url}")
    webbrowser.open(dashboard_url)
    
    print("\nTodo listo. Puedes cerrar esta ventana. Docker seguirá corriendo en segundo plano.")
    time.sleep(5)

if __name__ == "__main__":
    main()
