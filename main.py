from google import genai
import os

client = genai.Client()
print("AI Agent dengan tools siap dijalankan!")

# 1. Bikin fungsi yang bisa dieksekusi sama si agent
def tulis_catatan(nama_file: str, isi_catatan: str):
    """Menyimpan catatan penting ke dalam file teks lokal di komputer.

    Args:
        nama_file: Nama file teks (contoh: tugas.text atau catatan text)
        isi_catatan: Teks atau isi catatan yang ingin disimpan ke dalam file
        """
    try:
        with open(nama_file, "w", encoding="utf-8") as f:
            f.write(isi_catatan)
        return f"Sukses! Catatan berhasil disimpan ke file '{nama_file}' di komputer."
    except Exception as e:
        return f"Gagal menyimpan file: {e}"

def baca_catatan(name_file:str):
    """Membaca isi file teks yang ada di folder proyek.
    Args:
        name_file: Nama file teks yang ingin di baca (contoh: 'catatan_text')
        """
    try: 
        with open (name_file, "r", encoding="utf-8") as f:
            isi = f.read()
            return f"Isi file {name_file}:\n{isi}"
    except Exception as e:
        return f"Gagal membaca file: {e}"

# 2. Masukkan fungsi ke dalam tools chat
chat = client.chats.create(
    model="gemini-3.5-flash",
    config={
        "tools": [tulis_catatan, baca_catatan],
        "system_instruction": (
            "Kamu adalah asisten Ai yang disiplin, aman, dan patuh."
            "Aturan ketat: "
            "1. Jangan pernah menulis file sembarangan atau di luar folder proyek."
            "2. Hanya gunakan tool 'tulis_catatan' jika benar-benar diperlukan untuk tugas yang diminta"
            "3. Selalu konfirmasi atau berikan penjelasan ringkas sebelum atau sesudah melakukan aksi."
        ),

    },
)

while True:
    user_input = input("kamu: ")
    
    if user_input.lower() == "keluar":
        print("AI Agent: Sampai jumpa!")
        break
        
    try:
        response = chat.send_message(user_input)
        print(f"AI Agent: {response.text}")
        
    except Exception as e:
        print(f"AI Agent: Waduh, servernya lagi sibuk atau error nih. (Info: {e})")