# myproject/urls.py (atau nama_proyek_utama_anda/urls.py)

from django.contrib import admin
from django.urls import path, include # Pastikan 'include' sudah diimpor
# Import views dari onlinecourse untuk routing langsung jika diperlukan
from django.conf import settings # Import settings untuk serve media files
from django.conf.urls.static import static # Import static untuk serve media files

urlpatterns = [
    path('admin/', admin.site.urls),
    # Sertakan URL dari aplikasi onlinecourse
    # Anda bisa memilih path prefix yang Anda inginkan, misalnya 'onlinecourse/'
    # Atau jika Anda ingin aplikasi onlinecourse menjadi homepage, Anda bisa menggunakan ''
    path('onlinecourse/', include('onlinecourse.urls')), # Contoh: akan diakses melalui http://127.0.0.1:8000/onlinecourse/
    # Atau, jika Anda ingin halaman utama adalah dari onlinecourse:
    # path('', include('onlinecourse.urls')),
]

# Tambahkan ini untuk melayani media files (seperti gambar kursus) dalam mode development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)