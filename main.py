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

# 2. Masukkan fungsi ke dalam tools chat
chat = client.chats.create(
    model="gemini-3.5-flash",
    config={
        "tools": [tulis_catatan]

    }
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