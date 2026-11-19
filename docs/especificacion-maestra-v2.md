# Especificación maestra --- IT Knowledge Map v2

**Estado:** borrador de especificación funcional y de producto\
**Versión:** 2.0\
**Fecha:** 17 de noviembre de 2026\
**Documento de referencia:** Especificación maestra de IT Knowledge Map
v1 (977 líneas)

------------------------------------------------------------------------

# 1. Contexto del proyecto

IT Knowledge Map cuenta con una primera versión cuyo resultado principal
es una base de conocimiento de ingeniería de software compuesta por más
de 250 conceptos.

Cada concepto dispone de documentación propia y forma parte de una
estructura conceptual interconectada. El trabajo de v1 se concentró en
investigar, contextualizar, documentar y relacionar esos conceptos con
profundidad universitaria y profesional.

La v2 parte de ese activo existente. No tiene como objetivo volver a
producir la Knowledge Base ni reemplazar el trabajo realizado en v1. Su
propósito es convertir el conocimiento y la documentación acumulados en
un producto digital público, navegable e interactivo.

El alcance incluye también la documentación del proceso de desarrollo:
cómo se investigaron los temas, qué decisiones se tomaron, qué
herramientas se utilizaron, qué problemas aparecieron y cómo evolucionó
el proyecto.

La especificación de v1 continúa siendo la referencia para comprender
los criterios de calidad, profundidad y organización de la Knowledge
Base. Este documento define el siguiente estadio del producto.

# 2. Objetivo general

Construir una plataforma web pública para explorar la base de
conocimiento de IT Knowledge Map y su proceso de desarrollo, mediante
una experiencia interactiva que permita:

-   explorar conceptos y áreas de ingeniería de software;
-   comprender las relaciones entre conceptos y el motivo de cada
    conexión;
-   consultar documentación y fuentes asociadas;
-   conocer cómo se desarrolló el proyecto y cómo se aplicaron
    determinados conocimientos;
-   realizar preguntas mediante un chatbot conectado con el contenido
    documentado;
-   recorrer el proyecto mediante distintas rutas de exploración.

La plataforma debe permitir que una persona comprenda tanto el
conocimiento organizado en el proyecto como el trabajo realizado para
construirlo.

# 3. Objetivos de producto

## 3.1. Exposición pública del proyecto

IT Knowledge Map debe poder presentarse públicamente mediante canales
como LinkedIn y GitHub.

La plataforma debe facilitar que una persona que llega por primera vez
pueda comprender qué es el proyecto, qué contiene, cómo se desarrolló y
qué puede explorar.

La experiencia pública debe permitir mostrar el trabajo realizado sin
depender de una explicación personal en cada visita.

## 3.2. Visibilidad profesional

El proyecto también funcionará como una muestra pública de capacidades
aplicadas al desarrollo de software.

La presentación debe permitir observar, a través del propio producto:

-   organización y modelado de conocimiento;
-   investigación y documentación técnica;
-   diseño de arquitectura y toma de decisiones;
-   automatización de procesos;
-   desarrollo de interfaces;
-   integración de servicios y modelos de IA;
-   construcción de herramientas interactivas.

Estas capacidades deben poder reconocerse en el producto y en la
documentación disponible. No se debe convertir la plataforma en una
lista de habilidades declaradas sin evidencia.

## 3.3. Aprendizaje y evolución técnica

La construcción de v2 también constituye una instancia de aprendizaje y
aplicación práctica.

Se busca trabajar especialmente sobre frontend, arquitectura de
software, visualización interactiva con Three.js y sistemas RAG. Estas
áreas representan intereses y objetivos de aprendizaje, pero no
determinan por sí solas la arquitectura final.

La implementación debe permitir comprender y documentar las decisiones
técnicas tomadas durante el desarrollo.

## 3.4. Continuidad de la Knowledge Base

La Knowledge Base existente debe conservar su estructura, profundidad y
criterios de calidad.

La nueva plataforma debe aprovechar el contenido disponible y facilitar
su exploración. No debe reemplazar las notas existentes por respuestas
generadas en tiempo real ni tratar el contenido como una colección de
textos independientes.

# 4. Activos principales del proyecto

La plataforma trabajará con dos conjuntos de información principales.
Deben poder explorarse por separado y también relacionarse cuando exista
una conexión documentada.

## 4.1. Knowledge Base

La Knowledge Base contiene los conceptos de ingeniería de software
desarrollados durante v1.

Incluye, según corresponda a cada concepto:

-   explicaciones y fundamentos;
-   propósito y funcionamiento;
-   contexto profesional;
-   relaciones con otros conceptos;
-   fuentes y documentación;
-   ejemplos y rutas de estudio;
-   información sobre actualidad y evolución.

La estructura existente debe ser considerada la fuente principal del
contenido conceptual del proyecto.

La v2 debe consumir y presentar esta información sin modificarla de
forma destructiva. Cualquier transformación o adaptación necesaria para
la plataforma deberá preservar la trazabilidad con el material original.

