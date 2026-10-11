
# LA CONSTITUCIÓN DEMOCRÁTICA

**Parte 2: Argumentación y Filosofía**

**El por qué de cada decisión**

---

# INTRODUCCIÓN: FILOSOFÍA DE DISEÑO

## El problema que resuelve esta Constitución

La mayoría de las "democracias" actuales son oligarquías electivas disfrazadas de democracias. La apariencia existe: elecciones periódicas, parlamento, separación de funciones que pretende ser de poderes. El fondo no: los partidos controlan fuertemente o completamente la selección de candidatos, la financiación y los medios. En el peor de los casos, estos son controlados por grandes capitales extranjeros, privados o estatales, foráneos a la nación. El resultado es una ilusión de elección gestionada por élites que lleva a paises a realizar decisiones que claramente van en contra del propio interés de su pueblo, iniciar guerras innecesarias por ejemplo. Esto pasa porque no siempre se alinean los deseos de la élite con los de la población.

¿Acaso esto es bueno? ¿Acaso es malo? Lo analizaré más adelante. Lo que si que es es evitable, adoptando sistemas realmente democráticos que den al pueblo una capacidad mucho más real de decisión y acción.

Las constituciones actuales son muchas y diversas: cada país tiene la suya, con sus propios principios, historia y compromisos. Intentar reformarlas una a una sería un esfuerzo titánico e interminable. Pero las dinámicas de poder no entienden de culturas específicas. La tendencia a concentrar poder, a corromper instituciones, a capturar mecanismos de control es una constante humana, no cultural. Aquí es cuando se me ocurrió que, si el problema es universal, la solución también debería serlo. Esta Constitución busca ser esa solución: un marco de referencia agnóstico, en el sentido de adaptable, a cualquier contexto histórico-cultural, basado únicamente en cómo funciona el poder entre seres humanos. Para que, si un pueblo lo desee, empiece a transicionar hacia unas dinámicas de poder realmente democráticas.

## Diseño con mentalidad defensiva

Esta Constitución no asume la buena voluntad. Asume el peor caso: un actor con recursos ilimitados intentando capturar el sistema. Cada mecanismo está diseñado para que ese peor caso sea lo más caro, difícil y arriesgado posible. Esta obra se puede entender como el resultado de una auditoría de seguridad sobre el concepto, sobre el código, de la democracia.

El diseño ha sido creado utilizando la mentalidad de un hacker de sombrero blanco, es decir, preguntando "¿cómo podría romperse esto? ¿si se rompe, cómo minimizamos el daño y cómo lo reparamos lo mejor y más rápido posible?". Cada mecanismo se somete a las preguntas: ¿cuál es el vector de ataque? ¿Cuánto cuesta aprovecharlo? ¿Cómo se detecta el abuso ó el ataque?

El ejemplo más claro de esto reside en el AOCD (Algoritmo de Optimización del Coste de Corrupción de Distritos). Donde se utiliza una medida objetiva aproximada para elevar el coste de corromper el resultado en las elecciones distritales de los representantes. Como el percentil 25 de renta (P25) de la población con capacidad de acción.

Un principio general derivado de esta mentalidad es abstraerse del moralismo. Asumir que si algo puede ir mal, en algún momento, irá mal. El diseño debe maximizar ese precio a pagar por intentar romper el sistema fuera de las normas marcadas. No se moraliza sobre si la gente se corrompe o no; se asume que puede ser comprada y se diseña para que el coste de comprarla sea lo más alto posible dentro de los límites naturales y sociales del ser humano.

## Influencias teóricas conscientes

Cualquier coincidencia entre los principios de esta Constitución y los de otros pensadores no mencionados aquí es exactamente eso: coincidencia. Mis disculpas si no los he nombrado, simplemente no soy consciente de ellos.

- Antonio García Trevijano: distritos uninominales, doble vuelta, revocabilidad, autodestrucción mutua, diversos límites a la financiación de partidos. Esta Constitución adopta en gran medida su marco y añade detalles específicos para completarlo.

- Robert Michels: Ley de Hierro de las Oligarquías. Toda organización tiende a concentrar el poder. Se diseña contra esto. Por ejemplo con mecanismos como poner límite al ritmo al que se crean las leyes, es decir, la burocracia, es decir, una de las razones fundamentales que llevan a la necesidad de una oligarquía de especialistas burocráticos. // TODO: revisar y releer a robert para añadir más detalle

