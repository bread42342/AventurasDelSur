from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from core.models import ConfiguracionEcoparque
from cuentas.models import Perfil, Usuario
from experiencias.models import Categoria, Experiencia, Inscripcion

CATEGORIAS = [
    ('Trekking', 'Caminatas guiadas por volcanes, cerros y bosque nativo del sur de Chile.'),
    ('Canopy', 'Tirolesas entre las copas de los árboles.'),
    ('Arriendo de equipos', 'Arriendo de bicicletas, bastones y equipo de camping.'),
    ('Kayak y rafting', 'Remo en lagos y descenso de ríos de aguas claras.'),
    ('Observación de aves', 'Salidas de avistamiento con guía especializado.'),
    ('Termas y relajo', 'Baños termales rodeados de bosque y volcanes.'),
    ('Cabalgatas', 'Recorridos a caballo por valles y orillas de lago.'),
    ('Turismo cultural', 'Visitas a ferias, museos y rutas gastronómicas de la región.'),
]

EXPERIENCIAS = {
    'trabajador1': [
        ('Trekking Volcán Osorno, Puerto Varas', 'Ascenso guiado hasta el refugio con vista al lago Llanquihue.', 'Trekking', 32000, 12, 5),
        ('Trekking Parque Nacional Villarrica, Pucón', 'Caminata de 5 horas por bosque de araucarias y coladas de lava.', 'Trekking', 35000, 10, 9),
        ('Trekking Reserva Altos de Lircay, Talca', 'Recorrido hasta el Mirador del Valle del Venado en la precordillera.', 'Trekking', 22000, 15, 6),
        ('Canopy Lago Calafquén, Villarrica', 'Circuito de 8 tirolesas con vista al lago y al volcán.', 'Canopy', 38000, 8, 7),
        ('Cabalgata Valle del Río Maullín, Puerto Montt', 'Paseo a caballo de 3 horas por el valle y la ribera.', 'Cabalgatas', 30000, 8, 12),
        ('Termas Geométricas, Panguipulli', 'Jornada de relajo en pozones termales entre pasarelas de madera.', 'Termas y relajo', 45000, 20, 15),
        ('Trekking Parque Nacional Conguillío, Temuco', 'Sendero Sierra Nevada entre araucarias milenarias y lagunas.', 'Trekking', 34000, 12, 11),
    ],
    'trabajador2': [
        ('Kayak Lago Panguipulli, Los Ríos', 'Remada de 3 horas por las aguas del lago con picnic incluido.', 'Kayak y rafting', 28000, 10, 6),
        ('Rafting Río Trancura, Pucón', 'Descenso de aguas bravas clase III con equipo completo.', 'Kayak y rafting', 36000, 10, 10),
        ('Navegación en kayak Río Calle-Calle, Valdivia', 'Paseo tranquilo entre humedales y lobos marinos.', 'Kayak y rafting', 26000, 10, 8),
        ('Avistamiento de aves Santuario Río Cruces, Valdivia', 'Salida de amanecer con binoculares para ver cisnes de cuello negro.', 'Observación de aves', 18000, 8, 4),
        ('Ruta de los Humedales de Chiloé, Ancud', 'Avistamiento de aves migratorias y visita a palafitos.', 'Observación de aves', 24000, 8, 13),
        ('Ruta gastronómica Mercado Fluvial, Valdivia', 'Recorrido por el mercado, cervecerías y productos locales.', 'Turismo cultural', 20000, 15, 9),
        ('Arriendo Pack Camping, Puerto Montt', 'Carpa, saco y aislante para una noche en Cochamó.', 'Arriendo de equipos', 15000, 15, 14),
        ('Arriendo de bicicletas, Temuco', 'Bicicleta de montaña con casco por el día para rutas urbanas y rurales.', 'Arriendo de equipos', 12000, 15, 3),
    ],
}

RESERVAS = {
    'cliente1': ['Trekking Volcán Osorno, Puerto Varas', 'Canopy Lago Calafquén, Villarrica', 'Kayak Lago Panguipulli, Los Ríos', 'Avistamiento de aves Santuario Río Cruces, Valdivia'],
    'cliente2': ['Trekking Parque Nacional Villarrica, Pucón', 'Rafting Río Trancura, Pucón', 'Termas Geométricas, Panguipulli'],
}

REALIZADAS = [
    ('trabajador1', 'Trekking Cerro Mariposas, Talca', 'Ascenso al cerro con vista a la ciudad y al valle del Maule.', 'Trekking', 18000, 12, -9, 0, 'finalizada'),
    ('trabajador2', 'Kayak Río Maule, Talca', 'Remada por el río entre humedales y bosque de ribera.', 'Kayak y rafting', 24000, 10, -4, 0, 'finalizada'),
    ('trabajador1', 'Canopy Bosque Valdiviano, Valdivia', 'Circuito de 10 tirolesas entre árboles nativos con instructores certificados.', 'Canopy', 34000, 8, 0, -4, 'en_curso'),
]