## 4.2. Development Journey

Development Journey reúne la documentación del proceso mediante el cual
se desarrolló IT Knowledge Map.

Puede incluir:

-   capturas de pantalla;
-   videos;
-   documentos y notas;
-   recursos guardados;
-   ideas y propuestas;
-   investigaciones;
-   decisiones de producto y arquitectura;
-   experimentos;
-   pruebas;
-   errores y problemas encontrados;
-   soluciones aplicadas;
-   herramientas utilizadas;
-   etapas y acontecimientos del desarrollo;
-   aprendizajes y aplicaciones prácticas.

El objetivo es que el visitante pueda conocer qué se hizo, cuándo se
hizo, por qué se hizo y cómo se llevó adelante.

No se debe asumir que todo el material existente está centralizado o
preparado para publicación. La ubicación, organización, inventario y
selección de estos recursos quedan pendientes de relevamiento.

## 4.3. Relación entre ambos activos

La Knowledge Base y Development Journey son secciones diferenciadas,
pero no deben funcionar como repositorios aislados.

Cuando un concepto de la Knowledge Base tenga una aplicación o
antecedente documentado en el desarrollo del proyecto, la plataforma
debe permitir acceder a ese contexto.

Ejemplo:

Un visitante consulta el concepto RAG. Además de comprender su
funcionamiento general, puede encontrar documentación sobre cómo se
investigó, evaluó o aplicó RAG dentro de IT Knowledge Map, siempre que
exista material suficiente para respaldar esa conexión.

La relación debe apoyarse en documentación existente. No se debe
presentar una asociación inferida por el modelo como si fuera un hecho
registrado del proyecto.

# 5. Experiencia general de usuario

## 5.1. Principio de navegación

La plataforma debe ofrecer distintos puntos de entrada. No se debe
imponer un único recorrido obligatorio para todos los visitantes.

Una persona puede llegar con objetivos diferentes: conocer el proyecto,
consultar un concepto, explorar el grafo, revisar el proceso de
desarrollo o realizar una pregunta.

La interfaz debe facilitar esas alternativas y mantener accesibles las
secciones principales.

## 5.2. Presentación del proyecto

La plataforma debe incluir una presentación breve que permita
comprender:

-   qué es IT Knowledge Map;
-   qué problema u objetivo aborda;
-   qué contiene;
-   cómo se organiza;
-   qué puede hacer el visitante dentro de la plataforma.

La presentación debe ser clara y suficiente para orientar a alguien que
no conoce el proyecto.

El formato visual y la secuencia concreta de esta presentación quedan
pendientes de diseño.

## 5.3. Exploración inicial

Debe existir una forma de obtener una primera impresión visual del
proyecto y de su estructura.

La exploración inicial puede permitir observar las áreas, los conceptos
y las conexiones principales, sin exigir que el visitante comprenda todo
el grafo desde el primer momento.

La visualización inicial debe facilitar el descubrimiento y ofrecer
accesos claros hacia las distintas secciones.

## 5.4. Recorridos guiados

La plataforma debe permitir ofrecer recorridos guiados para quienes
prefieran una introducción estructurada.

Como líneas iniciales de recorrido se consideran:

-   **Conocer el proyecto:** objetivos, alcance, estructura e historia.
-   **Explorar el conocimiento:** áreas, conceptos y relaciones.
-   **Conocer el desarrollo:** investigación, herramientas,
    automatización, arquitectura y decisiones.

Estos recorridos son propuestas de organización inicial. Su contenido,
duración y orden deberán definirse durante el diseño funcional.

El visitante también debe poder abandonar un recorrido y continuar
explorando libremente.

## 5.5. Acceso al chatbot

El chatbot debe estar disponible como una vía de consulta transversal a
la Knowledge Base y Development Journey.

Su presencia no debe reemplazar la navegación convencional ni
convertirse en la única forma de acceder a la información.

El visitante debe poder consultar directamente las secciones y utilizar
el chatbot cuando necesite una explicación, una relación o una
orientación adicional.

## 5.6. Onboarding

Se considera la posibilidad de incorporar una introducción interactiva
para nuevos visitantes.

No está decidido si será necesaria una experiencia de onboarding
independiente, ni qué elementos debería incluir. La presentación del
proyecto y los recorridos guiados deben evaluarse primero para evitar
introducir pasos redundantes.

# 6. Knowledge Graph

## 6.1. Objetivo

El grafo debe permitir explorar la estructura conceptual de la Knowledge
Base y comprender cómo se relacionan sus elementos.

La visualización actual de Obsidian sirve como punto de partida
conceptual, pero la experiencia de v2 debe incorporar información y
comportamientos que no están representados por una conexión visual
simple.

## 6.2. Nodos

Los nodos representan conceptos, áreas u otras unidades de información
que se definan para el modelo del grafo.

La selección de un nodo debe permitir acceder a su información
contextual y a la documentación correspondiente.