- Diseño de sistemas descentralizados: el autor es ingeniero de software y hacker de blockchain. La mentalidad de diseño de esta Constitución proviene en gran medida de la ingeniería de sistemas distribuidos y resistentes a ataques: tolerancia a fallos bizantinos (el sistema funciona aunque algunos participantes sean maliciosos), eliminación de puntos únicos de fallo (ningún órgano concentra todo el poder), mecanismos de consenso con umbrales variables (los niveles N1-N6), auditoría pública y verificabilidad (transparencia presupuestaria, voto verificable), e inmutabilidad probabilística de reglas fundamentales. Además, ciertas ideas de sistemas operativos como un proceso de arranque (bootstrap) también provienen de esta influencia.

- Alegrismo (Cheerfulism): obra filosífica y de análisis de la existencia humana propia del autor. Su tesis central es que la felicidad es el motor y objetivo más profundo del comportamiento humano una vez la supervivencia está asegurada. Las siguientes ideas de la complejidad siempre creciente de la sabiduría humana, y la conclusión de que la democracia es el destino natural de las dinámicas de poder en civilizaciones prósperas provienen de esta obra.

---
---

# QUÉ ES DEMOCRACIA Y POR QUÉ UNA DEMOCRACIA

Antes de entrar a explicar cada decisión de diseño de esta Constitución, conviene que el lector y el escritor compartamos un mismo punto de partida: qué entendemos por democracia, por qué apostar por ella y cuáles son sus límites reales.

## Definición

La palabra democracia viene del griego: demos (pueblo) y kratos (poder). Poder del pueblo. Pero esta etimología es insuficiente como definición operativa. "El poder reside en el pueblo" es una declaración bonita que no dice nada sobre cómo funciona exactamente el sistema.

Es más, por motivos tan fundamentales como la física que explicaré más adelante, la democracia perfecta, aquella en la que todo el poder reside en el pueblo, no existe. En realidad, lo que existe es la cualidad de lo democrático, es decir, cuan democrático un sistema es, es decir, una medida o estimación referente a cuanto poder ostenta el pueblo.

Contra menos poder ostenta el pueblo, o de la misma forma, contra más poder ostenta una minoría, menos democrático el sistema es, tras traspasar cierto umbral, se convierte en oligarquía, y tras transpasar otro umbral, en dictadura.

La definición clara y precisa de estos umbrales es muy debatida. En mi caso, he llegado a concluir que estos son los tres umbrales los cuales deben cumplirse para empezar a considerar y llamar a un sistema una democracia:

// TODO: habia un error en mi pensamiento, la estrucutra interna predeterminada si importa, la de financiación. Seguramente esto esté mal explicado en Alegrismo. Y quizá en alguna parte de aquí más abajo. Also, lo de pacíficamente... No es necesario pero si útil. quiza añadirlo a alegrismo tambien y ver que pongo aqui al respecto. quiza una: nota curiosa.

**1. Competencia abierta por el poder.** Cualquier ciudadano ó grupo de ciudadanos, por el mero hecho de serlo, puede organizarse pacíficamente para aspirar a gestionar el Estado. Sin necesitar la aprobación de los grupos existentes. Sin embargo, si debe seguir las normas de financiación y publicidad democráticas, ya que sin ellas, la competencia en la práctica solo estaría abierta a los grupos con mayor riqueza, eventualmente creando una oligarquía. Estas normas se encuentran en el Artículo 17. Esto aspira a crear un entorno análogo a la idea que genera prosperidad a base de competencia perfecta en economía: que cualquiera que sepa fabricar un producto mejor pueda acceder a los medios para crearlo. En la democracia ideal, cualquiera que tenga una visión para su sociedad puede crear un grupo para reflejarla y mostrarla a sus vecinos en la mayor igualdad de condiciones posible.

**2. Separación real de poderes.** El Estado tiene tres funciones naturales: legislar (crear las reglas), ejecutar (aplicarlas) y juzgar (resolver conflictos cuando las reglas se incumplen). En democracia, estas tres funciones son ejercidas por órganos independientes entre sí, con independencia de nombramiento y de financiación. Sin esta separación, la democracia, otra vez, colapsa en oligarquía: un grupo que legisla, ejecuta y juzga simultáneamente no tiene casi límites a lo que puede hacer. Quizá colapse en una oligarquía plutocrática ("los ricos mandan"), o tecnocrática ("los expertos mandan"), o ambas a la vez; independientemente del sistema en el que colapse, oligarquía o incluso dictadura; sin este requisito, la democracia acaba colapsando.
// TODO: dar un poco más de detalle de como. Creo que venia de: "El ser humano solo se mueve ante la adversidad, tendencia a la vagueria, y si alguien puede, sera vago, cada vez mas, a no ser que haya una fuerza que se lo impida." (en tendencia, simepre existe sin embargo un pequeño grupo de curiosos aburridos que se mueven por curiosidad, pues el aburrimiento es doloroso) Ademas, se tapan los unos a los otros etc. ademas cambiar titulo: (a nivel fundamental), en su fundamento, quien los crea nombra y como comen, dinero.

