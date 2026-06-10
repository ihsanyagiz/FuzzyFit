# FuzzyFit: Presentation Outline

Bu belge, CENG 386 dersi için yapacağınız sunumun (Beamer LaTeX sunumu) slayt planını ve sunum sırasında hocanıza söylemeniz gereken anahtar cümleleri (Speaker Notes) içermektedir.

---

### Slide 1: Title Slide
* **Visual:** Projenin adı "FuzzyFit: Adaptive Workout Intensity & Recovery Guide", adınız ve ders kodu (CENG 386 - Fuzzy Logic).
* **Speaker Notes:** "Herkese merhaba, bugün sizlere geleneksel statik antrenman programlarının aksine, insanın değişken fiziksel ve psikolojik durumunu hesaba katan Bulanık Mantık tabanlı akıllı fitness asistanım FuzzyFit'ten bahsedeceğim."

### Slide 2: The Problem with Traditional Systems
* **Visual:** İki farklı resim; birinde sabit bir takvim (Pazartesi ağır bacak günü), diğerinde yorgun ve uykusuz bir sporcu.
* **Speaker Notes:** "Klasik antrenman planları ikilidir (binary). 'Bugün bacak günü, o yüzden 100 kilo kaldırmalısın' derler. Fakat insan vücudu bulanıktır (fuzzy). Gece kötü uyumuş, stresli veya beslenmesi yetersiz olabilir. Bu belirsizliği modellemek ve sürdürülebilir antrenman önermek için Fuzzy Logic mükemmel bir araçtır."

### Slide 3: System Architecture (Inputs & Outputs)
* **Visual:** Ortada bir "Fuzzy Engine" kutusu, soldan giren 4 ok (Sleep, Soreness, Energy, Stress), sağdan çıkan 2 ok (Intensity, Volume).
* **Speaker Notes:** "Sistemimiz Mamdani çıkarım modelini kullanıyor. 4 adet girdimiz (Uyku Kalitesi, Kas Ağrısı, Enerji Seviyesi ve Stres Seviyesi) ve karşılığında bize o günkü antrenmanın şiddetini (%) ve hacmini (Dakika) veren 2 adet çıktımız var."

### Slide 4: Fuzzification (Equations & Membership Functions)
* **Visual:** Girdi ve çıktı değişkenlerinin üyelik fonksiyonları grafiklerinin ekran görüntüleri ve matematiksel formülleri (triangular/trapezoidal).
* **Speaker Notes:** "Girdilerimizi ve çıktılarımızı modellerken keskin sınırlar yerine, insani dilin doğasına uygun olan üçgensel (trimf) ve yamuksal (trapmf) üyelik fonksiyonları kullandık. Formüllerde gördüğünüz üzere, örneğin bir uyku kalitesi 4.5 olduğunda sistem bunu kısmen 'Kötü' ve kısmen 'Ortalama' olarak eşzamanlı değerlendirir."

### Slide 5: The Rule Base (Knowledge Base)
* **Visual:** Sistemdeki 18 kuraldan en önemli 3-4 tanesinin mantıksal listesi.
* **Speaker Notes:** "Sistemimizde uzman görüşüne (expert knowledge) dayanan 18 adet AND/OR bağlaçlı kural bulunuyor. Örneğin: Eğer uyku iyi VE kas ağrısı düşük VE enerji fazlaysa; antrenman şiddeti maksimum olmalıdır. Kuralları geniş tutarak girdi uzayının tamamını kapsadık ve hiçbir ihtimalin ölü bölgede kalmamasını sağladık."

### Slide 6: Defuzzification Mathematics
* **Visual:** Centroid (Ağırlık Merkezi), Bisector ve MOM (Maksimumun Ortalaması) yöntemlerinin integral formülleri.
* **Speaker Notes:** "Bulanık kümeleri gerçek hayatta uygulanabilir keskin değerlere (crisp values) dönüştürmek için durulaştırma (defuzzification) yapıyoruz. Ağırlık Merkezi (Centroid) varsayılan yöntemimizdir. Ancak akademik derinliği artırmak adına sistemimizi farklı matematiksel durulaştırma yöntemlerini de destekleyecek şekilde kurduk."

### Slide 7: Defuzzification Methods Comparison
* **Visual:** Farklı fiziksel profillerde (Profile 1: Yorgun, Profile 2: Dengeli) durulaştırma yöntemlerinin ürettiği sonuçları karşılaştıran tablo.
* **Speaker Notes:** "Sistemimizde farklı durulaştırma yöntemlerini test ettik. Girdi değerlerinin durumuna göre yöntemler benzer çıktılar verebilir. Simetrik üyelik fonksiyonlarının aktif olduğu dengeli durumlarda Centroid, Bisector ve MOM'un aynı sonuçları vermesi, sistemimizin kararlı ve tutarlı çalıştığının matematiksel kanıtıdır."

### Slide 8: Technology Stack & Web App Features (MATLAB vs Python)
* **Visual:** Streamlit uygulamasının arayüzünden (Öneri Tablosu, Canlı Bulanıklaştırma ve Grafik Paneli) ekran görüntüleri.
* **Speaker Notes:** "Derste MATLAB yaygın kullanılsa da, ben projeyi gerçek dünyada çalışabilecek, bulut konuşlu bir web uygulaması tasarlamak istedim. Python (scikit-fuzzy) + Streamlit kullanarak; girdilerin üyelik derecelerini anlık gösteren Canlı Bulanıklaştırma Paneli, Plotly ile etkileşimli 3D yüzey grafikleri, hedeflere ve seçilen kas gruplarına göre egzersiz listesi üreten ve set sayılarını fuzzy çıktı hacmine (dakika) göre dinamik ayarlayan Akıllı Antrenman Üreteci ve antrenman geçmişini kaydedip CSV formatında indirmeyi sağlayan bir performans takip paneli geliştirdim."

### Slide 9: Live Demo & Q&A
* **Visual:** "Live Demo" ve "Thank You! / Questions?" yazısı.
* **Speaker Notes:** "Şimdi sistemin canlı olarak nasıl çalıştığına, kuralların nasıl hesaplandığına ve ürettiği dinamik antrenman programına hep birlikte bakalım. Dinlediğiniz için teşekkürler, sorularınız varsa alabilirim."
