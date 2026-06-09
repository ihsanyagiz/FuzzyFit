# FuzzyFit: Presentation Outline

Bu belge, CENG 386 dersi için yapacağınız sunumun (PowerPoint / Canva) slayt planını ve sunum sırasında hocanıza söylemeniz gereken anahtar cümleleri (Speaker Notes) içermektedir.

---

### Slide 1: Title Slide
* **Visual:** Projenin adı "FuzzyFit: Adaptive Workout Intensity & Recovery Guide", adınız ve ders kodu.
* **Speaker Notes:** "Herkese merhaba, bugün sizlere geleneksel statik antrenman programlarının aksine, insanın değişken fiziksel durumunu hesaba katan Bulanık Mantık tabanlı akıllı fitness asistanım FuzzyFit'ten bahsedeceğim."

### Slide 2: The Problem with Traditional Systems
* **Visual:** İki farklı resim; birinde sabit bir takvim (Pazartesi ağır bacak günü), diğerinde yorgun ve uykusuz bir sporcu.
* **Speaker Notes:** "Klasik sistemler siyah veya beyazdır. 'Bugün bacak günü, o yüzden 100 kilo kaldırmalısın' derler. Fakat insan vücudu bulanıktır (fuzzy). Gece kötü uyumuş, stresli veya yorgun olabiliriz. Bu belirsizliği modellemek için Fuzzy Logic mükemmel bir araçtır."

### Slide 3: System Architecture (Inputs & Outputs)
* **Visual:** Ortada bir "Fuzzy Engine" kutusu, soldan giren 4 ok (Sleep, Soreness, Energy, Stress), sağdan çıkan 2 ok (Intensity, Volume).
* **Speaker Notes:** "Sistemimiz Mamdani çıkarım modelini kullanıyor. 4 adet girdimiz (Uyku, Kas Ağrısı, Enerji ve Stres) ve karşılığında bize o günkü antrenmanın şiddetini ve hacmini veren 2 adet çıktımız var."

### Slide 4: Membership Functions (Fuzzification)
* **Visual:** `app.py` üzerinden aldığınız girdi grafiklerinin ekran görüntüleri (Üçgen ve yamuk üyelik fonksiyonları).
* **Speaker Notes:** "Girdilerimizi ve çıktılarımızı modellerken keskin sınırlar yerine, insani dilin doğasına uygun olan üçgensel (trimf) ve yamuksal (trapmf) üyelik fonksiyonları kullandık. Örneğin bir uykuyu 0-10 arasında 'Kötü', 'Ortalama' ve 'İyi' olarak bulanıklaştırdık."

### Slide 5: The Rule Base (Knowledge Base)
* **Visual:** Sistemdeki 18 kuraldan en ilginç 3-4 tanesinin listesi.
* **Speaker Notes:** "Sistemimizde uzman görüşüne (expert knowledge) dayanan 18 adet AND/OR bağlaçlı kural bulunuyor. Örneğin: Eğer uyku iyi VE kas ağrısı düşük VE enerji fazlaysa; antrenman şiddeti maksimum olmalıdır. Kuralları geniş tutarak hiçbir ihtimalin ölü bölgede kalmamasını sağladık."

### Slide 6: Defuzzification & 3D Control Surfaces
* **Visual:** Uygulamadaki 3D Karar Yüzeyi (Control Surface) grafiğinin bir videosu veya GIF'i.
* **Speaker Notes:** "Sonucu keskinleştirmek (Defuzzification) için Ağırlık Merkezi (Centroid) yöntemini kullanıyoruz. Ekranda gördüğünüz 3D Karar Yüzeyi, sabit stres ve yorgunluk altında, Uyku ve Enerji seviyesinin antrenman şiddetini nasıl doğrusal olmayan (non-linear) bir şekilde etkilediğini çok net gösteriyor."

### Slide 7: Why Python & Modern UI/UX? (MATLAB vs Python)
* **Visual:** Solda sıkıcı bir MATLAB ekranı, sağda sizin hazırladığınız neon arayüzlü Streamlit uygulaması ve "Gestalt Principles" yazısı.
* **Speaker Notes:** *(Burayı özellikle vurgulayın)* "Derste MATLAB görmemize rağmen, ben projeyi gerçek dünyada kullanılabilecek, modern bir web uygulaması olarak tasarlamak istedim. Bu yüzden Python'un `scikit-fuzzy` kütüphanesini tercih ettim. Ayrıca arayüz tasarımında **Gestalt prensiplerini** (Örneğin girdileri aynı alanda toplayarak 'Common Region' kuralı ve ekranı 'Symmetry' ile ikiye bölme) uygulayarak, kullanıcı dostu (User-centric) bir deneyim yarattım."

### Slide 8: Live Demo
* **Visual:** Sadece "Live Demo" yazısı.
* **Speaker Notes:** "Şimdi sistemin canlı olarak nasıl çalıştığına, kuralların nasıl hesaplandığına ve farklı defuzzification yöntemlerinin (Centroid, Bisector) sonucu nasıl etkilediğine bakalım." *(Burada app.py'yi açıp sunum yaparsınız).*

### Slide 9: Conclusion & Q&A
* **Visual:** Teşekkürler mesajı.
* **Speaker Notes:** "Bulanık mantığın teorik hesaplamalarının, doğru bir UI/UX mimarisiyle birleştiğinde günlük hayatta ne kadar pratik bir ürüne dönüşebileceğini görmüş olduk. Dinlediğiniz için teşekkürler, sorularınız varsa alabilirim."