**3. Representación real con rendición de cuentas.** En sociedades grandes, la democracia directa es inviable para la gestión diaria. Se necesitan representantes debido a los límites físicos y cognitivos del ser humano. Sin embargo, la representación solo es democrática si cumple dos condiciones: que el representante sea elegido directamente por una comunidad lo suficientemente pequeña como para conocerle (distritos uninominales), y que esa comunidad pueda despedirle en cualquier momento si no cumple (revocabilidad). Sin estas dos condiciones, el representante acaba sirviendo al partido que le puso en la lista ó al mejor postor, no al ciudadano que le votó. Pues el poder sería completamente transferido y no delegado, extrayendo así el kratos (poder) del demos (pueblo). No ostentas poder sobre aquello que no puedes afectar en un tiempo razonable, aquello que no puedes alcanzar. Un mero humano desnudo no tiene poder sobre la nube encima de su cabeza, porque no la puede alcanzar de forma inmediata.

Cuando estos tres puntos se cumplen, entonces, considero que el sistema ha pasado el umbra a partir del cual algo se puede considerar democrático.

// TODO: esto es mas un argumento de porque la definición de democracia requiere separación de poders más que un argumento a favor de querer una democracia. Quizá añadir más arriba: La separación de poderes previene la deriva natural hacia la tiranía
Sin separación de poderes, un grupo elegido democráticamente que controle todo el Estado acabará, por tendencia natural, modificando las reglas para mantenerse en el poder. No necesariamente por maldad, sino por incentivos: quien tiene el poder de cambiar las reglas y el incentivo de conservar el poder, acabará cambiando las reglas a su favor. La separación de poderes rompe ese ciclo: quien hace las leyes no las ejecuta ni las interpreta, quien las ejecuta ni juzga si se cumplen ni las crea, y quien juzga ni las escribe ni las hace.

## El trilema democrático

Durante la lectura de esta Constitución seguramente hayas notado que algunas reglas no son todo lo democráticas que podrían ser. Como ya he mencionado, la democracia es un punto que determina un umbral en un espectro, y una vez dadas las tres condiciones de arriba, el resto de decisiones, podrán ser más o menos democrácticas, pero democráticas serán.

Esto proviene de los límites físicos de nuestra existencia. Análogo al trilema de blockchain (descentralización, seguridad, escalabilidad), la democracia enfrenta: Descentralización ↔ Estabilidad ↔ Eficiencia. No se pueden maximizar las tres.

La descentralización hace referencia a cuanto el pueblo puede influir y ejercer su voluntad. Es decir, en cuantas cuestiones puede influir y cuan relevantes estas son.

La estabilidad hace referencia a cuanto el sistema es capaz de procesar cambios internos sin romperse, ya sea porque el sistema desaparezca ó sea disfuncional. Con desaparecer me refiero a degradarse a una oligarquía u otro sistema más centralizado. Y en cuanto a disfuncional me refiero a que, si la ley cambiara a cada hora, aún por muy democrático que haya sido el medio para lograr tal hecho, el sistema se rompería pues un ser humano no puede estar adaptando su comportamiento de manera tan fundamental a cada hora, se volvería loco.

Y la eficiencia hace referencia a cuanto el sistema puede tomar decisiones rápidas y efectivas. La eficiencia del cambio es un arma de doble filo, es preferible que los cambios que sí sean democráticos ó deseados ocurran lo más rápido posible, sin embargo, estos mismos mecanismos también, fácilmente, pueden abrir las puertas a que aquellos cambios que no sean democráticos ó deseados ocurran.

Si maximizas eficiencia, te cargas la estabilidad del sistema pues primero habrían muchos cambios, y segundo, un atacante podría aprovechar la confusión de la velicidad para poco a poco integrar cambios maliciosos en el sistema.

Si maximizas estabilidad el sistema colapsaría a medio y largo plazo pues no sería capaz de adaptarse en el día a día a los cambios que siempre acaban ocurriendo en la sociedad, ya sean morales ó tecnológicos. Una alta estabilidad requiere forzosamente de una baja eficiencia.

