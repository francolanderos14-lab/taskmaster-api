# ECS Fargate vs Kubernetes (k3s): comparación práctica

Notas escritas en base a la experiencia real de implementar el mismo backend
(TaskMaster API) en dos orquestadores distintos dentro del mismo proyecto de
portfolio.

## Complejidad de implementación

Levantar la infraestructura en ECS Fargate (Etapas 3-4) resultó más simple en
términos de piezas a conectar: VPC, ALB, ECS, pipeline de CI/CD — todo
integrado de forma nativa por AWS. Kubernetes con k3s, en cambio, requirió más
pasos manuales de configuración (por ejemplo, la autenticación contra ECR), lo
cual lo hizo más tedioso en el momento, pero también más entretenido y
formativo: entender cada pieza de forma manual generó una comprensión más
profunda de lo que realmente está pasando por debajo.

Importante aclarar: esta comparación no es "ECS completo" vs "k3s completo".
En ECS se construyó todo el ecosistema (ALB, métricas, pipeline de CI/CD
integrado), mientras que en k3s solo se cubrieron los fundamentos (Pods,
Deployment, Service) — no se llegó a implementar Ingress, monitoreo tipo
Prometheus, ni un pipeline de CI/CD equivalente. La mayor "robustez" percibida
en ECS responde en parte a esa diferencia de alcance, no únicamente a
diferencias inherentes entre plataformas.

## Autenticación y seguridad

En ECS, la autenticación contra ECR la maneja AWS de forma transparente. En
k3s, hubo que crear manualmente un Secret de Kubernetes (`ecr-secret`) con un
token temporal de ECR (válido por 12 horas). Esto se percibió como un paso
tedioso pero no como una desventaja: obliga a estar más al tanto de las
credenciales y agrega una capa de seguridad explícita. Queda pendiente
explorar en el futuro mecanismos más elegantes para producción (por ejemplo,
IAM Roles for Service Accounts), sin profundizar aún en el abanico completo
de escenarios que existen alrededor del manejo de Secrets en Kubernetes.

## Resiliencia y arquitectura

La instalación de k3s de este proyecto corrió en un único nodo EC2 — una
elección consciente por presupuesto y por ser un proyecto de portfolio, no
una ventaja real de arquitectura. En un entorno de producción, la resiliencia
de Kubernetes viene de tener un cluster con múltiples nodos: si un nodo cae,
el Deployment reprograma los Pods en otro nodo disponible. Un solo nodo no
resuelve el problema de disponibilidad — solo permite aprender los
fundamentos sin el costo de un cluster multi-nodo.

## Fundamentos aprendidos

Al cierre de esta etapa, los tres conceptos centrales de Kubernetes quedaron
claros a nivel práctico:

- **Pod:** la unidad mínima que contiene el contenedor de la aplicación
  corriendo.
- **Deployment:** vigila la cantidad de réplicas de Pods activos y repone
  automáticamente los que se caen, manteniendo el número deseado. (No
  verifica la salud interna de la aplicación en sí — eso correspondería a
  readiness/liveness probes, no cubierto en esta etapa.)
- **Service:** cumple un rol equivalente al del ALB en ECS — reparte el
  tráfico entrante entre los Pods activos, sin que importe cuáles son ni
  dónde están en un momento dado.

## Conclusión honesta para portfolio

No se cuenta con experiencia sólida de Kubernetes en producción. Sí se
adquirió comprensión práctica y verificada de los fundamentos —Pods,
Deployments, Services— trabajando en un entorno real (EC2 con k3s), suficiente
para hablar de ellos con criterio propio, sin sobrerrepresentar el nivel de
experiencia alcanzado.