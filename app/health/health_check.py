from app.models.resource_model import ResourceModel
from app.services.redis_service import redis_conn


def redis_available():
    redis_conn.client()
    return True, "redis is ok"


def mongodb_available():
    try:
        result = ResourceModel.objects()
        if result:
            return True, "database is ok"
    except Exception as e:
        return False, str(e)


HEALTH_CHECKS = [redis_available, mongodb_available]
