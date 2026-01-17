import flet as ft
import pandas as pd
import random

def main(page: ft.Page):
    page.title = "KPSS Hazırlık"
    page.horizontal_alignment = "center"
    page.scroll = "adaptive"
    page.bgcolor = "#F0F2F5" # Açık gri arka plan

    state = {
        "veriler": [],
        "secilen_sorular": [],
        "current_index": 0,
        "dogru_sayisi": 0,
    }

    try:
        df = pd.read_excel("sorular.xlsx")
        df.columns = [str(col).strip().lower() for col in df.columns]
        state["veriler"] = df.to_dict('records')
    except Exception as e:
        page.add(ft.Text("Excel Hatası: " + str(e), color="red"))
        return

    def kategori_sec(e):
        # Butonun içindeki Text objesinden veriyi alıyoruz
        kat_adi = str(e.control.data).strip().lower()
        filtreli = [s for s in state["veriler"] if str(s.get('kategori', '')).strip().lower() == kat_adi]
        
        if not filtreli: return

        state["secilen_sorular"] = random.sample(filtreli, min(len(filtreli), 20))
        state["current_index"] = 0
        state["dogru_sayisi"] = 0
        
        ana_ekran.visible = False
        test_ekrani.visible = True
        soru_yukle()
        page.update()

    def soru_yukle():
        s = state["secilen_sorular"][state["current_index"]]
        soru_no.value = "SORU " + str(state["current_index"] + 1) + " / " + str(len(state["secilen_sorular"]))
        soru_metni.value = str(s.get('soru', ''))
        
        # BUTON METİNLERİNİ GÜNCELLEME (content.value kullanarak)
        # Bu yöntem en eski sürümlerde bile çalışır.
        btn_a.content.value = "A) " + str(s.get('a', ''))
        btn_b.content.value = "B) " + str(s.get('b', ''))
        btn_c.content.value = "C) " + str(s.get('c', ''))
        btn_d.content.value = "D) " + str(s.get('d', ''))
        btn_e.content.value = "E) " + str(s.get('e', ''))
        page.update()

    def cevap_ver(e):
        dogru = str(state["secilen_sorular"][state["current_index"]].get('cevap', '')).strip().lower()
        
        # Tıklanan butonun içindeki metni alıyoruz
        try:
            tiklanan_metin = e.control.content.value
            secilen = tiklanan_metin.split(") ", 1)[1].strip().lower()
        except:
            secilen = ""
        
        if secilen == dogru:
            state["dogru_sayisi"] += 1
        
        if state["current_index"] < len(state["secilen_sorular"]) - 1:
            state["current_index"] += 1
            soru_yukle()
        else:
            test_ekrani.visible = False
            sonuc_ekrani.visible = True
            skor_text.value = "DOĞRU: " + str(state["dogru_sayisi"])
            page.update()

    def ana_sayfaya_don(e):
        sonuc_ekrani.visible = False
        ana_ekran.visible = True
        page.update()

    # --- UI OLUŞTURMA ---
    
    # 1. ANA EKRAN
    kat_listesi = sorted(list(set([str(s.get('kategori', '')).strip() for s in state["veriler"] if pd.notna(s.get('kategori'))])))
    
    ana_ekran_items = [
        ft.Text("KPSS SINAV MERKEZİ", size=28, weight="bold", color="#1565C0"),
        ft.Divider(),
    ]

    for k in kat_listesi:
        # Buton oluştururken text parametresi YERİNE content kullanıyoruz
        btn = ft.ElevatedButton(
            content=ft.Text(k, size=16),
            data=k, # Veriyi burada saklıyoruz
            on_click=kategori_sec,
            bgcolor="#1976D2",
            color="white",
            width=300,
            height=50
        )
        ana_ekran_items.append(btn)

    ana_ekran = ft.Column(controls=ana_ekran_items, horizontal_alignment="center", visible=True)

    # 2. TEST EKRANI
    soru_no = ft.Text("", size=16, color="#0D47A1", weight="bold")
    soru_metni = ft.Text("", size=20, text_align="center", weight="w500")

    # Şık Butonlarını Content Wrapper ile oluşturuyoruz
    # text="A" YERİNE content=ft.Text("A") yazıyoruz. Hata buradan geliyordu.
    btn_a = ft.ElevatedButton(content=ft.Text(""), on_click=cevap_ver, width=350, height=55, bgcolor="white", color="black")
    btn_b = ft.ElevatedButton(content=ft.Text(""), on_click=cevap_ver, width=350, height=55, bgcolor="white", color="black")
    btn_c = ft.ElevatedButton(content=ft.Text(""), on_click=cevap_ver, width=350, height=55, bgcolor="white", color="black")
    btn_d = ft.ElevatedButton(content=ft.Text(""), on_click=cevap_ver, width=350, height=55, bgcolor="white", color="black")
    btn_e = ft.ElevatedButton(content=ft.Text(""), on_click=cevap_ver, width=350, height=55, bgcolor="white", color="black")

    test_ekrani = ft.Column(
        controls=[
            ft.Container(height=20),
            soru_no,
            ft.Container(
                content=soru_metni,
                padding=20,
                bgcolor="white",
                border=ft.border.all(1, "#BBDEFB"),
                border_radius=15,
                margin=ft.margin.only(bottom=20)
            ),
            btn_a, btn_b, btn_c, btn_d, btn_e
        ],
        horizontal_alignment="center",
        visible=False
    )

    # 3. SONUÇ EKRANI
    skor_text = ft.Text("", size=30, weight="bold", color="#2E7D32")
    sonuc_ekrani = ft.Column(
        controls=[
            ft.Container(height=50),
            ft.Text("SINAV TAMAMLANDI", size=24),
            skor_text,
            ft.ElevatedButton(
                content=ft.Text("ANA SAYFAYA DÖN"),
                on_click=ana_sayfaya_don,
                bgcolor="#1565C0",
                color="white",
                width=200
            )
        ],
        horizontal_alignment="center",
        visible=False
    )

    page.add(ana_ekran, test_ekrani, sonuc_ekrani)

ft.app(target=main)
