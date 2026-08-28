# Brief Técnico del Proyecto Sello: ChaskiPC

---

## 1. Datos del equipo
* **Nombre del equipo:** Equipo 01 - ChaskiByte Systems
* **Sección:** 5to Ciclo - Grupo Único
* **Repositorio (URL):** https://github.com/jaisesasaki24-cloud/pagatu-orden-ms
* **Topics del repositorio configurados (sí/no):** Sí (`campus-juliaca`, `semestre-2026-2`, `linea-software`, `tipo-ps`, `dist`, `seccion-g1`, `grupo-01-chaskipc`)
* **Integrantes:**

| Integrante | Rol o énfasis previsto | Microservicio transaccional | Microservicio no transaccional |
| :--- | :--- | :--- | :--- |
| **Eliceo Parillo Mostajo** | Arquitectura backend, gestión de órdenes de compra y catálogo de hardware | `pc-orden-ms` | `pc-catalogo-ms` |
| **Laura Vargas Cristhian Paul** | Pasarela de pagos externa (Mercado Pago), seguridad y autenticación (Keycloak/JWT) | `pc-pago-ms` | `pc-auth-ms` |

> ⚠️ *Nota aclaratoria:* La asignación de roles, microservicios, alcance y tareas de cada integrante son preliminares y están **sujetas a modificaciones o ajustes** conforme avance el desarrollo del proyecto durante el ciclo.

---

## 2. Dominio del proyecto
* **Nombre del proyecto:** **ChaskiPC Hardware E-Commerce** (Sistema Distribuido para la Venta de Computadoras y Componentes)
* **Problema o necesidad que resuelve (2-4 líneas):**  
  Resuelve la dificultad que enfrentan los usuarios y empresas para cotizar y adquirir computadoras ensambladas, periféricos y piezas de hardware con verificación de stock en tiempo real. Proporciona una plataforma distribuida ágil, segura y confiable que automatiza el flujo completo desde la selección de piezas hasta el pago electrónico inmediato.
* **Dominio de negocio:**  
  Comercio electrónico especializado en tecnología y cómputo (laptops, PCs de escritorio, procesadores, tarjetas gráficas, placas madre, fuentes de poder y periféricos). El flujo operativo es: **Catálogo de Hardware (`pc-catalogo-ms`) → Generación de Orden de Compra (`pc-orden-ms`) → Liquidación y Pago en Línea (`pc-pago-ms`)**.
* **Usuarios / actores principales:**  
  * **Cliente / Comprador:** Explora componentes, filtra por especificaciones técnicas, genera órdenes y realiza pagos en línea.
  * **Administrador / Gestor de Inventario:** Gestiona el catálogo, actualiza precios, repone existencias y supervisa el estado de las transacciones.
* **Servicio externo real que integra el proyecto:**  
  **Mercado Pago API (Checkout Pro / Checkout API en modo Sandbox)**: Procesamiento real de transacciones bancarias, tarjetas de débito/crédito y validación asíncrona de pagos mediante Webhooks/IPN oficiales.
* **¿Continúa un proyecto de un ciclo anterior, o es un dominio nuevo?**  
  Dominio nuevo, adaptando el marco arquitectónico y el flujo distribuido de *PagaTu*.

---

## 3. Microservicios previstos y alcance esperado

### Fichas por Microservicio

#### Microservicio: `pc-orden-ms` (Integrante: Eliceo Parillo Mostajo · Tipo: Transaccional)
* **Descripción breve:** Administra el ciclo de vida de las órdenes de compra. Recibe los productos seleccionados, valida existencias con el catálogo, calcula subtotales, el 18% de IGV y el total general, emitiendo la orden en estado pendiente de cobro.
* **Cabecera-Detalle:** Cabecera: `Orden` / Detalle: `DetalleOrden`
* **Datos iniciales previstos:**  
  * `Orden`: `id`, `codigo_orden`, `cliente_id`, `fecha_creacion`, `subtotal`, `igv`, `total`, `estado` (PENDIENTE, PAGADO, CANCELADO, ENVIADO).
  * `DetalleOrden`: `id`, `orden_id`, `producto_id`, `nombre_producto`, `precio_unitario`, `cantidad`, `subtotal_item`.
* **Endpoints iniciales previstos:**  
  * `POST /api/v1/ordenes`: Registra una nueva orden con su respectivo detalle de ítems.
  * `GET /api/v1/ordenes/{id}`: Consulta la información completa de una orden.
  * `GET /api/v1/ordenes/cliente/{clienteId}`: Lista el historial de compras de un cliente.
  * `PUT /api/v1/ordenes/{id}/estado`: Actualiza el estado de la orden tras recibir confirmación de pago.
* **¿Se comunica con otro microservicio?** Sí. Síncrono (OpenFeign) con `pc-catalogo-ms` y con `pc-pago-ms`.
* **Rutas protegidas y roles:** `POST /api/v1/ordenes` (Rol `CLIENTE`), `PUT /api/v1/ordenes/{id}/estado` (Rol `SISTEMA`/`ADMIN`).
* **Lista inicial de requisitos:**  
  1. Validar que la cantidad de ítems solicitada no supere el stock disponible.
  2. Calcular automáticamente el 18% de IGV y el monto total en base a los subtotales del detalle.
  3. Bloquear la edición de ítems una vez que la orden pase a estado `PAGADO`.

