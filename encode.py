#!/usr/bin/env python
# coding: utf-8

# In[10]:


# conda install opencv
# pip installl pypng
# coding utf-8


# In[101]:

from PIL import Image
import cv2
import png
import os
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
from tkinter import simpledialog
import sys

# In[115]:


# dizin belirleme
Tk().withdraw()
path = askopenfilename(title="İşlenecek Fotoğrafı Seçiniz.", filetypes=(("Image", "*.png"), ("Image", "*.jpg*")))
if os.path.splitext(path)[1] != ".png" and os.path.splitext(path)[1] != ".jpg":
    messagebox.showwarning("Warning", "Dosya .png ya da .jpg uzantılı olmalıdır.")
    sys.exit()
# In[118]:


# resim ekleme
try:
    resim = Image.open(path)
    if resim.size[0] < 9:
        messagebox.showwarning("Warning", "İşlenecek dosya ebatları çok küçük!")
        sys.exit()
    resim_rgb = resim.convert("RGB")
    maks_uzunluk = (int(resim.size[0] / 3)) * resim.size[1] - 3
    resim.close()
except FileNotFoundError:
    messagebox.showwarning("Warning", "İşlenecek dosya bulunamadı! ")
    sys.exit()
except PermissionError:
    messagebox.showwarning("Warning", "İşlenecek dosya yoluna erişim hakkınız bulunmuyor!")
    sys.exit()

# In[119]:


degis_resim = list()
for i in range(0, resim.size[1]):
    satir = list()
    for j in range(0, resim.size[0]):
        pixel = [*resim_rgb.getpixel((j, i))]
        satir.append(pixel[0])
        satir.append(pixel[1])
        satir.append(pixel[2])
    degis_resim.append(satir)

# In[120]:


# resme gizli mesajı entegre etme
mesaj = simpledialog.askstring('Veri Girisi', 'Gizlenecek veriyi giriniz ')
if mesaj == None or not len(mesaj) > 0:
    messagebox.showwarning("Warning", "Veri girdisi yapılmadı!")
    sys.exit()
if len(mesaj) > maks_uzunluk:
    messagebox.showwarning("Warning", "Hatalı girdi yapıldı!\nPrograma tanımladığınız {}×{} ebatlarındaki resim için"
                                      " işlenebilecek mesajın maksimum karakter sayısı {} olmalıdır. \nLütfen daha"
                                      " kısa bir mesaj giriniz veya işlenecek resmin boyutlarını büyütüp programı"
                                      " yeniden çalıştırınız. \nEntegre edilmek istenen karakter sayısı : {}"
                           .format(resim.size[0], resim.size[1], maks_uzunluk, uzunluk))
    sys.exit()
uzunluk = len(mesaj)
for i in range(0, uzunluk):
    if ord([*mesaj][i]) > 512:
        messagebox.showwarning("Warning", "Hatalı girdi yapıldı!\nGirdiğiniz {} karakteri işlemeye uygun değildir."
                                          "Lütfen mesajı kontrol ediniz. ".format([*mesaj][i]))
        sys.exit()
if uzunluk > (2 ** 28):
    messagebox.showwarning("Warning", "Hatalı girdi yapıldı!\nProgram en fazla {} karakterlik veri işleyebilirsiniz. "
                                      "{} Karakterlik mesaj girebildiğiniz için sizi tebrik ederiz. Umarız bu mesajı "
                                      "görebilirsiniz. :)".format(2 ** 28, uzunluk))
    sys.exit()

# In[121]:


# şifre uzunluğu entegresi
parca_uzunluk = [*format(uzunluk, "27b")]
for i in range(0, 27):
    if parca_uzunluk[i] == " ":
        parca_uzunluk[i] = 0
u_kontrol_indisi = 0
u_pixel_sayac_en = 0
u_pixel_sayac_boy = 0
for i in range(0, 3):
    for j in range(u_pixel_sayac_en, u_pixel_sayac_en + 9, 3):
        u_pixel = degis_resim[u_pixel_sayac_boy][j:j + 3]
        for k in range(0, 3):
            # print(u_pixel)
            if (int(parca_uzunluk[u_kontrol_indisi]) == u_pixel[k] % 2):
                u_kontrol_indisi += 1
            elif (int(parca_uzunluk[u_kontrol_indisi]) == 1):
                degis_resim[u_pixel_sayac_boy][j + k] += 1
                u_kontrol_indisi += 1
            else:
                degis_resim[u_pixel_sayac_boy][j + k] -= 1
                u_kontrol_indisi += 1
    u_pixel_sayac_en += 9;

# In[122]:

parca_mesaj = [*mesaj]
if resim.size[0] < 18:
    pixel_sayac_en = 0
    pixel_sayac_boy = 1
else:
    pixel_sayac_en = 27
    pixel_sayac_boy = 0
for i in range(0, uzunluk):
    if pixel_sayac_en >= 3 * resim.size[0] - 3 * (resim.size[0] % 3):
        pixel_sayac_en = 0
        pixel_sayac_boy += 1

    parca_byte = [*format(ord(parca_mesaj[i]), "09b")]
    kontrol_indisi = 0;
    for j in range(pixel_sayac_en, pixel_sayac_en + 9, 3):
        pixel = degis_resim[pixel_sayac_boy][j:j + 3]

        for k in range(0, 3):
            if (int(parca_byte[kontrol_indisi]) == pixel[k] % 2):
                kontrol_indisi = kontrol_indisi + 1

            elif (int(parca_byte[kontrol_indisi]) == 1):
                degis_resim[pixel_sayac_boy][j + k] += 1
                kontrol_indisi += 1
            else:
                degis_resim[pixel_sayac_boy][j + k] -= 1
                kontrol_indisi += 1
    pixel_sayac_en += 9;

messagebox.showinfo("Message", "{} karakterlik bir mesaj resme işlendi.\n\n "
                               "Lütfen mesaj uzunluğunu not etmeyi unutmayınız! Resim çözümleme aşamasında"
                               " bu değerin hatalı girilmesi durumunda mesaj okunamayacaktır.".format(uzunluk))
newPath = ''.join([os.path.dirname(os.path.abspath(path)), '\\new', os.path.basename(path)])
# In[123]:


try:
    p = degis_resim
    with  open(newPath, 'wb') as f:
        w = png.Writer(resim.size[0], resim.size[1], greyscale=False)
        w.write(f, p)
except PermissionError:
    messagebox.showwarning("Warning", "Mevcut dosya yoluna yazma hakkınız bulunmuyor!")
    sys.exit()

# In[127]:


