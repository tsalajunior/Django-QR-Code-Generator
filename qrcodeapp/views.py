from django.shortcuts import render
from .models import QR_code

# Create your views here.
def index(request, *args, **kwargs):
    context = {}

    if request.method == "POST":
        data = request.POST.get("data", "").strip()
        if not data:
            context["error"] = "Enter some text to generate a QR code."
        elif len(data) > 250:
            context["error"] = "Text must be 250 characters or fewer."
        else:
            context["data"] = data
            context["qr_code"] = QR_code.objects.create(data=data)

    return render(request, "index.html", context)