#### Microservicio: `pc-catalogo-ms` (Integrante: Eliceo Parillo Mostajo · Tipo: No transaccional)
* **Descripción breve:** Gestiona el inventario de piezas de hardware (CPUs, GPUs, RAM, Placas), periféricos y computadoras organizadas por categorías y marcas.
* **Entidad principal:** `Producto` / `Categoria`
* **Datos iniciales previstos:**  
  * `Producto`: `id`, `sku`, `nombre`, `marca`, `precio`, `stock_disponible`, `categoria_id`, `imagen_url`.
  * `Categoria`: `id`, `nombre`, `descripcion`, `activo`.
* **Endpoints iniciales previstos:**  
  * `GET /api/v1/productos`: Consulta pública del catálogo con filtros por marca, precio y categoría.
  * `GET /api/v1/productos/{id}`: Retorna la ficha técnica y existencias de un componente.
  * `POST /api/v1/productos`: Registra un nuevo componente en el catálogo.
  * `PUT /api/v1/productos/{id}/stock`: Descuenta o repone stock tras compras.
* **¿Se comunica con otro microservicio?** Sí, atiende validaciones de existencias desde `pc-orden-ms`.
* **Rutas protegidas y roles:** `GET /api/v1/productos/**` (Público), `POST`, `PUT`, `DELETE` (Rol `ADMIN`).
* **Lista inicial de requisitos:**  
  1. Permitir consultar y filtrar componentes por categoría y precio de forma pública.
  2. Validar la unicidad del código `SKU` para evitar productos duplicados.
  3. Descontar stock en tiempo real tras la confirmación de compra.

#### Microservicio: `pc-pago-ms` (Integrante: Laura Vargas Cristhian Paul · Tipo: Transaccional)
* **Descripción breve:** Procesa cobros conectándose con la pasarela real **Mercado Pago**, generando preferencias de pago y recibiendo notificaciones asíncronas vía Webhook.
* **Cabecera-Detalle:** Cabecera: `Pago` / Detalle: `TransaccionPasarela`
* **Datos iniciales previstos:**  
  * `Pago`: `id`, `orden_id`, `monto`, `moneda` (PEN), `metodo_pago`, `estado` (PENDING, APPROVED, REJECTED), `fecha_pago`.
  * `TransaccionPasarela`: `id`, `pago_id`, `payment_id_externo`, `preference_id`, `respuesta_raw_json`, `fecha_procesamiento`.
* **Endpoints iniciales previstos:**  
  * `POST /api/v1/pagos/checkout`: Crea la preferencia en Mercado Pago y genera el link de pago.
  * `POST /api/v1/pagos/webhook`: Recibe la notificación de cobro exitoso enviada por Mercado Pago.
  * `GET /api/v1/pagos/orden/{ordenId}`: Consulta el estado financiero de una orden.
* **¿Se comunica con otro microservicio?** Sí. Recibe la orden de `pc-orden-ms` y notifica el resultado.
* **Rutas protegidas y roles:** `POST /api/v1/pagos/checkout` (Rol `CLIENTE`), `POST /api/v1/pagos/webhook` (Público con firma segura).
* **Lista inicial de requisitos:**  
  1. Conectarse a la API de Mercado Pago para generar un `preference_id` válido en Sandbox.
  2. Procesar el webhook entrante y validar el estado `approved` antes de marcar la orden como pagada.
  3. Guardar el identificador de pago externo para auditoría financiera.

#### Microservicio: `pc-auth-ms` (Integrante: Laura Vargas Cristhian Paul · Tipo: No transaccional)
* **Descripción breve:** Proveedor de identidad y control de acceso. Administra usuarios, credenciales y emisión de tokens JWT firmados con roles (`CLIENTE`, `ADMIN`).
* **Entidad principal:** `Usuario` / `Rol`
* **Datos iniciales previstos:**  
  * `Usuario`: `id`, `username`, `email`, `password_hash`, `nombre_completo`, `activo`.
  * `Rol`: `id`, `nombre_rol` (`ROLE_CLIENTE`, `ROLE_ADMIN`).
* **Endpoints iniciales previstos:**  
  * `POST /api/v1/auth/register`: Registro de nuevos clientes.
  * `POST /api/v1/auth/login`: Autenticación de credenciales y retorno del Token JWT.
  * `GET /api/v1/auth/validate`: Verificación y decodificación de tokens para el API Gateway y microservicios.
* **¿Se comunica con otro microservicio?** No; los demás microservicios validan los tokens emitidos por este componente.
* **Rutas protegidas y roles:** `POST /api/v1/auth/login` y `register` (Públicas), `GET /api/v1/usuarios/**` (Rol `ADMIN`).
* **Lista inicial de requisitos:**  
  1. Encriptar las contraseñas con BCrypt antes de almacenarlas en la base de datos.
  2. Emitir tokens JWT firmados con tiempo de expiración y roles en el payload.
  3. Rechazar registros con correos electrónicos duplicados.

---

## Alcance Global del Proyecto

### ✅ Qué SÍ cubre:
1. Catálogo interactivo de hardware y computadoras con control de inventario dinámico.
2. Gestión de compras mediante órdenes transaccionales estructuradas en cabecera y detalle.
3. Procesamiento real de pagos en línea integrado con la API de **Mercado Pago (Sandbox)** y Webhooks.
4. Seguridad distribuida con validación de tokens JWT en todos los microservicios.
5. Arquitectura completa: Config Server, Eureka, API Gateway y bases de datos independientes en PostgreSQL (Docker).

### ❌ Qué NO cubre:
1. Integración con empresas de transporte o courier para tracking físico de envíos.
2. Facturación electrónica formal conectada con la SUNAT.
3. Simulador 3D de ensamblaje o cálculo automático de vatios de fuente de poder.

---

## 4. Aprobación
* **Docente:** _______________________________
* **Fecha:** 27 de agosto de 2026