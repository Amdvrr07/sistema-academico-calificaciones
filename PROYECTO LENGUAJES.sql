CREATE TABLE IF NOT EXISTS cursos(
	curso_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	grado INT NOT NULL CHECK(grado>=1 AND grado <=5),
	seccion char NOT NULL CHECK(seccion IN ('A', 'B', 'C', 'D')),
	periodo_escolar varchar(10) NOT NULL CHECK(periodo_escolar ~'^\d{4}-\d{4}$'),
	CONSTRAINT curso_unico UNIQUE (grado, seccion, periodo_escolar)
);

CREATE TABLE IF NOT EXISTS roles(
	rol_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	codigo varchar(20) NOT NULL UNIQUE,
	nombre varchar(30) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS usuarios(
	usuario_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	nombre_usuario varchar(100) NOT NULL UNIQUE,
	correo varchar(100) NOT NULL UNIQUE,
	contrasenia varchar(255) NOT NULL,
	rol_id INT NOT NULL,
	fecha_creacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	CONSTRAINT fk_usuarios_rol 
	FOREIGN KEY (rol_id)
	REFERENCES roles(rol_id)
	ON DELETE RESTRICT
	ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS representantes (
	representante_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	nombre varchar(100) NOT NULL,
	cedula varchar(10) NOT NULL UNIQUE,
	correo varchar(100) NOT NULL UNIQUE,
	telefono varchar(20) NOT NULL,
	direccion varchar(200) NOT NULL
);

CREATE TABLE IF NOT EXISTS alumnos(
	alumno_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	nombre varchar(100) NOT NULL,
	cedula varchar(10) NOT NULL UNIQUE,
	fecha_nacimiento DATE NOT NULL,
	representante_id INT NOT NULL,
	CONSTRAINT fk_alumnos_representantes
		FOREIGN KEY(representante_id)
		REFERENCES representantes(representante_id)
		ON DELETE RESTRICT
		ON UPDATE CASCADE
);


CREATE TABLE IF NOT EXISTS materias(
	materia_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	nombre varchar(50) NOT NULL,
	codigo varchar(10) NOT NULL UNIQUE,
	grado INT NOT NULL CHECK(grado>=1 AND grado <=5),
	CONSTRAINT grado_nombre_unico UNIQUE (nombre, grado)
);

CREATE TABLE IF NOT EXISTS profesores(
	profesor_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	nombre varchar(100) NOT NULL,
	cedula varchar (10) UNIQUE NOT NULL,
	telefono varchar(20) NOT NULL,
	correo varchar(100) NOT NULL UNIQUE,
	especialidad varchar(20) NOT NULL,
	salario_base DECIMAL(8, 2) NOT NULL CHECK( salario_base >0),
	usuario_id INT NOT NULL UNIQUE,

	CONSTRAINT fk_profesores_usuario
	FOREIGN KEY (usuario_id)
	REFERENCES usuarios(usuario_id)
	ON DELETE RESTRICT
	ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS cobranzas(
	cobranza_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	concepto varchar(100) NOT NULL,
	fecha_vencimiento DATE NOT NULL,
	monto numeric(8,2) NOT NULL CHECK(monto >0),
	estado varchar(15) NOT NULL CHECK (estado IN ('pagado', 'por cobrar')),
	alumno_id INT NOT NULL,
	representante_id INT NOT NULL,
	
	CONSTRAINT fk_cobranzas_alumno
	FOREIGN KEY (alumno_id)
	REFERENCES alumnos(alumno_id)
	ON DELETE RESTRICT
	ON UPDATE CASCADE,
	
	CONSTRAINT fk_cobranzas_representante
	FOREIGN KEY (representante_id)
	REFERENCES representantes(representante_id)
	ON DELETE RESTRICT
	ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS pagos (
	pago_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	fecha_pago DATE NOT NULL DEFAULT CURRENT_DATE,
	concepto varchar(100) NOT NULL,
	monto decimal(8,2) NOT NULL CHECK(monto > 0),
	profesor_id INT NOT NULL,
	CONSTRAINT fk_pagos_profesor
	FOREIGN KEY (profesor_id)
	REFERENCES profesores(profesor_id)
	ON DELETE RESTRICT
	ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS profesores_cursos(
	profesor_id INT NOT NULL,
	materia_id INT NOT NULL,
	curso_id INT NOT NULL,
	CONSTRAINT pk_profesor_materia
	PRIMARY KEY (profesor_id, materia_id, curso_id),

	CONSTRAINT fk_profesores_cursos_profesor
	FOREIGN KEY (profesor_id)
	REFERENCES profesores(profesor_id)
	ON DELETE CASCADE
	ON UPDATE CASCADE,
	
	CONSTRAINT fk_profesores_cursos_materia
	FOREIGN KEY (materia_id)
	REFERENCES materias(materia_id)
	ON DELETE CASCADE
	ON UPDATE CASCADE,

	CONSTRAINT fk_profesores_cursos_curso
	FOREIGN KEY (curso_id)
	REFERENCES cursos(curso_id)
	ON DELETE CASCADE
	ON UPDATE CASCADE,

	CONSTRAINT materia_curso_unico
	UNIQUE (materia_id, curso_id)
);

CREATE TABLE IF NOT EXISTS inscripciones(
	inscripcion_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	alumno_id INT NOT NULL,
	materia_id INT NOT NULL,
	curso_id INT NOT NULL,

	CONSTRAINT inscripcion_unica
	UNIQUE(alumno_id, materia_id, curso_id),

	CONSTRAINT fk_inscripciones_alumno
	FOREIGN KEY (alumno_id)
	REFERENCES alumnos (alumno_id)
	ON DELETE RESTRICT
	ON UPDATE CASCADE,

	CONSTRAINT fk_inscripciones_materia
	FOREIGN KEY (materia_id)
	REFERENCES materias(materia_id)
	ON DELETE RESTRICT
	ON UPDATE CASCADE,
	

	CONSTRAINT fk_inscripciones_curso
	FOREIGN KEY (curso_id)
	REFERENCES cursos(curso_id)
	ON DELETE RESTRICT
	ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS notas (
	nota_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	inscripcion_id INT NOT NULL,
	fecha_registro TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	calificacion DECIMAL(4,2) NOT NULL CHECK(calificacion >= 0 AND calificacion <=20),
	lapso INT NOT NULL CHECK (lapso BETWEEN 1 AND 3),
	
	CONSTRAINT fk_notas_inscripcion
	FOREIGN KEY (inscripcion_id)
	REFERENCES inscripciones(inscripcion_id)
	ON DELETE CASCADE
	ON UPDATE CASCADE,
	
	CONSTRAINT nota_unica
	UNIQUE (inscripcion_id, lapso)
);

CREATE TABLE IF NOT EXISTS aulas(
	aula_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	codigo varchar(10) NOT NULL UNIQUE,
	ubicacion varchar(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS bloques(
	bloque_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	aula_id INT NOT NULL,
	materia_id INT NOT NULL,
	curso_id INT NOT NULL,
	profesor_id INT NOT NULL,
	dia varchar(10) NOT NULL CHECK (dia IN ('lunes', 'martes', 'miercoles', 'jueves', 'viernes')),
	hora_inicio time NOT NULL,
	hora_fin time NOT NULL,

	CONSTRAINT hora_valida CHECK (hora_fin > hora_inicio),

	CONSTRAINT fk_bloques_aula
	FOREIGN KEY (aula_id)
	REFERENCES aulas(aula_id)
	ON DELETE RESTRICT
	ON UPDATE CASCADE,

	CONSTRAINT fk_bloques_materia
	FOREIGN KEY (materia_id)
	REFERENCES materias(materia_id)
	ON DELETE RESTRICT
	ON UPDATE CASCADE,

	CONSTRAINT fk_bloques_curso
	FOREIGN KEY (curso_id)
	REFERENCES cursos(curso_id)
	ON DELETE RESTRICT
	ON UPDATE CASCADE,

	CONSTRAINT fk_bloques_profesores_curso
	FOREIGN KEY (profesor_id, materia_id, curso_id)
	REFERENCES profesores_cursos(profesor_id, materia_id, curso_id)
	ON DELETE RESTRICT
	ON UPDATE CASCADE
);


CREATE TABLE auditorias_notas(
	auditoria_nota_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	nota_id INT NOT NULL,
	usuario_id INT NOT NULL,
	fecha_cambio TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	calificacion_anterior DECIMAL(4,2) NOT NULL,
	calificacion_modificada DECIMAL(4,2) NOT NULL,

	CONSTRAINT fk_auditorias_notas_nota
	FOREIGN KEY (nota_id)
	REFERENCES notas(nota_id)
	ON DELETE RESTRICT 
	ON UPDATE CASCADE,

	CONSTRAINT fk_auditorias_notas_usuario 
	FOREIGN KEY (usuario_id)
	REFERENCES usuarios(usuario_id)
	ON DELETE RESTRICT
	ON UPDATE CASCADE
);


-- Creando Triggers

CREATE OR REPLACE FUNCTION revisar_disponibilidad_insert()
RETURNS TRIGGER AS $$
DECLARE 
	prof_ocupado BOOL;
	aula_ocupada BOOL;
	seccion_ocupada BOOL;
	periodo_actual varchar(10);
BEGIN
	SELECT periodo_escolar INTO periodo_actual 
	FROM cursos WHERE curso_id = NEW.curso_id;

	
	SELECT EXISTS (
		SELECT 1
		FROM bloques b 
		JOIN cursos c ON b.curso_id = c.curso_id
		WHERE LOWER(dia) = LOWER(NEW.dia)
		AND profesor_id = NEW.profesor_id
		AND c.periodo_escolar = periodo_actual
		AND hora_inicio < NEW.hora_fin AND NEW.hora_inicio < hora_fin
		) INTO prof_ocupado;

	SELECT EXISTS (
		SELECT 1 FROM bloques b
		JOIN cursos c ON b.curso_id = c.curso_id
		WHERE
			LOWER(dia) =LOWER(NEW.dia) AND
			aula_id = NEW.aula_id AND
			c.periodo_escolar = periodo_actual AND
			hora_inicio < NEW.hora_fin AND NEW.hora_inicio < hora_fin
	) INTO aula_ocupada;

	SELECT EXISTS (

		SELECT 1 FROM bloques
		WHERE
			LOWER(dia) = LOWER(NEW.dia) AND
			curso_id = NEW.curso_id AND
			hora_inicio < NEW.hora_fin AND NEW.hora_inicio < hora_fin
			
	) INTO seccion_ocupada;

	IF prof_ocupado THEN 
		RAISE EXCEPTION 'Operacion Cancelada: Ya el profesor % esta asignado a una clase entre la hora % y %', NEW.profesor_id, NEW.hora_inicio, NEW.hora_fin;
	END IF;

	IF aula_ocupada THEN 
		RAISE EXCEPTION 'Operacion Cancelada: Ya el aula % esta asignado a una clase entre la hora % y %', NEW.aula_id, NEW.hora_inicio, NEW.hora_fin;
	END IF;

	IF seccion_ocupada THEN 
		RAISE EXCEPTION 'Operacion Cancelada: Ya la seccion % tiene una clase asignada entre la hora % y %', NEW.curso_id, NEW.hora_inicio, NEW.hora_fin;
	END IF;

	RETURN NEW;
END;

$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_evitar_solapamiento_insert
BEFORE INSERT  ON bloques
FOR EACH ROW
EXECUTE FUNCTION revisar_disponibilidad_insert();


-- Trigger update
CREATE OR REPLACE FUNCTION revisar_disponibilidad_update()
RETURNS TRIGGER AS $$
DECLARE 
	prof_ocupado BOOL;
	aula_ocupada BOOL;
	seccion_ocupada BOOL;
	periodo_actual varchar(10);
BEGIN

	SELECT periodo_escolar INTO periodo_actual
	FROM cursos WHERE curso_id = NEW.curso_id;
	
	SELECT EXISTS (
		SELECT 1
		FROM bloques b
		JOIN cursos c ON b.curso_id = c.curso_id
		WHERE LOWER(dia) = LOWER(NEW.dia)
		AND profesor_id = NEW.profesor_id
		AND c.periodo_escolar = periodo_actual
		AND hora_inicio < NEW.hora_fin AND NEW.hora_inicio < hora_fin
		AND bloque_id <> NEW.bloque_id
		) INTO prof_ocupado;

	SELECT EXISTS (
		SELECT 1 FROM bloques b
		JOIN cursos c ON b.curso_id = c.curso_id
		WHERE
			LOWER(dia) = LOWER(NEW.dia) AND
			aula_id = NEW.aula_id AND
			c.periodo_escolar = periodo_actual AND
			hora_inicio < NEW.hora_fin AND NEW.hora_inicio < hora_fin
			AND bloque_id <> NEW.bloque_id
	) INTO aula_ocupada;

	SELECT EXISTS (

		SELECT 1 FROM bloques 
		WHERE
			LOWER(dia) = LOWER(NEW.dia) AND
			curso_id = NEW.curso_id AND 
			hora_inicio < NEW.hora_fin AND NEW.hora_inicio < hora_fin
			AND bloque_id <> NEW.bloque_id
			
	) INTO seccion_ocupada;

	IF prof_ocupado THEN 
		RAISE EXCEPTION 'Operacion Cancelada: Ya el profesor % esta asignado a una clase entre la hora % y %', NEW.profesor_id, NEW.hora_inicio, NEW.hora_fin;
	END IF;

	IF aula_ocupada THEN 
		RAISE EXCEPTION 'Operacion Cancelada: Ya el aula % esta asignado a una clase entre la hora % y %', NEW.aula_id, NEW.hora_inicio, NEW.hora_fin;
	END IF;

	IF seccion_ocupada THEN 
		RAISE EXCEPTION 'Operacion Cancelada: Ya la seccion % tiene una clase asignada entre la hora % y %', NEW.curso_id, NEW.hora_inicio, NEW.hora_fin;
	END IF;

	RETURN NEW;
END;

$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_evitar_solapamiento_update
BEFORE UPDATE  ON bloques
FOR EACH ROW
EXECUTE FUNCTION revisar_disponibilidad_update();

	
-- Creamos el trigger para validar el grado de la materia y el grado de un curso especifico

CREATE OR REPLACE FUNCTION validar_grado()
RETURNS TRIGGER AS $$
DECLARE 
	grado_materia INT;
	grado_tabla INT;
BEGIN 
	SELECT grado INTO grado_materia FROM materias WHERE materia_id = NEW.materia_id;

	SELECT grado INTO grado_tabla FROM cursos WHERE curso_id = NEW.curso_id;

	IF grado_materia IS DISTINCT FROM grado_tabla THEN
		RAISE EXCEPTION 'Operacion Cancelada: EL grado de la materia % no coincide con el grado del curso % ',
		grado_materia, grado_tabla;
	END IF;

	RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER validad_grado_profesores_cursos
BEFORE INSERT ON profesores_cursos
FOR EACH ROW
EXECUTE FUNCTION validar_grado();

CREATE TRIGGER validar_grado_bloques
BEFORE INSERT ON bloques
FOR EACH ROW
EXECUTE FUNCTION validar_grado();

CREATE TRIGGER validad_grado_inscripciones
BEFORE INSERT ON inscripciones
FOR EACH ROW 
EXECUTE FUNCTION validar_grado();

-- UPDATE
CREATE TRIGGER validad_grado_profesores_cursos_update
BEFORE UPDATE ON profesores_cursos
FOR EACH ROW
EXECUTE FUNCTION validar_grado();

CREATE TRIGGER validar_grado_bloques_update
BEFORE UPDATE ON bloques
FOR EACH ROW
EXECUTE FUNCTION validar_grado();

CREATE TRIGGER validad_grado_inscripciones_update
BEFORE UPDATE ON inscripciones
FOR EACH ROW 
EXECUTE FUNCTION validar_grado();


-- Trigger auditoria
-- application level audit logs postgresql

CREATE OR REPLACE FUNCTION crear_log_auditoria()
RETURNS TRIGGER AS $$
DECLARE 
	user_id INT;
BEGIN
	user_id := NULLIF(current_setting('app.current_user_id', TRUE), '')::INT;

	IF user_id IS NULL THEN
		RAISE EXCEPTION 'Operacion Cancela: Se necesita el ID de algun usuario para realizar la actualizacion';
	END IF;


	INSERT INTO auditorias_notas(nota_id, usuario_id, fecha_cambio, calificacion_anterior, calificacion_modificada)
		VALUES
		(
			OLD.nota_id,
			user_id,
			CURRENT_TIMESTAMP, 
			OLD.calificacion,
			NEW.calificacion
		);
		

	RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER actualizar_auditoria_notas
AFTER UPDATE ON notas
FOR EACH ROW
WHEN (OLD.calificacion IS DISTINCT FROM NEW.calificacion)
EXECUTE FUNCTION crear_log_auditoria();