El contenido mostrado debe proceder de la Knowledge Base o de otra
fuente identificada. La interfaz no debe depender exclusivamente de una
explicación generada por el chatbot.

## 6.3. Relaciones como unidades de conocimiento

Una conexión entre dos nodos no debe limitarse a indicar que existe una
relación.

Cada relación relevante debe poder contar con una explicación propia que
describa su naturaleza y su función.

Por ejemplo, una conexión entre Frontend y Backend puede explicar cómo
se comunican, qué responsabilidades corresponden a cada lado y qué
conceptos intermedios intervienen, como HTTP, APIs, solicitudes y
respuestas.

Las relaciones pueden representar distintos tipos de vínculo, entre
ellos:

-   dependencia;
-   uso;
-   implementación;
-   comunicación;
-   complementariedad;
-   requisito previo;
-   especialización o abstracción;
-   aplicación práctica.

La clasificación definitiva de relaciones y su representación en los
datos quedan pendientes de diseño.

## 6.4. Selección de una relación

Cuando el visitante seleccione una conexión, la interfaz debe presentar
la explicación disponible para esa relación.

Cuando exista documentación asociada, también debe permitir profundizar
en:

-   conceptos involucrados;
-   documentación y fuentes;
-   ejemplos;
-   conceptos relacionados;
-   aplicaciones dentro del proyecto;
-   consultas adicionales al chatbot.

La explicación debe reutilizar el conocimiento documentado. El chatbot
puede ampliar la consulta, pero no debe reemplazar el contenido
registrado de la relación.

## 6.5. Visualización contextual

El grafo debe poder adaptar su presentación según el contexto de
exploración.

Ejemplo:

Si el visitante pregunta cómo se conecta Frontend con Backend, la
interfaz puede destacar esos nodos y mostrar las relaciones relevantes,
incluyendo los conceptos intermedios que correspondan.

El objetivo es facilitar la comprensión de una parte del mapa sin exigir
que el visitante interprete simultáneamente todos los nodos.

La selección de elementos relevantes debe basarse en relaciones
documentadas o en resultados identificados explícitamente como
inferidos.

## 6.6. Estado de exploración

Se acordó que la experiencia debe combinar una visualización general con
vistas contextuales.

El visitante debe poder:

-   volver al grafo general;
-   abrir una visualización contextual a partir de una consulta;
-   conservar visualizaciones exploradas anteriormente;
-   recuperar una vista anterior;
-   continuar navegando sin perder innecesariamente el contexto de
    exploración.

La forma concreta de almacenar y recuperar esos estados queda pendiente
de diseño técnico y de experiencia de usuario.

## 6.7. Visualización 2D y 3D

Se contempla investigar visualizaciones avanzadas y el uso de Three.js.

Sin embargo, no está decidido que el grafo deba ser completamente
tridimensional ni que Three.js deba utilizarse en toda la interfaz.

La elección deberá responder a la utilidad de la visualización, la
legibilidad, el rendimiento y la complejidad de interacción.

# 7. Development Journey

## 7.1. Objetivo de la sección

Development Journey debe contar con una sección propia y accesible desde
la navegación principal.

Su finalidad es presentar el proceso de desarrollo de IT Knowledge Map a
partir de material y acontecimientos documentados.

No debe limitarse a una cronología de publicaciones. Debe permitir
comprender las actividades, decisiones y resultados que dieron forma al
proyecto.

## 7.2. Formas de exploración

Se deberá evaluar si el contenido puede organizarse y consultarse por:

-   orden cronológico;
-   etapa del proyecto;
-   tema;
-   tecnología;
-   tipo de actividad;
-   decisión o problema;
-   relación con conceptos de la Knowledge Base.

La organización definitiva depende del inventario de material disponible
y del modelo de información que se defina.

## 7.3. Contenido de cada registro

Un registro de Development Journey podrá incluir, cuando exista
información suficiente:

-   título;
-   fecha o período;
-   contexto;
-   objetivo;
-   descripción de la actividad;
-   decisiones tomadas;
-   herramientas y tecnologías utilizadas;
-   problemas encontrados;
-   soluciones o resultados;
-   evidencias y archivos asociados;
-   conceptos de la Knowledge Base relacionados.

No todos los registros deben tener obligatoriamente todos estos campos.
La estructura debe adaptarse al tipo de material y evitar completar
información que no esté documentada.

## 7.4. Evidencias

Las capturas, videos, documentos y otros archivos pueden utilizarse como
evidencia del proceso.

La plataforma debe conservar la relación entre cada recurso y el
registro al que pertenece.

Antes de publicar un recurso deberá verificarse que puede compartirse y
que no expone información privada, credenciales, datos personales de
terceros u otro contenido que no corresponda hacer público.

## 7.5. Relación con la Knowledge Base

Cuando un registro del proceso esté vinculado con conceptos de la
Knowledge Base, ambas secciones deben ofrecer accesos cruzados.

Ejemplo:

