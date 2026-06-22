# Notificador automático

**Notificador automático** es una herramienta de gestion bancaria desarrollada en **Python** para analizar cuotas o prestamos bancarios **con el fin de enviar un correo** a un destinatario específico, con **avisos por impago o cuotas vencidas**.

¿Que soluciona esta herramienta automática?:  
**Sustituye el seguimiento manual de los pagos, retrasos en las reclamaciones y una comunicación tardía con los clientes.**.

---

## ¿Por qué creé esta herramienta?
Nacio con la idea de practicar conceptos de programación orientada a objetos aplicándolos a un problema cotidiano en lugar de desarrollar ejemplos comunes o aislados, así que decidí crear una pequeña herramienta con una utilidad concreta que podria llegar a ser útil.


Esta herramienta permite al usuario:

- Identificar cada cuota mediante un nombre descriptivo (por ejemplo: Agua, Luz, Internet o Netflix)
- Definir el importe requerido para cada cuota de forma independiente
- Registrar pagos realizados indicando la fecha de pago y el importe abonado
- Detectar automáticamente cuotas pagadas fuera de plazo
- Identificar cuotas impagadas
- Calcular los recargos aplicables en función de los días de retraso
- Enviar notificaciones automáticas por correo electrónico cuando detecte incidencias en cuotas

Alacance de esta herramienta:

- No gestiona la contratación, modificación o cancelación de servicios financieros.
- Su responsabilidad se limita al análisis del estado de cuotas previamente definidas y a la automatización de las notificaciones según resultados de dicho analisis.

---

## Funcionalidades principales

### Planificación automática de cuotas
El programa genera automáticamente las fechas previstas de las cuotas a partir de una fecha de inicio definida por el usuario.

Además, tiene en cuenta los días no laborables para desplazar los vencimientos al siguiente día hábil cuando sea necesario.

Esto permite simular de forma más realista el comportamiento de un sistema de gestión de pagos recurrentes.

---

### Gestión de cuotas descriptivas
La herramienta permite trabajar con cuotas identificadas mediante nombres descriptivos en lugar de simples índices numéricos.

Por ejemplo:

- `Agua`
- `Luz`
- `Internet`
- `Netflix`

Esto hace que el análisis sea mucho más comprensible tanto para desarrolladores como para usuarios finales.

---

### Análisis automático del estado de los pagos
El sistema compara las cuotas planificadas con los pagos realmente efectuados para determinar el estado de cada una.

Puede identificar automáticamente situaciones como:

- cuotas pagadas correctamente y dentro del plazo
- cuotas pagadas con retraso
- cuotas impagadas
- cuotas abonadas parcialmente

De esta forma, se elimina la necesidad de revisar manualmente cada pago.

---

### Detección y cálculo de incidencias
Cuando una cuota presenta alguna incidencia, la aplicación calcula automáticamente la información necesaria para gestionarla.

Entre otros aspectos, puede determinar:

- días de retraso acumulados
- importe pendiente de abonar
- recargos aplicables por demora

Esto permite automatizar tareas que habitualmente requieren una revisión manual.

---

### Sistema automático de notificaciones
Cuando se detecta una incidencia en una cuota, la herramienta genera y envía una notificación por correo electrónico al destinatario configurado.

Las notificaciones incluyen información relevante como:

- cuota afectada
- días de retraso
- recargo aplicado

De esta forma, el proceso de comunicación con el cliente queda completamente automatizado.

---

### Validación de datos de entrada
Antes de procesar la información, el programa realiza diversas comprobaciones para garantizar la integridad de los datos recibidos.

Puede detectar situaciones como:

- fechas inválidas
- listas de pagos incorrectas
- correos electrónicos mal formados
- pagos sin estructura válida
- información obligatoria ausente

Refuerza la robustez del sistema.

---

### Sistema de logs
La aplicación incluye un sistema de logging estructurado que registra:

- el flujo completo de ejecución
- la generación de cuotas
- pagos procesados
- incidencias detectadas
- advertencias
- errores de validación
- envío de notificaciones por correo
- estado final del análisis

Para facilitar el mantenimiento(deteccion de posibles bugs) y la depuración del proceso.

---

## Estructura del proyecto

```bash
BankSystem/
│
├── main.py
├── banco.py
├── eventos.py
├── notificaciones.py
├── logger.py
├── README.md
├── requirements.txt
├── .gitignore
│
├── logs/
│   └── banco.log
│
└── .env
