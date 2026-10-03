import mimetypes
from django.http import FileResponse, Http404
from .models import Car

def car_photo(request, path):
    # Only files referenced by a car are public; never expose arbitrary disk paths.
    car = Car.objects.filter(image=path).first()
    if not car or not car.image:
        raise Http404
    try:
        photo = car.image.open("rb")
    except (FileNotFoundError, OSError):
        raise Http404
    response = FileResponse(photo, content_type=mimetypes.guess_type(car.image.name)[0] or "application/octet-stream")
    response["X-Content-Type-Options"] = "nosniff"
    return response
