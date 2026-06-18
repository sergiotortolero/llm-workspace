using System;
using System.Diagnostics;
using System.IO;
using System.Threading;

namespace ShellyLauncher
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("========================================");
            Console.WriteLine("   Lanzador del Sistema Shelly Energy   ");
            Console.WriteLine("========================================");

            if (!CheckDocker())
            {
                Console.WriteLine("Presiona Enter para salir...");
                Console.ReadLine();
                return;
            }

            string currentDir = AppDomain.CurrentDomain.BaseDirectory;

            if (!StartDockerCompose(currentDir))
            {
                Console.WriteLine("Presiona Enter para salir...");
                Console.ReadLine();
                return;
            }

            WaitForServices();

            string dashboardUrl = "http://localhost:8501";
            Console.WriteLine(string.Format("🌍 Abriendo el Dashboard energético en el navegador: {0}", dashboardUrl));
            Process.Start(new ProcessStartInfo(dashboardUrl) { UseShellExecute = true });

            Console.WriteLine("\nTodo listo. Puedes cerrar esta ventana. Docker seguirá corriendo en segundo plano.");
            Thread.Sleep(5000);
        }

        static bool CheckDocker()
        {
            try
            {
                Process p = new Process();
                p.StartInfo.FileName = "docker";
                p.StartInfo.Arguments = "info";
                p.StartInfo.UseShellExecute = false;
                p.StartInfo.RedirectStandardOutput = true;
                p.StartInfo.RedirectStandardError = true;
                p.StartInfo.CreateNoWindow = true;
                p.Start();
                p.WaitForExit();

                if (p.ExitCode != 0)
                {
                    Console.WriteLine("⏳ Docker no está corriendo. Intentando iniciar Docker Desktop...");
                    string dockerPath = @"C:\Program Files\Docker\Docker\Docker Desktop.exe";
                    if (File.Exists(dockerPath))
                    {
                        Process.Start(new ProcessStartInfo(dockerPath) { UseShellExecute = true });
                        Console.WriteLine("⏳ Esperando 30 segundos a que Docker inicie...");
                        Thread.Sleep(30000);
                        return true;
                    }
                    else
                    {
                        Console.WriteLine("❌ No se pudo encontrar Docker Desktop. Por favor inícialo manualmente.");
                        return false;
                    }
                }
                return true;
            }
            catch (Exception)
            {
                Console.WriteLine("❌ El comando 'docker' no fue encontrado. Instala Docker o agrégalo al PATH.");
                return false;
            }
        }

        static bool StartDockerCompose(string dirPath)
        {
            Console.WriteLine("⏳ Levantando los contenedores de Docker (docker-compose up -d)...");
            try
            {
                Process p = new Process();
                p.StartInfo.FileName = "docker";
                p.StartInfo.Arguments = "compose up -d";
                p.StartInfo.WorkingDirectory = dirPath;
                p.StartInfo.UseShellExecute = false;
                p.Start() ;
                p.WaitForExit();

                if (p.ExitCode != 0)
                {
                    Console.WriteLine("❌ Error al levantar Docker Compose.");
                    return false;
                }
                
                Console.WriteLine("✅ Servicios levantados exitosamente.");
                return true;
            }
            catch (Exception ex)
            {
                Console.WriteLine(string.Format("❌ Error ejecutando docker-compose: {0}", ex.Message));
                return false;
            }
        }

        static void WaitForServices()
        {
            Console.WriteLine("⏳ Esperando a que el Dashboard de Streamlit esté listo (aprox. 10s)...");
            Thread.Sleep(10000);
            Console.WriteLine("✅ Servicios listos.");
        }
    }
}
