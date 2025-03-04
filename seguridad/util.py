import datetime
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils import timezone
import logging

logger = logging.getLogger('django')

def es_admin(request):
    usuario = request.user
    esAdmin = usuario.groups.filter(name="SUPERUSUARIO").exists()
    return esAdmin
    
def ofuscarDatosUsuario(pk):
    # from clientes.models import Clientes
    # from reservas.models import Reservas
    # from seguridad.models import User_Detalle
    
    # usuario = User.objects.get(id=pk)
    # fecha = datetime.date.today()

    # fechas = Q(Q(usuario = usuario) & Q(fecha_desde__lte=fecha ) & Q(fecha_hasta__gte=fecha ))

    # if Reservas.objects.filter(fechas).exclude(estado_id=4).count() == 0:

    #     usuario.anonymise()
    #     try:
    #         cliente = Clientes.objects.get(usuario=usuario)
    #         cliente.anonymise()
            
    #         userdetalle = User_Detalle.objects.get(usuario=usuario) 
    #         userdetalle.anonymise()
    #     except:
    #         pass
    #     return True
        
    #     usuario.is_active = False
    #     usuario.save()

    # else:
    return False

def registra_session(usuario,token):
    from seguridad.models import SessionHistory
    now = timezone.now()
    logger = logging.getLogger('django')

    try:
        session_history = SessionHistory.objects.get(user=usuario,last_activity__isnull=True)
    except:
        try:
            session_history, created = SessionHistory.objects.get_or_create(
                user=usuario,
                session_key=token,
                duration=datetime.timedelta(seconds=0),
                defaults={'start_time': now, 'last_activity': None}
            )

            if not created:
                session_history.save()

        except Exception as e:
            logger.error(e)
    
def finaliza_session(token):
    from seguridad.models import SessionHistory
    
    session_history = SessionHistory.objects.filter(
        session_key=token
    ).first()
    
    if session_history:
        session_history.last_activity = datetime.datetime.now()
        session_history.duration = datetime.datetime.now(datetime.timezone.utc) - session_history.start_time
        session_history.save()