Desde un concepto se puede acceder a su aplicación documentada en el
proyecto. Desde un registro del desarrollo se puede acceder a los
conceptos necesarios para comprender la tecnología o decisión
involucrada.

# 8. Chatbot del proyecto

## 8.1. Objetivo

El chatbot debe facilitar la consulta y exploración de IT Knowledge Map.

Puede responder preguntas generales de ingeniería de software y
preguntas específicas sobre el contenido del proyecto. Su función
principal es conectar ambas perspectivas cuando exista información
suficiente.

No debe comportarse como un asistente general sin límites temáticos.

## 8.2. Alcance temático

El chatbot está orientado a:

-   ingeniería de software;
-   conceptos y tecnologías relacionadas;
-   arquitectura y desarrollo de sistemas;
-   áreas incluidas en la Knowledge Base;
-   investigación y documentación técnica;
-   proceso de desarrollo de IT Knowledge Map;
-   decisiones, herramientas y experiencias documentadas del proyecto.

Las consultas claramente ajenas al proyecto y a la ingeniería de
software deben recibir una respuesta breve que explique el alcance del
chatbot y redirija al visitante hacia los temas que puede consultar.

No se debe utilizar el modelo para desarrollar conversaciones abiertas
sobre asuntos sin relación con el producto.

## 8.3. Fuentes de respuesta

El chatbot puede utilizar distintas clases de información. Debe
diferenciarlas en su funcionamiento y, cuando sea relevante para la
respuesta, también en la presentación al usuario.

### A. Knowledge Base

Información recuperada de los conceptos y documentos del proyecto.

### B. Development Journey

Información recuperada de registros, decisiones, evidencias y
documentación del proceso.

### C. Conocimiento general del modelo

Información general de ingeniería de software que el modelo pueda
aportar aunque no exista una nota específica en el proyecto.

### D. Relaciones documentadas

Relaciones que están registradas explícitamente en la Knowledge Base o
en los datos del proyecto.

### E. Relaciones inferidas

Asociaciones que el modelo propone a partir de conocimiento general o
del contexto, pero que no están documentadas como relaciones del
proyecto.

El chatbot no debe presentar una inferencia como una relación confirmada
de IT Knowledge Map.

## 8.4. Conexión entre conocimiento general y contenido del proyecto

Cuando un visitante consulte un concepto general, el chatbot debe
identificar si existen temas relacionados dentro de la Knowledge Base o
Development Journey.

Ejemplo:

El visitante pregunta qué es Docker. El chatbot puede explicar el
concepto y, si existen contenidos relacionados en el proyecto, ofrecer
acceso a virtualización, contenedores, entornos de desarrollo u otros
temas documentados.

La sugerencia debe mostrarse solamente cuando haya contenido relacionado
que pueda recuperarse.

## 8.5. Conexión con Development Journey

Cuando una consulta tenga relación con una aplicación documentada en el
proyecto, el chatbot debe poder ofrecer esa exploración.

Ejemplo:

El visitante pregunta qué es RAG. Si existe material pertinente en
Development Journey, el chatbot puede ofrecer conocer cómo se investigó
o aplicó RAG en IT Knowledge Map.

La formulación debe ajustarse al contenido disponible. Si la
documentación describe una implementación, debe hablar de la
implementación; si describe una investigación o evaluación, no debe
presentarla como una aplicación terminada.

Al aceptar la sugerencia, el visitante debe poder acceder al contexto,
objetivo, decisiones, herramientas, proceso, problemas y evidencias
disponibles.

## 8.6. Diferenciación de información y límites de conocimiento

Si el chatbot no encuentra documentación suficiente sobre un aspecto del
proyecto, debe indicarlo.

Puede aportar una explicación general cuando sea pertinente, pero debe
aclarar que esa explicación no proviene de documentación específica de
IT Knowledge Map.

No debe inventar:

-   decisiones del proyecto;
-   implementaciones;
-   resultados;
-   fechas;
-   experiencias;
-   relaciones documentadas;
-   archivos o evidencias;
-   herramientas que supuestamente se hayan utilizado.

Cuando la información no esté disponible, debe reconocerlo y, si es
posible, orientar al visitante hacia contenido relacionado que sí
exista.

## 8.7. Interacción con la interfaz

El chatbot debe poder conectar sus respuestas con la plataforma.

Según la consulta y el contenido recuperado, podrá:

-   destacar nodos y relaciones del grafo;
-   abrir conceptos;
-   mostrar registros de Development Journey;
-   presentar fuentes y documentación;
-   sugerir recorridos;
-   conservar o recuperar una visualización contextual.

Estas acciones deben responder al contenido de la conversación y a
elementos existentes en el sistema. No deben producir enlaces o destinos
inexistentes.

## 8.8. Contexto de conversación

El chatbot debe poder mantener el contexto necesario para que el
visitante realice preguntas de seguimiento sin tener que repetir toda la
consulta.

La cantidad de historial que se conserve, el mecanismo de persistencia y
la política de retención todavía no están definidos.

