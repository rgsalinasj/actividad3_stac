import pandas as pd


def create_corpus(filename: str = "corpus.csv") -> None:
    documents = [
        # --- CATEGORÍA 1: Politicas/Procesos (DOC001 - DOC012) ---
        {
            "id": "DOC001",
            "title": "Política de Trabajo Remoto y Esquema Híbrido",
            "category": "Politicas/Procesos",
            "text": (
                "Los empleados pueden trabajar de forma remota hasta tres días por semana con aprobación "
                "de su gerente directo. El horario núcleo de colaboración es de 10:00 a 15:00 horas. "
                "Los trabajadores remotos deben mantener un espacio seguro, utilizar la VPN corporativa "
                "para acceder a sistemas internos y contar con conexión estable a internet."
            ),
        },
        {
            "id": "DOC002",
            "title": "Estándar de Seguridad de la Información y Acceso VPN",
            "category": "Politicas/Procesos",
            "text": (
                "Todas las conexiones remotas hacia redes corporativas, repositorios en la nube y bases de datos "
                "internas deben realizarse mediante la VPN empresarial autorizada con autenticación multifactor. "
                "Queda estrictamente prohibido compartir credenciales o conectarse desde redes Wi-Fi públicas "
                "sin cifrado ni túnel VPN activo."
            ),
        },
        {
            "id": "DOC003",
            "title": "Política de Gestión de Contraseñas y Autenticación Multifactor",
            "category": "Politicas/Procesos",
            "text": (
                "Las cuentas corporativas exigen contraseñas de al menos 14 caracteres combinando mayúsculas, "
                "minúsculas, números y símbolos. La autenticación multifactor mediante aplicación autenticadora "
                "o llave física es obligatoria para correo electrónico, VPN y portales de inicio de sesión único."
            ),
        },
        {
            "id": "DOC004",
            "title": "Procedimiento de Viáticos y Reembolso de Gastos de Viaje",
            "category": "Politicas/Procesos",
            "text": (
                "Los colaboradores que viajen por motivos laborales deben cargar facturas fiscalmente válidas "
                "en el portal de gastos dentro de los 15 días hábiles posteriores al regreso. Son reembolsables "
                "boletos de avión en clase económica, hospedaje estándar, transporte terrestre y alimentos."
            ),
        },
        {
            "id": "DOC005",
            "title": "Lineamientos de Uso de Tarjetas de Crédito Corporativas",
            "category": "Politicas/Procesos",
            "text": (
                "Las tarjetas corporativas se asignan a viajeros frecuentes y líderes de área para compras "
                "empresariales autorizadas, licencias de software y hospedaje. Los titulares deben conciliar "
                "sus estados de cuenta mensuales con comprobantes en el portal financiero antes del día 5."
            ),
        },
        {
            "id": "DOC006",
            "title": "Proceso de Solicitud de Vacaciones y Días Libres",
            "category": "Politicas/Procesos",
            "text": (
                "El personal de tiempo completo acumula 20 días hábiles de vacaciones al año. Las solicitudes "
                "mayores a tres días consecutivos deben registrarse en el portal de Recursos Humanos con al "
                "menos dos semanas de anticipación para aprobación del supervisor."
            ),
        },
        {
            "id": "DOC007",
            "title": "Política de Incapacidades Médicas y Ausencias por Salud",
            "category": "Politicas/Procesos",
            "text": (
                "Los empleados que no puedan laborar por enfermedad o consulta médica deben notificar a su "
                "supervisor antes del inicio de jornada y registrar la ausencia en el portal de Recursos Humanos. "
                "Ausencias mayores a tres días requieren certificado médico oficial."
            ),
        },
        {
            "id": "DOC008",
            "title": "Lista de Verificación de Incorporación y Aprovisionamiento TI",
            "category": "Politicas/Procesos",
            "text": (
                "Recursos Humanos inicia el proceso de incorporación cinco días hábiles antes del ingreso. "
                "El área de TI prepara computadora portátil, correo corporativo, credenciales de inicio de sesión "
                "único y certificados VPN. El nuevo ingreso debe completar la capacitación de ciberseguridad."
            ),
        },
        {
            "id": "DOC009",
            "title": "Procedimiento de Baja de Personal y Devolución de Equipos",
            "category": "Politicas/Procesos",
            "text": (
                "Ante renuncia o terminación laboral, Recursos Humanos notifica a seguridad informática para "
                "revocar accesos de VPN, correo electrónico y aplicaciones corporativas al cierre del último turno. "
                "El colaborador debe devolver laptop, credencial física y tarjeta corporativa en cinco días hábiles."
            ),
        },
        {
            "id": "DOC010",
            "title": "Clasificación de Datos y Manejo de Información Confidencial",
            "category": "Politicas/Procesos",
            "text": (
                "Todos los archivos de la empresa deben clasificarse como Públicos, Internos, Confidenciales o "
                "Restringidos. Los registros financieros y datos personales de clientes deben cifrarse en reposo "
                "y en tránsito, almacenándose únicamente en repositorios en la nube aprobados."
            ),
        },
        {
            "id": "DOC011",
            "title": "Proceso de Compras, Proveedores y Adquisición de Software",
            "category": "Politicas/Procesos",
            "text": (
                "Toda nueva suscripción SaaS o contrato con terceros superior a 2,500 dólares requiere evaluación "
                "de seguridad informática, revisión de privacidad de datos y aprobación de compras antes de contratar. "
                "No se reembolsan licencias pagadas con tarjetas personales."
            ),
        },
        {
            "id": "DOC012",
            "title": "Política de Seguridad para Dispositivos Personales (BYOD)",
            "category": "Politicas/Procesos",
            "text": (
                "Los empleados que consulten correo corporativo o mensajería empresarial en teléfonos celulares "
                "personales deben registrar el equipo en la plataforma MDM, activar bloqueo biométrico y autorizar "
                "el borrado remoto de datos corporativos en caso de robo o extravío del teléfono."
            ),
        },

        # --- CATEGORÍA 2: Soporte/Incidentes (DOC013 - DOC024) ---
        {
            "id": "DOC013",
            "title": "Incidente INC-401: Errores de Tiempo Agotado en Autenticación VPN",
            "category": "Soporte/Incidentes",
            "text": (
                "Varios trabajadores remotos reportaron desconexiones de VPN y errores de tiempo agotado al "
                "autenticarse en el nodo principal. La causa raíz fue un certificado RADIUS vencido en el servidor "
                "secundario de autenticación. La renovación del certificado restableció el servicio VPN."
            ),
        },
        {
            "id": "DOC014",
            "title": "Incidente INC-402: Bucle de Inicio de Sesión Único en Portal Web",
            "category": "Soporte/Incidentes",
            "text": (
                "Los usuarios experimentaron un bucle infinito de redirección al ingresar a los portales de "
                "Recursos Humanos y gastos desde Chrome. El fallo se debió a cookies de sesión SAML corruptas "
                "tras actualizar el proveedor de identidad. Limpiar caché y actualizar metadatos resolvió el error."
            ),
        },
        {
            "id": "DOC015",
            "title": "Incidente INC-403: Retraso en Notificaciones Push de Autenticación Multifactor",
            "category": "Soporte/Incidentes",
            "text": (
                "Mesa de ayuda recibió 45 tickets por retrasos de hasta tres minutos en notificaciones push de "
                "autenticación multifactor durante el horario matutino. Se recomendó a los usuarios emplear "
                "códigos temporales TOTP de la aplicación autenticadora mientras el proveedor estabilizaba el envío."
            ),
        },
        {
            "id": "DOC016",
            "title": "Ticket TKT-812: Laptop Nueva No Conecta a Red Wi-Fi Corporativa",
            "category": "Soporte/Incidentes",
            "text": (
                "Una computadora portátil recién aprovisionada falló al autenticarse en la red inalámbrica "
                "corporativa WPA2-Enterprise. La revisión mostró que faltaba el certificado raíz interno en la "
                "imagen inicial. Se desplegó el perfil mediante MDM y se restableció la conexión Wi-Fi."
            ),
        },
        {
            "id": "DOC017",
            "title": "Incidente INC-408: Alto Consumo de CPU y Consultas Lentas en Base de Datos",
            "category": "Soporte/Incidentes",
            "text": (
                "La latencia en el proceso de pago aumentó debido a un 98% de uso de CPU en la base de datos "
                "PostgreSQL de producción. El registro de consultas lentas detectó un escaneo completo sin índice "
                "en la tabla de pedidos. Crear un índice compuesto redujo el uso de CPU al 25%."
            ),
        },
        {
            "id": "DOC018",
            "title": "Incidente INC-411: Interrupción 502 Bad Gateway en API Gateway",
            "category": "Soporte/Incidentes",
            "text": (
                "Clientes externos recibieron errores HTTP 502 Bad Gateway durante 22 minutos. Los contenedores "
                "del microservicio agotaron su límite de memoria por una fuga en la serialización JSON. Revertir "
                "el despliegue y ampliar la cuota de memoria estabilizó el tráfico."
            ),
        },
        {
            "id": "DOC019",
            "title": "Ticket TKT-845: Error al Subir Comprobantes PDF en Portal de Gastos",
            "category": "Soporte/Incidentes",
            "text": (
                "Colaboradores en viaje reportaron errores HTTP 413 al cargar facturas PDF de alta resolución en el "
                "portal de reembolso de gastos. El proxy inverso tenía un límite de carga de 2 MB. Incrementar "
                "el parámetro client_max_body_size a 15 MB solucionó la carga de archivos."
            ),
        },
        {
            "id": "DOC020",
            "title": "Incidente INC-419: Retraso en Entrega de Correo Electrónico Externo",
            "category": "Soporte/Incidentes",
            "text": (
                "Los correos corporativos enviados a clientes externos quedaron en cola durante dos horas. Se detectó "
                "un registro DNS SPF y DKIM mal configurado tras migrar el servidor de salida. Corregir los registros "
                "DNS restauró la entrega inmediata de correo electrónico."
            ),
        },
        {
            "id": "DOC021",
            "title": "Ticket TKT-890: Bloqueo Recurrente de Cuenta Tras Cambio de Contraseña",
            "category": "Soporte/Incidentes",
            "text": (
                "La cuenta de un usuario se bloqueaba cada 10 minutos después de actualizar su contraseña. Un cliente "
                "de correo en su teléfono móvil y una unidad de red guardaban credenciales anteriores. Eliminar las "
                "contraseñas en caché y reautenticar el correo móvil detuvo los bloqueos."
            ),
        },
        {
            "id": "DOC022",
            "title": "Incidente INC-425: Permiso Denegado en Carpeta Compartida de Finanzas",
            "category": "Soporte/Incidentes",
            "text": (
                "Integrantes del área financiera perdieron acceso de lectura a la carpeta de conciliación trimestral "
                "tras modificar roles IAM. Una regla de denegación bloqueó los permisos sobre archivos confidenciales. "
                "Restaurar la política explícita del grupo de finanzas devolvió el acceso."
            ),
        },
        {
            "id": "DOC023",
            "title": "Ticket TKT-904: Notificaciones de Mensajería No Sincronizan en Celular",
            "category": "Soporte/Incidentes",
            "text": (
                "Varios usuarios con teléfonos personales BYOD reportaron falta de notificaciones en la aplicación "
                "de mensajería corporativa. El ahorro de batería y una política MDM desactualizada suspendían la "
                "sincronización en segundo plano. Actualizar el perfil MDM resolvió el problema."
            ),
        },
        {
            "id": "DOC024",
            "title": "Incidente INC-430: Fallo en Respaldo Nocturno Automatizado de Base de Datos",
            "category": "Soporte/Incidentes",
            "text": (
                "La copia de seguridad nocturna de la base de datos de clientes falló por falta de espacio en el "
                "almacenamiento de respaldos. Las reglas de retención no depuraban copias mayores a 90 días. "
                "Activar el archivado automático y ampliar la cuota permitió completar el respaldo."
            ),
        },

        # --- CATEGORÍA 3: Ingenieria/Operaciones (DOC025 - DOC030) ---
        {
            "id": "DOC025",
            "title": "Guía Operativa de Indexación y Optimización de Consultas SQL",
            "category": "Ingenieria/Operaciones",
            "text": (
                "Para diagnosticar consultas lentas en PostgreSQL, revise pg_stat_statements y ejecute EXPLAIN ANALYZE "
                "para identificar escaneos secuenciales en tablas grandes. Cree índices compuestos en columnas de "
                "filtrado frecuente y ejecute reportes pesados sobre réplicas de lectura."
            ),
        },
        {
            "id": "DOC026",
            "title": "Manual de Despliegue Sin Interrupciones para Microservicios",
            "category": "Ingenieria/Operaciones",
            "text": (
                "Los despliegues en producción deben utilizar actualizaciones graduales con sondas de disponibilidad "
                "y reversión automática. Monitoree tasas de error HTTP 5xx, memoria de contenedores y latencia del "
                "API Gateway durante 15 minutos tras liberar cambios."
            ),
        },
        {
            "id": "DOC027",
            "title": "Protocolo de Recuperación ante Desastres y Verificación de Respaldos",
            "category": "Ingenieria/Operaciones",
            "text": (
                "Las bases de datos críticas requieren copias de seguridad cifradas cada noche replicadas en dos "
                "regiones geográficas. Operaciones debe realizar simulacros mensuales de restauración para validar "
                "la integridad de los respaldos y el cumplimiento del tiempo objetivo de recuperación."
            ),
        },
        {
            "id": "DOC028",
            "title": "Matriz de Clasificación de Severidad y Escalamiento de Incidentes",
            "category": "Ingenieria/Operaciones",
            "text": (
                "Los incidentes de Severidad 1 que afecten autenticación, VPN o pagos de clientes exigen alertar de "
                "inmediato al ingeniero de guardia y publicar actualizaciones cada 15 minutos. El análisis de causa "
                "raíz debe documentarse dentro de las 48 horas posteriores."
            ),
        },
        {
            "id": "DOC029",
            "title": "Guía de Diagnóstico de Red Wi-Fi Empresarial y Certificados",
            "category": "Ingenieria/Operaciones",
            "text": (
                "La red inalámbrica corporativa autentica dispositivos mediante WPA2-Enterprise y RADIUS usando "
                "certificados digitales. Si una laptop no conecta, verifique la sincronización del reloj del sistema, "
                "el perfil MDM instalado y la vigencia del certificado raíz interno."
            ),
        },
        {
            "id": "DOC030",
            "title": "Configuración de Proxy Inverso y Límites de Tamaño en API Gateway",
            "category": "Ingenieria/Operaciones",
            "text": (
                "El proxy inverso perimetral aplica cifrado TLS, límites de tamaño de petición y control de tasa para "
                "proteger microservicios. Ajuste client_max_body_size en portales que reciben archivos PDF pesados "
                "y configure tiempos de espera adecuados para evitar errores 502 y 504."
            ),
        },
    ]

    df = pd.DataFrame(documents)[["id", "title", "text", "category"]]
    df.to_csv(filename, index=False, encoding="utf-8")
    print(f"Archivo '{filename}' generado exitosamente con {len(df)} documentos.")


if __name__ == "__main__":
    create_corpus()
