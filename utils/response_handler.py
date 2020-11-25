from rest_framework.response import Response


def success(message, data, total=None):
    if total == None:
        return Response({'success': True, 'message': message, 'data': data})

    return Response({'success': True, 'message': message, 'data': data, 'total': total})


def not_found(message):
    return Response({'success': False, 'message': message, 'data': []})


def error_has_ocurred(message, error):
    return Response({'success': False, 'message': message, 'error': error})
