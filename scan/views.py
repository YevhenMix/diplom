from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages

from .forms import ScanFilesForm
from .models import ScanFile
from .scan_utils import scan_file, convert_to_pdf


class HomeView(View):

    def get(self, request):
        form = ScanFilesForm()
        context = {'form': form}
        return render(request, 'scan/home.html', context)

    def post(self, request):
        form = ScanFilesForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            name = request.FILES.get('photo').name.split('.')[0]
            scan_file(name)

            image = ScanFile.objects.last()
            name = image.scanned_photo.name.split('/')[-1].split('.')[0]
            convert_to_pdf(image_path=image.scanned_photo.path, name=name, image=image)
            messages.success(request, 'Фото успешно отсканировано!')
            return redirect('scan:scanned')
        context = {'form': form}
        return render(request, 'scan/home.html', context)


class ScannedView(View):

    def get(self, request):
        photo = ScanFile.objects.all()[::-1]
        context = {'photos': photo}
        return render(request, 'scan/scanned.html', context)


class ScanDetailView(View):

    def get(self, request, pk):
        image = ScanFile.objects.get(id=pk)
        context = {'photo': image}
        return render(request, 'scan/detail.html', context=context)
