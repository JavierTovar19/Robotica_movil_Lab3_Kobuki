# Robotica_movil_Lab3_Kobuki
## Actividad 1 : Verificación del robot kobuki
Para esta actividad se configura el workspace y se lanzan los siguientes comandos en la carpeta del kobuki : 
```
catkin_make\
source devel/setup.bash\
roslaunch kobuki_node minimal.launch --screen\
```
En la interfaz mostrada podemos verificar el funcionamiento de los sensores y la evidencia se encuentra en el siguiente clip:\
[Clip de sensores](./.img/monitor_sensores.mp4)

## Actividad 2 : Creación del nodo propio 
### Cuadrado
 Este nodo de encuentra en [Nodo cuadrado](./local_kobuki/scripts/kobuki_control_create_sqare.py).
 
  Su funcionamiento se basa en alternar giros sobre su propio eje con desplazamientos lineales hacia adelante, monitoreando constantemente la posición y orientación del robot a través de la odometría. Las funciones realizan las siguientes acciones: 
  
  callback(data): Esta función se ejecuta cada vez que llega un mensaje de odometría del robot. Su objetivo es actualizar las variables globales de posición (X, Y) y convertir la orientación del robot de cuaterniones a ángulos de Euler para obtener el yaw (giro sobre el eje Z).
  
  sentido(X, Y, yaw): Esta función determina una velocidad angular basada en la proximidad del robot a ciertos límites definidos como "muros". Evalúa si la posición actual ha cruzado los límites establecidos y,devuelve una velocidad para girar y evitar salir del área delimitada dependiendo de la orientación actual.
  
  Bloque principal (if __name__ == '__main__':): Se inicializa el nodo de ROS y se definen el publisher de velocidad y el suscriber de odometría. Utiliza un bucle for que se repite 4 veces (una por cada lado del cuadrado).
  En cada iteración, primero realiza un giro hasta que el ángulo de orientación (yaw) alcanza un umbral específico.
  
  Posteriormente, desplaza el robot en línea recta durante un número determinado de ciclos (500 iteraciones) antes de pasar al siguiente giro.
  ### Diagrama de flujo
 
<img width="786" height="473" alt="image" src="https://github.com/user-attachments/assets/f68610f9-0e8e-42f4-b6b8-518e4fb2f2fe" />

### Video demostrativo
[Clip trayectoria cuadrado](./.img/square.mp4)


