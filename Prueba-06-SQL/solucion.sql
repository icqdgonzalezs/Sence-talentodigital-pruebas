-- ================================================================================
-- PRUEBA: Diseño y manipulación de tablas SQL
-- ================================================================================
-- Autor        : David González Santibañez
-- Curso        : Fundamentos de Análisis de Datos
-- Contexto     : Gestión de proveedores para un sistema de capacitaciones.
-- Descripción  : 
--   Esta prueba valida mis conocimientos de DDL (Data Definition Language) y
--   DML (Data Manipulation Language). Como ingeniero químico, veo esta base de
--   datos como un "proceso" donde debo establecer reglas estrictas (CHECK, NOT NULL)
--   para que la materia prima (los datos) no se contamine. 
--   A continuación, desarrollo la tabla, la poblo, la actualizo y la limpio.
-- ================================================================================

-- ================================================================================
-- REQUERIMIENTO 1: Creación de la tabla con restricciones (3 Puntos)
-- ================================================================================
-- Descripción: Creo la tabla 'proveedores_capacitaciones' con las reglas de calidad 
-- solicitadas. El CHECK actúa como una válvula de control de entrada para evitar 
-- categorías inválidas, y UNIQUE protege contra duplicados fiscales.
-- Código:

DROP TABLE IF EXISTS proveedores_capacitaciones;

CREATE TABLE proveedores_capacitaciones (
    id_proveedor SERIAL PRIMARY KEY,
    razon_social TEXT NOT NULL,
    rut TEXT NOT NULL UNIQUE,
    categoria TEXT NOT NULL CHECK (categoria IN ('Interno', 'Externo')),
    estado BOOLEAN DEFAULT TRUE
);

-- ================================================================================
-- REQUERIMIENTO 2: Insertar y validar registros (2 Puntos)
-- ================================================================================
-- 2.1 INSERCIONES VÁLIDAS
-- Descripción: Inserto 4 registros que cumplen todas las restricciones.
-- El campo 'estado' se llenará automáticamente con TRUE gracias a DEFAULT.
-- Código:

INSERT INTO proveedores_capacitaciones (razon_social, rut, categoria) VALUES 
    ('Capacitaciones Tech S.A.', '76987654-3', 'Externo'),
    ('Formación Interna Ltda.', '12345678-9', 'Interno'),
    ('Academia de Negocios Sur', '98765432-1', 'Externo'),
    ('Consultores Asociados', '56789012-4', 'Interno');


-- 2.2 INSERCIONES ERRÓNEAS (Documentación de errores en pgAdmin)
-- Descripción: Intencionalmente violo las restricciones para documentar los errores.
-- En pgAdmin, al ejecutar estas líneas, el panel de "Messages" mostrará los errores.
-- Intento 1: Violar UNIQUE (RUT duplicado). 
-- El motor lanzará: "duplicate key value violates unique constraint".
-- Código:

INSERT INTO proveedores_capacitaciones (razon_social, rut, categoria) VALUES 
    ('Nueva Empresa Falsa', '12345678-9', 'Externo');

-- Intento 2: Violar CHECK (Categoría inválida).
-- El motor lanzará: "check constraint violation".
-- Código:

INSERT INTO proveedores_capacitaciones (razon_social, rut, categoria) VALUES 
    ('Proveedor Errante', '11111111-1', 'Mixto');


-- ================================================================================
-- REQUERIMIENTO 3: Actualizar información (2 Puntos)
-- ================================================================================
-- Descripción: Actualizo registros basándome en decisiones de negocio.
-- Siempre se debe usar WHERE para afectar solo al registro objetivo.
-- Código:

-- 3.1 El proveedor 'Consultores Asociados' (id=4) cambia a proveedor externo.
UPDATE proveedores_capacitaciones 
SET categoria = 'Externo' 
WHERE id_proveedor = 4;

-- 3.2 El proveedor 'Academia de Negocios Sur' (id=3) queda inactivo (FALSE).
UPDATE proveedores_capacitaciones 
SET estado = FALSE 
WHERE id_proveedor = 3;


-- ================================================================================
-- REQUERIMIENTO 4: Eliminar registros con condiciones (3 Puntos)
-- ================================================================================
-- Descripción: Elimino el proveedor que quedó inactivo. 
-- ADVERTENCIA DE SEGURIDAD: La cláusula WHERE es la "válvula de seguridad".
-- Si ejecuto DELETE sin WHERE, borraría toda la tabla de proveedores.
-- Código:

DELETE FROM proveedores_capacitaciones 
WHERE estado = FALSE;

-- ================================================================================
-- VERIFICACIÓN FINAL
-- ================================================================================
-- Descripción: Verifico que el proceso completo haya funcionado correctamente.
-- Resultado esperado: Solo deben quedar 3 filas (id 1, 2 y 4). El id 3 fue eliminado.
-- Código de verificación:

SELECT id_proveedor, razon_social, estado 
FROM proveedores_capacitaciones;

-- Reflexión final de ingeniería (Nota mental para el profesor):
-- Esta prueba me ha permitido entender que una base de datos es un reactor químico de información.
-- Las restricciones (UNIQUE, CHECK, DEFAULT) son mis "sensores de seguridad".
-- Si los datos de entrada no cumplen con las especificaciones, el sistema debe
-- fallar de forma segura (rechazar la inserción) en lugar de aceptar datos contaminados 
-- que arruinen los reportes posteriores. Esto es exactamente lo que hacemos en control de calidad industrial.