## 8.9. Identificación de respuestas

La interfaz deberá permitir distinguir, cuando sea necesario, si una
respuesta se basa en documentación del proyecto o en conocimiento
general del modelo.

También deberá poder indicar cuándo una relación está documentada y
cuándo es una asociación inferida.

El diseño visual de estas indicaciones queda pendiente.

# 9. Autenticación y acceso al chatbot

## 9.1. Requisito de autenticación

El chatbot no estará disponible para visitantes anónimos.

Para utilizarlo, el visitante deberá completar un registro breve
mediante Google OAuth.

La decisión busca reducir la fricción del registro sin tener que
desarrollar y administrar un sistema propio de contraseñas.

## 9.2. Alcance del registro

El flujo inicial previsto es:

1.  El visitante intenta utilizar el chatbot.
2.  La plataforma solicita iniciar sesión con Google.
3.  Una vez autenticado, el visitante puede comenzar a consultar.
4.  El backend identifica al usuario autenticado y aplica los controles
    de uso correspondientes.

El registro debe limitarse a la información necesaria para autenticar y
administrar el acceso.

Los datos exactos que se conservarán, la política de privacidad y el
tratamiento de la información de cuenta quedan pendientes de definición.

## 9.3. Límites de consumo

El acceso autenticado debe estar sujeto a límites de uso para controlar
el consumo de la API y prevenir abusos.

Se han considerado los siguientes mecanismos:

-   presupuesto de tokens por usuario y período;
-   límite de solicitudes;
-   límite de tokens de salida por respuesta;
-   límite de concurrencia;
-   intervalo mínimo entre solicitudes;
-   límite de longitud de mensajes;
-   controles adicionales por dirección IP;
-   restricciones para consultas fuera del alcance temático.

Los valores concretos, ventanas temporales y comportamiento al alcanzar
un límite todavía no están definidos.

## 9.4. Control de consultas fuera de tema

Se propuso permitir hasta dos interacciones abiertas fuera del alcance
temático antes de detener ese tipo de conversación y redirigir al
visitante.

Esta regla debe combinarse con controles de consumo. No reemplaza los
límites de tokens, solicitudes ni protección contra automatizaciones
abusivas.

La definición exacta de qué se considera una interacción fuera de tema y
cómo se contabiliza queda pendiente.

## 9.5. Límites por IP

Se contempla aplicar límites adicionales por IP.

La IP no debe ser el único identificador para controlar el consumo:
varias personas pueden compartir una dirección y una misma persona puede
cambiarla.

Por lo tanto, el control principal deberá asociarse a la identidad
autenticada, con controles por IP como medida complementaria.

# 10. Contenido público y criterios de publicación

La plataforma será pública, pero eso no significa que todo el material
acumulado durante el desarrollo deba publicarse automáticamente.

Antes de incorporar contenido de Development Journey se deberá
determinar si puede compartirse.

Se deben revisar especialmente:

-   datos personales;
-   credenciales, tokens y secretos;
-   información privada;
-   información de terceros;
-   contenido sujeto a licencias o restricciones de distribución;
-   material provisional que pueda inducir a conclusiones incorrectas;
-   capturas o videos que muestren información no destinada a
    publicación.

Se propuso trabajar con niveles de publicación ---por ejemplo, público,
seleccionado y privado---, pero la clasificación definitiva y sus reglas
todavía no están aprobadas.

La plataforma debe permitir seleccionar qué contenido se publica sin
obligar a exponer el repositorio completo de trabajo.

# 11. Identidad y presentación profesional

En esta etapa, el foco de la plataforma debe estar puesto en IT
Knowledge Map como proyecto.

No se incorporará inicialmente una sección independiente de perfil
personal o portfolio tradicional.

La participación del desarrollador podrá reconocerse a través de la
historia del proyecto, las decisiones documentadas, el proceso de
trabajo y las aplicaciones realizadas.

Una sección personal independiente podrá evaluarse en una fase
posterior, sin condicionar la estructura inicial de v2.

# 12. Arquitectura y tecnologías

## 12.1. Criterio general

La arquitectura debe responder a los requisitos funcionales y de
operación definidos en esta especificación.

No se deben considerar confirmadas las tecnologías mencionadas durante
las primeras conversaciones hasta que se evalúen sus ventajas,
limitaciones, costos y compatibilidad.

## 12.2. Alternativas consideradas

Hasta el momento se mencionaron como posibilidades:

-   React y Vite para el frontend;
-   Tailwind CSS para estilos;
-   Three.js para determinadas visualizaciones;
-   Python para componentes del backend;
-   una arquitectura RAG para recuperar contenido del proyecto;
-   Groq como proveedor de inferencia;
-   GPT-OSS 120B como modelo candidato;
-   Netlify como alternativa de hosting para el frontend.

Estas tecnologías son candidatas, no decisiones técnicas aprobadas.

## 12.3. Componentes que deberán diseñarse

La propuesta de arquitectura deberá contemplar, como mínimo:

-   frontend público;
-   backend y API;
-   autenticación con Google OAuth;
-   almacenamiento y recuperación de la Knowledge Base;
-   almacenamiento y recuperación de Development Journey;
-   sistema de indexación y recuperación para RAG;
-   integración con el proveedor de modelos;
-   persistencia de usuarios y controles de consumo;
-   gestión de archivos y evidencias;
-   visualización del grafo;
-   registro de errores y trazabilidad.

La distribución de responsabilidades entre servicios, los contratos de
datos y las tecnologías concretas quedan pendientes de diseño.

## 12.4. Separación de responsabilidades

La interfaz no debe asumir responsabilidades que corresponden al
backend, especialmente en autenticación, autorización, límites de
consumo, acceso a credenciales y comunicación con proveedores externos.

Las claves de API y otros secretos no deben exponerse en el frontend.

El diseño técnico deberá establecer límites claros entre presentación,
lógica de negocio, recuperación de información, persistencia e
integraciones externas.

## 12.5. Despliegue

La plataforma requerirá una estrategia de despliegue para frontend y
backend.

El proveedor de hosting del frontend y el entorno de ejecución del
backend todavía no están definidos.

La decisión deberá considerar disponibilidad, costos, límites gratuitos,
configuración de variables de entorno, almacenamiento, observabilidad y
mantenimiento.

# 13. Requisitos de datos e integración

La implementación deberá definir cómo se representan y conectan los
datos de:

-   conceptos;
-   áreas;
-   relaciones;
-   fuentes;
-   registros de Development Journey;
-   archivos y evidencias;
-   usuarios;
-   conversaciones;
-   límites y consumo.

Los identificadores deben permitir conectar los distintos componentes
sin depender de títulos visibles o rutas de archivos que puedan cambiar.

La relación entre el contenido original y su representación para la web
debe ser trazable.

La estrategia de importación, sincronización o generación de datos
derivados desde los archivos existentes queda pendiente de diseño.

# 14. Calidad, seguridad y operación

La plataforma debe diseñarse considerando su exposición pública.

Como mínimo, la propuesta técnica deberá contemplar:

-   protección de credenciales y secretos;
-   validación de entradas;
-   autenticación y autorización en backend;
-   límites de solicitudes y consumo;
-   manejo de errores de proveedores externos;
-   protección frente a abuso automatizado;
-   control de acceso a archivos;
-   tratamiento seguro de contenido recuperado;
-   registros operativos sin exponer información sensible;
-   comportamiento ante indisponibilidad del proveedor de modelos.

La información recuperada desde documentos y archivos debe tratarse como
contenido, no como instrucciones que puedan modificar las reglas del
sistema o las políticas del chatbot.

Los requisitos específicos de privacidad, retención de conversaciones y
tratamiento de datos deberán definirse antes de habilitar el servicio
públicamente.

# 15. Etapas de trabajo propuestas

Las etapas siguientes organizan el trabajo de definición e
implementación. No representan todavía un cronograma ni compromisos de
fechas.

## Etapa 1 --- Relevamiento y modelado de contenido

-   revisar la estructura actual de la Knowledge Base;
-   identificar el formato de las notas y sus relaciones;
-   localizar e inventariar el material de Development Journey;
-   identificar qué contenido puede publicarse;
-   definir los modelos de datos y sus identificadores.

## Etapa 2 --- Definición de arquitectura

-   comparar alternativas de frontend y backend;
-   definir los límites entre componentes;
-   diseñar autenticación;
-   diseñar almacenamiento y recuperación;
-   definir la estrategia RAG;
-   evaluar proveedores de inferencia y hosting;
-   establecer contratos de API y datos.

## Etapa 3 --- Experiencia base de la plataforma

-   implementar estructura general de navegación;
-   presentar el proyecto;
-   habilitar acceso a Knowledge Base;
-   habilitar acceso a Development Journey;
-   definir el diseño visual y responsive.

## Etapa 4 --- Exploración del conocimiento

-   representar áreas y conceptos;
-   incorporar relaciones explicadas;
-   implementar selección y detalle de nodos y relaciones;
-   implementar vistas contextuales;
-   permitir recuperar visualizaciones anteriores;
-   evaluar visualizaciones 2D y 3D.

## Etapa 5 --- Chatbot

-   implementar autenticación con Google;
-   integrar recuperación de Knowledge Base y Development Journey;
-   diferenciar contenido documentado y conocimiento general;
-   implementar conexiones entre respuestas y elementos de la interfaz;
-   aplicar límites de consumo;
-   incorporar controles temáticos y manejo de consultas no admitidas.

## Etapa 6 --- Validación y publicación

-   verificar contenido y enlaces;
-   revisar permisos y publicación de archivos;
-   probar autenticación y límites;
-   probar fallos de servicios externos;
-   evaluar rendimiento y accesibilidad;
-   documentar despliegue y mantenimiento.

El orden definitivo podrá ajustarse cuando se conozcan las dependencias
técnicas y el estado real de los materiales.