Si maximizas descentralización, el caos sería tal que cualquier decisión no unánime no se llevaría a cabo, cargándote la estabilidad.

Las razones fundamentales detrás de estos límites son las siguientes.

La primera razón, aumentar el grado de democracia también aumenta la carga cognitiva del miembro del grupo, pues este ya no solo tendrá que preocuparse de su vida individual sino también de cuestiones extras relacionadas a las cuestiones de organizar el grupo, la burocracia. Y, en la práctica, tenemos un limitado "ancho de banda" cerebral, por lo que, tenemos un límite sobre la cantidad de decisiones en las que podemos físicamente participar en el día a día. Fijando esto cuan eficiente y estable nuestro sistema social puede llegar a ser.
// TODO: añadir quiza aqui una referencia a como la complejidad de la sociedad humana no escala linear al numero de individuos?

La segunda es que en situaciones dinámicas y complejas, como la interacción en casos de conflicto con otros grupos, que un grupo tenga la capacidad de tomar acción rápidamente es crucial. Para ello es requerido el mando por parte de un solo individuo, o del menor número de individuos posible. Ya que las discrepancias internas, ó simplemente el tiempo que se tarda en comunicar información para tomar la decisión, incluso si se está de acuerdo en cual debería ser esa decisión, es fricción y retardo de acción que el otro grupo puede, teórica y prácticamente aprovechar. De aquí proviene la necesidad de la centralización. Se podría argumentar que, si no hubiera conflicto, no haría falta tanta centralización, por ende la razón fundamental detrás de la necesidad de centralización es el conflicto, y sería correcto, ahora, no sería realista, no solo por conflictos surgen estructuras organizativas centralizadas. Pero esto es un tema bastante profundo y fuera del objetivo texto. Con conflicto no me refiero solo a guerras ó matanzas, sino a simplemente, resoluciones a cuestiones más calmadas pero complejas como: "Como fomentamos nuestra agricultura local frente a la de los vecinos".

Son con estos límites del manejo de la información del ser humano que debemos distanciarnos del mundo de las ideas y con los cuales debemos aceptar que la democracia ideal y perfecta nunca será. Lo mejor que podemos hacer, es ir ajustando el sistema para que, poco a poco, a medida que unos nacen y otros mueren, aprovechemos nuestras dotes cognitivas de la manera más democrática posible.

## Argumentos a favor y en contra de la democracia

Ahora que ya estamos en la misma página y ya sabemos como entiendo y defino el concepto de democracia, tanto en sus límites reales como ideales que la restringen y por tanto definen. Toca entender si esa cosa, ese método, ese protocolo, esa idea, es buena ó mala.

### A favor

#### 1.- La democracia produce un bucle de retroalimentación más rico

Todo progreso humano se basa en bucles de retroalimentación: actuar, observar el resultado, corregir, volver a actuar. Aprendemos así. La ciencia funciona así por ejemplo.

En una dictadura, el bucle de retroalimentación es pobre: una persona decide, y la información sobre si esa decisión fue buena o mala llega filtrada, tarde y distorsionada, por dinámicas sociales inevitables como el miedo a represalias ó el peloteo ávaro.

En una oligarquía, el bucle es algo más rico pero sigue limitado a las mismas dinámicas sociales humanas nombradas.

En democracia, el bucle incluye a toda la sociedad, bueno, a aquellos con derecho a voto: "millones", bueno muchas, personas evaluando decisiones, proponiendo alternativas, corrigiendo errores. Cuantas más perspectivas diversas participan en el bucle, mejor se puede entender la realidad y mejor se puede llegar a responder a ella.

A largo plazo no solo importa encontrar la solución correcta pero también haber contemplado la mayor cantidad de soluciones incorrectas posibles antes de llegar a la correcta, claro esta, sin sacrificar la llegada a esta. Con esto quiero decir que está muy bien plantearse alternativas, pero el tiempo es limitado y no podemos estar todo el rato pensando, ó preguntando cada vez a más y más personas antes de tomar una decisión. Hay un límite físico que nos impone un techo a la hora de intentar maximizar el número de perspectivas que se pueden llegar a tener en cuenta.

Ignorando, de momento, estos límites físicos, la forma más simple de entender este argumento es: "Para solucionar un problema es mejor preguntar a cien personas en vez de diez". Por pura probabilidad, asumiendo que todas son igualmente inteligentes, es mejor preguntar a las cien si queremos encontrar la respuesta.

Este argumento es simplista, pero sirve para empezar a divisar las razones que hacen de la democracia un sistema deseable. Las simplificaciones de este argumento ya han sido nombradas: la imposibilidad física de poder preguntar a todos, sí, puedes preguntar a cien personas, pero buena suerte preguntando a diez millones. Y la asunción de que todas las voces son igual de inteligentes, que no lo son. Ahora, si conseguimos encontrar formas ingeniosas para que estas restricciones afecten lo menos posible al funcionamiento del sistema democrático, entonces, la democracia es claramente superior en tanto en cuanto es capaz de procesar la realidad de una forma más completa, rica, y por tanto, adecuada.

Aparte de que el factor de la diversidad puede llevarnos a una adaptación más rica a la realidad, en democracia existe una revocabilidad mucho más rápida que en oligarquías y dictaduras. Pues, si un elemento del sistema, digamos un diputado de distrito, incumple y deja de representar las necesidades y deseos reales de su distrito, este puede ser revocado casi inmediatamente por otro que sí lo haga. De esta manera, el proceso de adaptación no solo es más rico, sino también más flexible y dinámico, permitiendo adaptarse más rápidamente a las nuevas circumstancias de la sociedad ya sean traidas por avances tecnológicos, cambios morales, u otros.

Por estos dos motivos, y bajo los límites explicados, la democracia es un sistema que permite un bucle de retroalimentación más rico, en el sentido de diverso y flexible, que nos permite adaptarnos mejor a la realidad, y con ello, resolver mejor los problemas que vayan surgiendo.  

// TODO: revisar esta imagen mental, dinamicas explicadas arribas es probabilidad de "corromper" el mensajem contra más plana sea la piramide mejor, pero, hay un límite de planitud creado por nuestros límites biologicos, no podemos tener 1 lider y todos seguidores, se necesitan niveles intermedios, burocracia. Pero contra menos mejor por cuestiones de probabilidad de error estructural. 2.- luego hay cuestiones de probabilidad de error indivdual, actitud, fuentes de abuso etc. 3.- Entonces esto no tiene que ver con este argumento, pero seguramente si con otro. Pues, lo que crea el error es la dinamica hunmana, la altura de la piramide solo aumenta las veces en las que se crea un escenario en el que el error se puede manifestar.

// TODO: más rico == más honesto. Más honesto quiere decir con mayor visibilidad, pero no necesiariemnte se puede asegurar la acción en esa dirreción. ¿Queremos más visibilidad? ¿Ó preferimos visibilidad de distancia reducida pero de mayor calidad? (Debate de tecnocracia vs democracia, contestado abajo)

// TODO: esto estaba aquí pero en otra sección, lol, no se pq, es lo mismo, incluir en lo anterior ó hacer 2 secciones si al final lo requiere, creo que es más probable que haya que incluir.
Todo sistema de poder replica este mecanismo pero en la escala social: las leyes son las variables fijas (estabilidad y previsibilidad) y los mecanismos de cambio político son las variables libres (adaptación). Esto es así en dictaduras, oligarquías y democracias por igual. La diferencia es la riqueza con la que cada sistema permite ejercer la parte dinámica.

#### 2.- La descentralización minimiza el impacto del abuso

Esta cualidad, en sistemas informáticos, y en sistemas ingenieriles en general es conocida como: tolerancia al fallo.

Todo poder, dado el tiempo suficiente, tiende al abuso. Esta es una observación empírica constante a lo largo de la historia humana. La pregunta no es "¿abusarán?" sino "¿cuánto daño pueden hacer cuando abusen, y cómo minimizar el daño hecho y repararlo lo mejor posible si consiguen abusar?".

La respuesta depende de cuánto poder concentra cada individuo. En una dictadura, un solo individuo concentra todo el poder, por tanto el daño potencial que puede hacer es máximo. En democracia, el poder está distribuido entre muchos actores independientes: legisladores de distrito, un poder ejecutivo independiente, un poder judicial independiente, y un pueblo con capacidad de intervención directa y ágil. El daño que puede hacer cualquier actor individual o grupo es limitado por los demás. No se elimina el abuso, el abuso es un fenómeno natural humano; "simplemente" se minimiza su alcance e impacto de forma sistemática.

Cuando, digamos por ejemplo, en una red de ordenadores, hay tres ordenadores y falla uno, la red está bastante en peligro pues un 33% de ella está destruida. Sin embargo, si en la red participan miles de ordenadores, incluso si tres de ellos fallan, el impacto es mínimo.

