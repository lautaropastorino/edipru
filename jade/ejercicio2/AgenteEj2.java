package ejercicio2;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;

import jade.core.*;

public class AgenteEj2 extends Agent {

    private String archivo = new String();

    public void moverse(String nombre) {
        try {
            ContainerID destino = new ContainerID(nombre, null);
            System.out.println("Migrando el agente a " + destino.getID());
            doMove(destino);
        } catch (Exception e) {
            System.out.println("\n\n\nNo fue posible migrar el agente\n\n\n");
            e.printStackTrace();
        }
    }

    public void setup() {
        Location origen = here();
        System.out.println(String.format("%n"));
        System.out.println(getLocalName() + " en " + origen.getID());
        String[] args = ((String) getArguments()[0]).split(" ");
        String nombreContenedor = args[0];
        this.archivo = args[1];
        moverse(nombreContenedor);
    }
        
    protected void afterMove() {
        Location origen = here();
        System.out.println(String.format("%n"));
        System.out.println("Contenedor actual: " + origen.getID()); 
        int suma = 0;
        File file = new File(archivo);
        try {
            Scanner reader = new Scanner(file);
            while (reader.hasNextLine()) {
                suma += Integer.parseInt(reader.nextLine());            
            }
            reader.close();
            System.out.println("La suma es: " + suma);
        } catch (FileNotFoundException e) {
            System.out.println("No se encontro el archivo: " + e);
        } catch (NumberFormatException e) {
            System.out.println("No se pudo transformar el string a int: " + e);
        }
    }

}
