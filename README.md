Nama : Arya Dwipa Wicaksana
NPM : 2506623111
Kelas : PBP E

### Tugas 1
Saya memakai Gemini untuk membantu mengerjakan  tugas ini sebagai alat bantu untuk mempelajari sintaks dan dokumentasi HTML/CSS.

1. Ya, saya menggunakan elemen semantik seperti header, nav, section, main, dan footer. Elemen semantik ini memudahkan saya untuk membagi halaman menjadi bagian-bagian yang lebih jelas dan terstruktur sehingga memudahkan saya untuk membaca ulang kode dan menambahkan fitur baru. 

2. Tantangan yang saya temukan seperti saat saya menaruh gambar tetapi gambar itu malah gepeng atau melebar sehingga terlihat aneh, saat ada gambar yang tidak sejarar dengan tulisan yang disebelahnya, atau ketika tulisan selalu melebar kesamping tidak kebawah. Saya mengevaluasi elemen mana yang harus diubah dengan bantuan inspect untuk membantu elemen mana yang perlu disesuaikan ukurannya.

3. Batasan yang saya rasakan adalah tidak bisanya untuk mengupdate data secara langsung dari web dan hanya bisa mengupdate data langsung melalui kodenya saja. Berdasarkan batasan tersebut, hal yang ingin saya buat selanjutnya adalah membuat fitur yang bisa langsung menambahkan data baru tanpa harus mengubah kode secara langsung

### Tugas 2
Saya memakai Gemini untuk membantu mengerjakan  tugas ini sebagai alat bantu mengeksplor lebih tentang django app seperti bagaimana caranya untuk membuat superuser yang juga bisa di up ke PWS dan bagaimana cara langsung  memasukkan data foto ke superuser.

1. Saat halaman portofolio dibuka oleh user di browser, browser akan mengirimkan HTTP request ke server yang akan diterima oleh urls.py proyek yang akan memeriksa path URL dasar dan mengarahkannya ke urls.py aplikasi yang sesuai. Kemudian, urls.py aplikkasi ini akan mengarahkan path URL tersebut ke kelas view yang bertugas untuk meminta pengambilan data portofolio dengan memanggil model yang akan mengambil datanya dari database. Setelah itu, view akan menyusun data dari model ke dalam variabel context, lalu mengirimkannya ke template.

2. Data untuk portofolio baru sebaiknya disimpan pada model karena ini akan memudahkan dalam memperbarui atau membenarkan data secara langsung tanpa harus masuk ke codenya, terutama jika sudah membuat superuser admin. Misalnya, saya tiba-tiba mendapatkan data baru dan ingin menambahkan sata itu sekarang juga tetapi tidak membawa laptop, dengan adanya model saya bisa langsung mengupdatenya lewat terminal pws di HP atau jika sudah membuat superuser admin, saya bisa langsung update datanya lewat namalink/admin tanpa harus repot-repot membuka laptop dan menambahkan datanya secara manual di file html.

3. Perbedaan dari makemigrations dan migrate adalah makemigrations baru bertugas membaca perubahan pada model.py dan membuat blueprint baru saja, sedangkan migrate memiliki tugas untuk menjalankan instruksi dari blueprint tersebut dan mengaplikasikan perubahannya ke database.
Contoh yang menjalankan kedua perintah itu adalah ketika saya menambahkan model baru, mengubah tipe field, menambah atau menghapus atribut/kolom, atau mengubah opsi field fi models.py, setiap kali saya melakukan itu, saya harus menjalankan perintah makemigrations dan migrate agar model dapat digunakan.

### Tugas 3
Saya memakai Gemini untuk membantu dalam pembuatan bagaimana caranya agar Create, Update, dan Delete hanya bisa diakses untuk yang memiliki password.

1. ModelForm digunakan karena di ModelForm itu udah otomatis membuat field form yang sesuai dengan field yang dibuat di model, sehingga tidak perlu ditulis ulang satu per satu di HTML. Selain itu, ada juga method/fungsi bawaan dari ModelForm yang memudahkan seperti is_valid() yang bisa ngecek kevalidan data atau save() yang berguna untuk pembuatan atau pembaruan data.

csrf_token wajib ditambahkan karena token tersebut menghasilkan token rahasia pada setiap sesi pengguna. Saat form dikirim, Django akan memverifikasi tokennya, jika cocok diterima, jika tidak cocok ditolak.

2. JSON lebih disukai karena file JSON lebih enak dilihat dan mudah dibaca karena berbentuk dictionary yang terdiri dari key-value, tidak seperti XML yang masih menggunakan tag, shingga kalau datanya banyak lebih tidak enak dilihat. Selain itu, JSON juga memiliki size file lebih kecil daripaa XML.

3. Pertama-tama, client mengirimkan request HTTP ke server Django. Setelah itu Django akan menyocokkan URL request dengan route yang sesuai di urls.py dan mengirimkan request tersebut ke view yang sesuai. View akan mengambil data dari database menggunakan Django ORM, seperti objects.all() yang akan mereturn QuerySet yang berisikan instance dari suatu objek. Karena tipe data QuerySet python tidak bisa langsung diubah ke JSON, data ini harus dizerialization dulu ke tipe data primitif python, disinilah zerialization diperlukan untuk mengubahnya menjadi JSON. Setelah dizerialization, data akan direturn ke client dengan header.