Imagina una base de datos descentralizada, popularmente conocidas a día de hoy como blockchains, si una muy grande, digamos Bitcoin, que tiene miles de operadores alrededor del mundo, fallan cien, el impacto no es nulo pero si que es mínimo. Nadie podrá crear dinero de la nada, ó robarte tu dinero, pero si que es verdad que si justo tu ordenador había hecho una transacción enviando el mensaje a uno de los ordenadores afectados, tu transacción quizá tarde en ejecutarse o la tengas que reenviar. Un pequeño retraso burocrático parte del sistema, pero ya está.

De forma análoga, si alguien se corrompe y abusa del poder, digamos robando fondos públicos, en una oligarquía es mucho más difícil detenerlo pues a nada que fallen unos pocos de los elementos del sistema, y a nada que esos elementos pertenezcan a los distintos pocos grupos, por tanto tengan el incentivo de taparse entre ellos, podrán seguir abusando. Sin embargo, en una democracia, a nada que cualquier ciudadano vea que su representante está abusando, tendrá no solo el incentivo de intentar hecharle para quedarse con su puesto, pues hay revocabilidad, sino que también el impacto de la corrupción se verá limitado a robar fondos destinados a una región más pequeña que a una escala nacional como suele pasar en las oligarquías. Cierto es, como con la transacción anterior, habrá un proceso de burocracia, en la forma de juicios y demás, pero eventualmente, tu transacción, el dinero robado será devuelto, ó como mínimo el agresor será castigado.

Este es el segundo argumento a favor de aspirar a un sistema político con un acceso al poder más descentralizado, su mayor resiliencia, tolerancia al fallo. Que mezclado con el argumento primero, una capacidad de adaptación más diversa y dinámica, ofrece a los participantes del sistema una mayor prosperidad.

// TODO: que pasa cuando el fallo es estructural y se acaba propagando entre niveles de la pirámide?

#### 3.- La complejidad siempre creciente de la sabiduría humana hace inevitable la democracia

Las sociedades humanas que sobreviven a largo plazo acarrean con ellas la suerte, o la maldición, de haber seguido la dinámica de la siempre creciente sabiduría humana.

Cada generación hereda el conocimiento acumulado de las anteriores y le añade el suyo. La complejidad de las sociedades humanas no para de crecer: más tecnología, más interconexión, más variables que gestionar. Un protocolo centralizado que funcionaba para una aldea de 500 personas no funciona para una ciudad de 5 millones. Un protocolo que funcionaba en el siglo XVIII no funciona en el siglo XXI.

Este incremento en la complejidad no solo es motivado por los problemas y las adversidades que hacen moverse a un ser humano. Incluso asumiendo que todas las necesidades de la raza humana sean cubiertas, la curiosidad y el aburrimiento que la motiva son rasgos intrínsecos al ser humano de los que no podemos escapar. Es similar al hambre, solo se sacia comiendo. Me atrebería incluso a apostar a que el aburrimiento es igualmente fundamental que el hambre. Pues una vez las necesidades están satisfechas, el motor que nos mueve es el aburrimiento, es lo que nos ha permitido cada vez vivir de manera más y más cómoda y más y más segura en más y más sitios. // TODO: la comodidad acarrea seguirdad?

Los sistemas centralizados y estáticos tienen un techo de complejidad que pueden gestionar más bajo. Cuando la sociedad supera ese techo, el sistema se fractura: en forma de violencia, de miseria silenciosa, de presión social insostenible. La democracia, al distribuir la toma de decisiones y permitir la renovación periódica, tiene un techo de complejidad más alto. No es infinito, pero es significativamente superior.

Dicho de otro modo: aunque sistemas más centralizados puedan ser la solución temporal que funciona ahora y funcionó en el pasado, tarde o temprano dejan de funcionar. La complejidad siempre creciente del conocimiento humano es una maldición (o una bendición) que empuja inevitablemente hacia protocolos más descentralizados y dinámicos que sean capaces de manejar todas las variables de forma más adaptativa y menos dolorosa. No indolora, ó sin necesidad de esfuerzo, pues el cambio siempre requiere de una de estas cosas, ó ambas, pero si más llevadera.

Por tanto, si seguimos comportándonos como estamos programados, o creados, para comportarnos, si seguimos transmitiendo nuestro conocimiento a nuestros hijos dejándonos llevar por la necesidad ó el aburrimiento, tarde o temprano, nos veremos forzados a tener sistemas más y más democráticos.

// TODO: seguir aquí

### En contra

#### 1.- La democracia es como darle una pistola a un mono