# 16. Criterios generales de aceptación

La plataforma no se considerará lista para publicación únicamente porque
la interfaz esté implementada o porque el chatbot responda preguntas.

La validación deberá comprobar, como mínimo, los siguientes aspectos.

## 16.1. Presentación y navegación

-   Una persona que no conoce el proyecto puede comprender su objetivo.
-   Las secciones principales son accesibles desde la navegación.
-   Existen alternativas para explorar libremente y mediante recorridos
    guiados.
-   El chatbot no es el único mecanismo de navegación.

## 16.2. Knowledge Base

-   Los conceptos se presentan a partir del contenido existente.
-   Las relaciones relevantes tienen una explicación accesible.
-   La selección de nodos y relaciones permite profundizar.
-   Las fuentes y documentos asociados pueden consultarse cuando estén
    disponibles.
-   La plataforma no altera ni reemplaza el contenido original de manera
    destructiva.

## 16.3. Development Journey

-   Existe una sección propia para explorar el proceso.
-   Los registros pueden relacionarse con evidencias y conceptos.
-   Las fechas y decisiones se presentan únicamente cuando están
    documentadas.
-   El contenido privado o no autorizado no queda expuesto.

## 16.4. Chatbot

-   Responde dentro del alcance temático establecido.
-   Puede consultar información de Knowledge Base y Development Journey.
-   Distingue información documentada de conocimiento general.
-   No presenta inferencias como relaciones confirmadas del proyecto.
-   Puede enlazar sus respuestas con elementos existentes de la
    plataforma.
-   Reconoce la falta de documentación cuando corresponde.
-   Aplica autenticación y límites de consumo.

## 16.5. Seguridad y operación

-   El chatbot no puede utilizarse sin autenticación.
-   Las credenciales no se exponen en el frontend.
-   Los límites de consumo se aplican desde el backend.
-   Los errores de servicios externos se manejan sin perder el control
    de la sesión.
-   Los recursos publicados respetan los criterios de acceso y
    publicación.

Los criterios específicos por funcionalidad deberán ampliarse durante el
diseño y la implementación.

# 17. Decisiones confirmadas

Esta sección registra decisiones tomadas durante la definición de v2.
Debe actualizarse cuando se aprueben nuevas decisiones.

1.  v2 será una plataforma web pública para explorar IT Knowledge Map.
2.  La Knowledge Base existente es un activo de v1 y debe conservarse.
3.  Development Journey tendrá una sección propia y accesible.
4.  Knowledge Base y Development Journey podrán explorarse de forma
    independiente y estarán conectadas cuando exista documentación que
    respalde la relación.
5.  El chatbot será transversal a ambas secciones.
6.  El chatbot podrá responder consultas generales de ingeniería de
    software y consultas basadas en el contenido del proyecto.
7.  El chatbot no será un asistente general: deberá mantenerse dentro
    del alcance de IT Knowledge Map y la ingeniería de software.
8.  El chatbot deberá distinguir contenido documentado, conocimiento
    general e inferencias.
9.  Las relaciones del grafo deberán contar con explicaciones propias;
    no serán únicamente conexiones visuales.
10. La visualización deberá admitir vistas contextuales y permitir
    recuperar exploraciones anteriores o volver al grafo general.
11. El chatbot requerirá autenticación para su uso.
12. El método inicial de autenticación elegido es Google OAuth.
13. El registro deberá ser breve y no requerir que el proyecto
    administre contraseñas propias.
14. El uso del chatbot estará sujeto a límites de consumo y controles
    contra abusos.
15. Los controles por IP serán complementarios y no el único mecanismo
    de identificación o limitación.
16. No se incorporará inicialmente una sección independiente de perfil
    personal o portfolio tradicional.
17. La especificación de v1 será la referencia de profundidad,
    estructura y criterios de calidad documental, pero v2 tendrá un
    alcance propio.

# 18. Decisiones pendientes

Los siguientes puntos requieren definición antes de cerrar el diseño
funcional o técnico correspondiente.

## 18.1. Contenido

-   ¿Dónde está almacenado el material de Development Journey?
-   ¿Qué cantidad y tipos de archivos existen?
-   ¿Qué material está listo para publicar y cuál necesita revisión?
-   ¿Qué política de clasificación se utilizará para contenido público,
    seleccionado y privado?
-   ¿Cómo se sincronizarán los cambios de la Knowledge Base con la
    plataforma?

## 18.2. Experiencia de usuario

-   ¿Cuál será la estructura definitiva de navegación?
-   ¿Qué contenido se mostrará en la primera pantalla?
-   ¿Cómo se presentará visualmente el proyecto?
-   ¿Qué recorridos guiados se implementarán inicialmente?
-   ¿Será necesario un onboarding independiente?
-   ¿Cómo se organizará Development Journey: cronológicamente, por tema,
    por etapa o mediante una combinación?
-   ¿Qué información aparecerá al seleccionar un nodo o una relación?