RESERVAS_REALIZADAS = [
    ('cliente1', 'Trekking Cerro Mariposas, Talca', 2, 2, 5),
    ('cliente2', 'Trekking Cerro Mariposas, Talca', 1, 1, 4),
    ('cliente2', 'Kayak Río Maule, Talca', 1, 1, 4),
    ('cliente1', 'Canopy Bosque Valdiviano, Valdivia', 3, 0, None),
]

USUARIOS = [
    ('admin', 'Eva3', 'admin', 'Sebastian', 'Gatica', 'SebastianGatica@aventurasdelsur.cl', '+56982345671', 'Puerto Varas'),
    ('trabajador1', 'Eva3', 'guia', 'Rick', 'Grimes', 'RickGrimes@aventurasdelsur.cl', '+56991234502', 'Puerto Varas'),
    ('trabajador2', 'Eva3', 'guia', 'Daryl', 'Dixon', 'DarylDixon@aventurasdelsur.cl', '+56978451263', 'Puerto Montt'),
    ('cliente1', 'Eva3', 'turista', 'Carol', 'Peletier', 'CarolPeletier@gmail.com', '+56965432198', 'Santiago'),
    ('cliente2', 'Eva3', 'turista', 'Maggie', 'Greene', 'MaggieGreene@gmail.com', '+56957123864', 'Concepción'),
]


class Command(BaseCommand):
    help = 'Carga usuarios, categorías, experiencias y reservas de prueba.'

    @transaction.atomic
    def handle(self, *args, **options):
        ConfiguracionEcoparque.objects.update_or_create(pk=1, defaults={
            'nombre': 'Aventuras del Sur',
            'descripcion': 'Ecoparque y reserva natural con experiencias guiadas en el sur de Chile.',
            'direccion': 'Camino a Volcán Osorno km 12, Puerto Varas',
            'telefono': '+56965001122',
            'correo': 'contacto@aventurasdelsur.cl',
            'horario_apertura': '09:00',
            'horario_cierre': '18:00',
            'politica_cancelacion': 'Las reservas con pago pendiente se pueden cancelar sin costo. Las reservas con pago confirmado se gestionan con el administrador.',
        })
        Inscripcion.objects.all().delete()
        Experiencia.objects.all().delete()
        Categoria.objects.all().delete()
        usuarios = {}
        for username, clave, rol, nombre, apellido, correo, telefono, ciudad in USUARIOS:
            usuario, _ = Usuario.objects.get_or_create(username=username)
            usuario.first_name = nombre
            usuario.last_name = apellido
            usuario.email = correo
            usuario.rol = rol
            usuario.is_staff = rol == 'admin'
            usuario.is_superuser = rol == 'admin'
            usuario.set_password(clave)
            usuario.save()
            Perfil.objects.update_or_create(
                usuario=usuario, defaults={'telefono': telefono, 'ciudad': ciudad, 'documento': ''})
            usuarios[username] = usuario

        categorias = {n: Categoria.objects.get_or_create(nombre=n, defaults={'descripcion': d})[0] for n, d in CATEGORIAS}

        ahora = timezone.now().replace(minute=0, second=0, microsecond=0)
        experiencias = {}
        for guia, lista in EXPERIENCIAS.items():
            for titulo, descripcion, categoria, precio, cupo, dias in lista:
                experiencia, _ = Experiencia.objects.get_or_create(
                    titulo=titulo,
                    defaults={
                        'descripcion': descripcion,
                        'precio': precio,
                        'cupo_maximo': cupo,
                        'fecha_hora': ahora + timedelta(days=dias, hours=3),
                        'categoria': categorias[categoria],
                        'creador': usuarios[guia],
                    },
                )
                experiencias[titulo] = experiencia

        for guia, titulo, descripcion, categoria, precio, cupo, dias, horas, estado in REALIZADAS:
            experiencias[titulo] = Experiencia.objects.create(
                titulo=titulo,
                descripcion=descripcion,
                precio=precio,
                cupo_maximo=cupo,
                fecha_hora=ahora + timedelta(days=dias, hours=horas),
                categoria=categorias[categoria],
                creador=usuarios[guia],
                estado=estado,
            )

        for turista, titulo, cantidad, asistentes, puntaje in RESERVAS_REALIZADAS:
            Inscripcion.objects.create(
                usuario=usuarios[turista],
                experiencia=experiencias[titulo],
                estado_pago='confirmado',
                cantidad=cantidad,
                asistentes=asistentes,
                puntaje=puntaje,
            )

        for turista, titulos in RESERVAS.items():
            for indice, titulo in enumerate(titulos):
                Inscripcion.objects.get_or_create(
                    usuario=usuarios[turista],
                    experiencia=experiencias[titulo],
                    defaults={'estado_pago': 'confirmado' if indice % 2 == 0 else 'pendiente', 'cantidad': 1 + indice % 3},
                )

        self.stdout.write(self.style.SUCCESS('Datos de prueba cargados.'))