El argumento más fuerte en contra de la democracia es el siguiente: la descentralización y el dinamismo solo funcionan bien si se otorgan a individuos con capacidad suficiente para gestionarlos. Dar poder de decisión sobre sistemas ó decisiones complejas a personas que no comprenden esos sistemas produce malas decisiones. Es como darle una pistola a un mono.

Un votante que no entiende cómo funcionan los incentivos fiscales no puede evaluar racionalmente propuestas fiscales. Un votante que nunca ha construido una casa ni estudiado de química no puede evaluar como reglamentar que materiales son permitidos en la construcción de viviendas. La democracia asume que la agregación de muchas decisiones parcialmente informadas produce un resultado razonable. A veces lo produce. A veces no.

Este argumento es el más fundamental utilizado por aquellos a favor de la tecnocracia, un tipo de oligarquía en el que los que ostentan y aspiran al poder son expertos en cuestiones técnicas y específicas, como la tecnología e ingeniería, ramas de la ciencia y demás.

#### 2.- Una transición democrática es muy arriesgada ya que la democracia es más difícil de diseñar e implementar que cualquier otro sistema

Diseñar una constitución democrática funcional es una tarea de complejidad extraordinaria. Una dictadura no necesita preocuparse tan profundamente por un diseño de incentivos tan preciso, de equilibrios de poder, por una redacción sin ambigüedades ni por mecanismos de autocorrección. Una democracia sí. Una democracia mal diseñada colapsa naturalmente en oligarquía o dictadura, porque los actores con más recursos acaban aprovechándose de las debilidades del diseño y poco a poco lo conquistan.

La gran dificultad de alcanzar la democracia es que, volviendo al punto anteiror, el sistema que más inteligencia requiere para su diseño es precisamente el que otorga más poder a personas que pueden no tener esa inteligencia.

Por ende, transicionar a la democracia es peligroso. Pues un cambio tan fundamental y preciso, si se realiza cuando la población aún no esta preparada, es decir, cuando aún no son lo suficientemente inteligentes, conlleva el reisgo del colapso total del sistema y el caos. Pues las dinámicas e instituciones del poder es una parte fundamental para una sociedad, y cuando fallan y colapsan, se crean guerras, incertidumbre, caos.

Intentar alcanzar la democracia es demasiado arriesgado, es como intentar cambiar el un ala de un avión en mitad del vuelo.

#### 3.- El problema de las verdades simplificadas

A medida que las sociedades crecen, ningún individuo puede conocer todo lo suficientemente bien debido a sus límites cognitivos naturales. La gente demanda explicaciones simples para realidades complejas. Los políticos lo saben y se aprovechan de esta necesidad: simplifican, polarizan, reducen problemas multidimensionales a eslóganes de una frase. Los ciudadanos se alinean con la simplificación que más les reconforta, no necesariamente con la que mejor describe la realidad o la que mejor solucione un problema.

Por ello es necesario, y más en democracia, simplificar la realidad para poder adquirir el poder al ganarte el apoyo de la gente. Esto lleva a mandatos basados en la simplificación, que como es de sentido común, no funciona frente a problemas complejos. Otra vez, acabamos dándole una pistola a un mono.

Por ende, y especialmente en sociedades más complejas, ya sea por tamaño ó cantidad de sabiduría, la democracia no lleva necesariamente a soluciones más acertadas, si eso, promueve un pensamiento más simplista.

// TODO: esto es como la respuesta al argumento, no parte de el
Este problema no es exclusivo de la democracia: es un problema de todas las sociedades humanas de alta complejidad, independientemente de su sistema de poder. Pero lo relevante aquí es que la democracia tampoco lo resuelve. La democracia no es una maravilla que lo soluciona todo; es el mejor protocolo disponible, con limitaciones reales que conviene reconocer sin disfrazarlas.

#### 4.- La tendencia oligárquica es inherente al humano

Incluso dentro de sistemas democráticos, por diversos motivos inevitables, las organizaciones tienden a concentrar el poder en pocas manos. Esta es la Ley de Hierro de las Oligarquías de Michels: todo partido, sindicato o movimiento acaba dominado por una élite interna. En la práctica, incluso las democracias mejor diseñadas tienden a la alternancia entre dos o pocos partidos dominantes. Los mecanismos constitucionales pueden limitar esta tendencia pero no eliminarla.

Un análisis de las relaciones humanas basado en teoría de grafos ofrece una explicación estructural de por qué. Si se modela una sociedad como un grafo donde cada persona es un nodo y cada relación es una arista, el número de relaciones posibles crece de forma no-linear.