## 18.3. Grafo

-   ¿Qué tipos de nodos y relaciones se soportarán?
-   ¿Cómo se almacenarán las explicaciones de las relaciones?
-   ¿Qué vistas contextuales se necesitan?
-   ¿Cómo se conservarán y recuperarán los estados de exploración?
-   ¿Qué partes se representarán en 2D o 3D?
-   ¿En qué casos se justifica utilizar Three.js?

## 18.4. Chatbot

-   ¿Se conservará el historial de conversaciones entre visitas?
-   ¿Durante cuánto tiempo se conservarán las conversaciones?
-   ¿Qué información de la cuenta se almacenará?
-   ¿Cómo se presentará la procedencia de las respuestas?
-   ¿Cómo se contabilizarán las dos interacciones abiertas fuera de tema
    propuestas?
-   ¿Qué mensaje y comportamiento se utilizarán al alcanzar los límites?
-   ¿Qué modelo y proveedor se utilizarán finalmente?
-   ¿Qué estrategia RAG y de indexación se implementará?

## 18.5. Arquitectura y operación

-   ¿Se utilizará React con Vite?
-   ¿Se utilizará Tailwind CSS?
-   ¿Qué responsabilidades tendrá el backend en Python?
-   ¿Qué base de datos y almacenamiento se utilizarán?
-   ¿Cómo se representará y consultará el grafo?
-   ¿Qué proveedor alojará el frontend y cuál el backend?
-   ¿Qué costos y límites operativos tendrá la solución?
-   ¿Qué mecanismos de logging, monitoreo y recuperación se necesitan?

Las alternativas mencionadas en conversaciones o propuestas no deben
tratarse como decisiones aprobadas hasta que se registren expresamente
en esta sección de decisiones confirmadas.

# 19. Criterios para tomar decisiones durante v2

Las decisiones de producto y arquitectura deberán evaluarse en función
de:

1.  cumplimiento de los objetivos de IT Knowledge Map;
2.  integridad y trazabilidad del conocimiento;
3.  utilidad para la exploración y comprensión del contenido;
4.  claridad de la experiencia de usuario;
5.  seguridad y control de acceso;
6.  viabilidad técnica;
7.  costos de desarrollo y operación;
8.  facilidad de mantenimiento y evolución.

Una tecnología no debe incorporarse solamente por ser nueva o porque
permita construir una visualización atractiva. Debe resolver una
necesidad identificada del producto.

Del mismo modo, no se debe descartar una funcionalidad relevante
únicamente porque requiera mayor complejidad. Si su implementación
presenta dificultades, deberán documentarse las alternativas y sus
consecuencias.

# 20. Instrucciones para el diseño e implementación

Esta especificación define objetivos, reglas de negocio y requisitos de
producto. No pretende reemplazar el diseño técnico detallado.

Antes de implementar cada componente, se deberá:

1.  identificar los requisitos que debe satisfacer;
2.  relevar los datos disponibles;
3.  definir contratos e interfaces;
4.  identificar dependencias;
5.  evaluar alternativas técnicas;
6.  registrar la decisión y sus motivos;
7.  definir criterios de aceptación;
8.  implementar;
9.  validar el comportamiento;
10. documentar limitaciones y decisiones relevantes.

Cuando una condición de esta especificación no pueda implementarse como
está planteada, se deberá explicar la limitación y proponer
alternativas. No se debe eliminar ni modificar un requisito de negocio
de manera silenciosa.

La implementación debe mantener una separación clara entre contenido
documentado, datos derivados, conocimiento generado por el modelo y
comportamiento de la interfaz.

# 21. Criterio documental

Este documento debe mantenerse como especificación de producto y no
convertirse en una conversación acumulada.

Por lo tanto:

-   registrar decisiones y requisitos, no el intercambio que llevó a
    ellos;
-   eliminar repeticiones cuando una regla ya esté definida en otra
    sección;
-   utilizar ejemplos cuando aclaren un comportamiento o una condición;
-   distinguir decisiones confirmadas de propuestas y pendientes;
-   no incorporar frases retóricas que no agreguen una condición,
    explicación o criterio;
-   no presentar como definitivo aquello que todavía está en evaluación;
-   actualizar las secciones afectadas cuando una decisión cambie.

El lenguaje debe ser directo y funcional. Cada sección debe permitir
comprender una parte del producto o establecer cómo debe comportarse.

# 22. Principio general de v2

IT Knowledge Map v2 debe convertir el conocimiento y la documentación
acumulados en una plataforma que permita explorar conceptos, comprender
sus relaciones y conocer el proceso mediante el cual se construyó el
proyecto.

La plataforma debe mantener la distinción entre lo que está documentado,
lo que puede explicarse desde conocimiento general y lo que todavía no
se ha investigado o registrado.

La calidad del producto dependerá de que la información pueda
encontrarse, comprenderse, relacionarse y verificarse, y de que la
experiencia permita recorrer el proyecto sin perder el contexto de cada
contenido.