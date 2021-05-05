#!/usr/bin/env python
# coding: utf-8

# In[10]:


#conda install opencv
#pip installl pypng
#coding utf-8



from PIL import Image
import cv2
import png
import os
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
from tkinter import simpledialog
import sys
try:
    Tk().withdraw()
    newpath = askopenfilename(title="Çözümlenecek Fotoğrafı Seçiniz.", filetypes=(("Image", "*.png"), ("Image", "*.jpg*")))
    if os.path.splitext(newpath)[1] != ".png" and os.path.splitext(newpath)[1] != ".jpg":
        messagebox.showwarning("Warning", "Dosya .png ya da .jpg uzantılı olmalıdır.")
        sys.exit()
    s_resim=Image.open(newpath)
    s_resim_rgb = s_resim.convert("RGB")
    s_maks_uzunluk = (int(s_resim.size[0] / 3)) * s_resim.size[1]
    s_resim.close()
except FileNotFoundError:
    messagebox.showwarning("Warning", "Çözümlenecek dosya bulunamadı! ")
    sys.exit()
except PermissionError:
    messagebox.showwarning("Warning", "Çözümlenecek dosya yoluna erişim hakkınız bulunmuyor!")
    sys.exit()

#şifre uzunluğu decode etme işlemi
s_u_pixel_sayac_en=0
s_u_pixel_sayac_boy=0
deger=0
s_u_kontrol_indisi=26;
for i in range(0, 3):
    for j in range(s_u_pixel_sayac_en,s_u_pixel_sayac_en+3):
        s_u_pixel=s_resim_rgb.getpixel((j,s_u_pixel_sayac_boy))
        for k in range(0,3):
            if (int(s_u_pixel[k])%2==1):
                deger=deger+(int(s_u_pixel[k])%2*(2**s_u_kontrol_indisi))
            s_u_kontrol_indisi-=1
    s_u_pixel_sayac_en+=3


# In[145]:


#decode etme işlemi
s_uzunluk=simpledialog.askstring('Veri Girisi','Çözümlenecek şifrenin uzunluğunu giriniz ')
if s_uzunluk==None or not len(s_uzunluk)>0:
    messagebox.showwarning("Warning","Veri girdisi yapılmadı!")
    sys.exit()
if not s_uzunluk.isdigit():
    messagebox.showwarning("Warning","Çözümlenecek şifrenin UZUNLUĞUNU girdiğinizden emin olunuz.")
    sys.exit()
try:
    s_uzunluk=int(s_uzunluk)
    if (s_uzunluk>s_maks_uzunluk):
        messagebox.showwarning("Warning","Programa tanımladığınız {}×{} ebatlarındaki resim için çözülebilecek mesajın maksimum karakter sayısı"
           " {} olmalıdır. \nLütfen size iletilen karakter sayısını giriniz veya işlenecek resmin yüklendiğinden emin "
           "olup programı yeniden çalıştırınız. \nÇözümlenmesi istenen karakter sayısı : {}"
           .format(s_resim.size[0], s_resim.size[1], s_maks_uzunluk, s_uzunluk))
        sys.exit()

    if s_uzunluk!=deger:
        messagebox.showwarning("Warning","Şifre uzunluk sayısı yanlış girildi! Lütfen şifre uzunluğunu "
                                         "doğru girdiğinizden emin olunuz!")
        sys.exit()

except ValueError:
    messagebox.showwarning("Warning","Çözümlenecek şifrenin UZUNLUĞUNU girdiğinizden emin olunuz.")
    sys.exit()


# In[150]:


if s_resim.size[0]<6:
    s_pixel_sayac_en=0
    s_pixel_sayac_boy=1
else:
    s_pixel_sayac_en=9
    s_pixel_sayac_boy=0
gizli_mesaj=""
for i in range(0, int(s_uzunluk)):
    if s_pixel_sayac_en>=s_resim.size[0]- s_resim.size[0] % 3:
        s_pixel_sayac_en=0
        s_pixel_sayac_boy+=1
    deger=0
    s_kontrol_indisi=8;
    for j in range(s_pixel_sayac_en,s_pixel_sayac_en+3):
        s_pixel=s_resim_rgb.getpixel((j,s_pixel_sayac_boy))
        #print(s_pixel)
        for k in range(0,3):
                deger=deger+(int(s_pixel[k])%2*(2**s_kontrol_indisi))
                s_kontrol_indisi-=1
        s_pixel_sayac_en+=1
    gizli_mesaj+=str(chr(deger))
messagebox.showinfo("Message","Mesajınız Başarıyla Çözümlendi!\n\nMesajınız:\n{}".format(gizli_mesaj))