En el caso más simple con 3 personas (A, B y C) hay exactamente 3 relaciones posibles: A con B, B con C, y C con A. Parece manejable. Pero con 10 personas hay 45 relaciones. Con 100 hay 4.950. Con 1.000 hay casi 500.000. Y al contar las alianzas posibles, subgrupos de 2 o más personas que pueden formarse, la cantidad y complejidad de las relaciones crece aún más rápido. Ningún cerebro humano puede procesar esa cantidad de relaciones simultáneamente. El resultado es que, a medida que un grupo crece, sus miembros necesitan simplificar: delegar, concentrar decisiones, crear jerarquías. No por maldad ni por algún diseño defectuoso que le abra paso, sino porque la complejidad combinatoria supera los límites cognitivos del individuo. La tendencia oligárquica no es un fallo de la democracia; es una consecuencia de los límites biológicos del cerebro humano operando en grupos grandes.

#### 5.- La democracia acarrea reisgo de lentitud de acción en situaciones bélicas

Aunque la democracia fuere funcional, esta lleva consigo el riesgo de que si durante un problema bélico entre Estados una ley impide al ejecutivo realizar cierta opración militar para la defensa del país, se corre el riesgo de que ese impedimento resulte en la pérdida total del país.

Sin embargo en un sistema donde el abuso es más dinámico y libre, el dictador o grupo dominante puede tomar decisiones más rápido y por ende se corre menos riesgo.

Los contrapesos de poderes son ideales y preferibles en tiempos de paz, pero en tiempos de guerra, por su naturaleza intrínsiquecamente abusadora, no favorecen.

### Conclusión: la democracia como destino

Los argumentos en contra son reales. Darle una pistola a un mono es un riesgo real. La dificultad de diseño es real. La tendencia oligárquica es inherente a los límites cognitivos del cerebro humano operando en grupos grandes. Las verdades simplificadas y la polarización son problemas de toda sociedad compleja que la democracia no resuelve. Y ningún sistema político, democrático o no, resuelve por sí solo las relaciones entre Estados soberanos. La democracia no es un sistema perfecto ni garantiza buenos resultados.

Pero los argumentos a favor son estructurales. El argumento de la complejidad siempre creciente de la sabiduría humana empuja inevitablemente hacia sistemas más descentralizados y dinámicos. No es una cuestión de preferencia ideológica: es una consecuencia de cómo acumula conocimiento la especie humana. Mientras sigamos reproduciéndonos, preservando y transmitiendo conocimiento, nuestras sociedades no harán otra cosa que aumentar en complejidad. Y habrá un punto, diferente para cada sociedad, en que los protocolos más centralizados y estáticos simplemente no serán suficientes. La democracia produce el bucle de retroalimentación más rico, refleja mejor la biología humana al conectar estabilidad con adaptación, y minimiza sistemáticamente el alcance del abuso.

Sin embargo, existen límites físicos, inexorables que debemos admitir y entender para que cuando sus efectos negativos se empiezen a divisar, seamos capaces de prevenirlos con madurez, responsabilidad y con moral, por muy ideal que sea, más que con sistemas de contrapeso de poderes. Pues como ya se ha visto en esta crítica, tienen sus límites.

La democracia no es el sistema perfecto. Pero es el protocolo de dinámicas de poder con el techo de complejidad más alto de los que involucran un Estado. Es el que mejor se adapta con la complejidad siempre creciente de las sociedades humanas.

La clave está en que toda la población sea consciente de sus límites y activamente intente no chocarse contra ellos. La clave esta que, en la medida de lo posible, se cree una conciencia nacional de la importancia de lo correcto cuando esos límites sean detectados, es decir, cuando un político

Su debilidad principal —darle una pistola a un mono— no se resuelve con menos democracia, sino con más educación. La solución al mono con la pistola no es quitarle la pistola; es enseñarle a usarla. Esta Constitución no puede resolver ese problema (la educación es competencia legislativa y personal, no constitucional), pero sí puede crear el marco en el que la solución sea posible.

La democracia es, en última instancia, un destino: no porque sea inevitable en cada momento y lugar, sino porque la dirección natural de la complejidad humana en sociedades prósperas apunta hacia ella y la acaba requiriendo. Las sociedades que no lleguen a ella sufrirán más presión, más fricción y más violencia que las que sí lo hagan. Entre todos los protocolos de poder disponibles, este es el que menos mal funciona a largo plazo.

// TODO: estudiar los motivos, desde aquí y Cheerfulism, y describirlo todo más claro entonces.
