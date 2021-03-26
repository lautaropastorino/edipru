package ejercicio1;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.concurrent.TimeUnit;

import jade.core.*;

public class Agente extends Agent {
    
    private static final int inicio = 6;
    private int index = 0;
    private long start = 0;
    private long end = 0;
    private String resultado = new String();


    public void moverse() {
        // Cambiar al siguiente contenedor 
        try {
            index++;
            ContainerID destino = new ContainerID("Container-" + index, null);
            System.out.println("Migrando el agente a " + destino.getID());
            doMove(destino);
        } catch (Exception e) {
            System.out.println("\n\n\nNo fue posible migrar el agente\n\n\n");
            e.printStackTrace();
        }
    }

    public String[] getMemoria() {
        // Obtener la memoria del contenedor donde estoy
        String[] res = null;
        try{
            // Creo un proceso Unix que ejecuta el comando
            Process proc = java.lang.Runtime.getRuntime().exec("free -h");
            BufferedReader stdInput = new BufferedReader(new InputStreamReader(proc.getInputStream()));
            int cont = 0;
            String s = null;
            while ((s = stdInput.readLine()) != null) {
                cont++;
                if (cont == 2) { // Solo queremos la segunda linea 
                   res = s.split(" ");
                   break;
                }
            }
        } catch(IOException e) {
            System.out.println("Error ejecutando el comando " + e);
        }
        String[] r = {res[19], res[11]};
        return r;
    }

    public String getCpu() {
        // Obtener los mhz del/los cpu/s donde estoy
        String[] res = null;
        try {
            Process proc = java.lang.Runtime.getRuntime().exec("cat /proc/cpuinfo");
            BufferedReader stdInput = new BufferedReader(new InputStreamReader(proc.getInputStream()));
            int cont = 0;
            String s = null;
            while ((s = stdInput.readLine()) != null) {
                cont++;
                if (cont == 8) { // solo queremos la linea de mhz
                    res = s.split(" "); // dividimos el texto en los espacios
                    break;
                }
            }
        } catch(IOException e) {
            System.out.println("Error ejecutando el comando " + e);
        }
        return res[2]; // en el indice 2 esta el numero
    }

    public void setup() {
        Location origen = here();
        System.out.println(String.format("%n"));
        System.out.println(getLocalName() + " en " + origen.getID());
        System.out.println(String.format("Iniciando recorrido%n"));
        start = System.currentTimeMillis();
        moverse();   //Inicio el recorrido
    }
        
    // Ejecutado al llegar a un contenedor como resultado de una migracion
    protected void afterMove()
    {
        Location origen = here();
        if (index == inicio) { // Si di toda la vuelta
            end = System.currentTimeMillis();
            System.out.println(String.format("%n"));
            System.out.println("Tiempo en dar toda la vuelta: " + (end-start) + "ms");
            System.out.println(String.format("%n"));
            System.out.println("Resultados:");
            System.out.println(String.format("%n"));
            System.out.println(resultado); // Imprimo los datos obtenidos
            try {
                TimeUnit.SECONDS.sleep(10); 
            } catch(InterruptedException e) {
                System.out.println("Thread interrumpida" + e);
            }
            // Vuelvo a iniciar el recorrido
            index = 0;
            resultado = new String();
            start = System.currentTimeMillis();
            moverse();
        } else { // No di toda la vuelta
            // Obtengo los datos de la computadora
            String[] mem = getMemoria(); 
            String cpu = getCpu();
            // Los agrego al string resultado
            this.resultado += String.format("Contenedor: %s%nMemoria: %sgb libre de %sgb totales%nCpu: %smhz%n%n", origen.getID(), mem[0], mem[1], cpu);
            moverse();
        }   
    }


}
