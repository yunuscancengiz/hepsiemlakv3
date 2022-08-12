import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

txt_file =  input("txt dosyası: ")
with open(txt_file, "r", encoding="utf-8") as file:
    for line in file:
        list_for_excel = list()
        line = line.strip()
        line = line.split(",")
        excel_file = line[0]
        starting_page = line[1]
        ending_page = line[2]
        total_page = line[3]
        f_website_url = line[4]
        
        starting_page = int(starting_page)
        ending_page = int(ending_page)
        total_page = int(total_page)

        try:
            # ALINAN LİNKTEKİ SAYFALARA GİDEREK İLAN LİNKLERİNİ ÇEKEN VE LİSTEYE ATAN KISIM
            headers = {
                "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36", 
                "X-Amzn-Trace-Id": "Root=1-6209086d-6b68c17b4f73e9d6174b5736"
            }

            if(ending_page > total_page):
                ending_page = total_page

            urls = list()
            url_counter = 1
            while(starting_page <= ending_page):
                print("\n------------------------\n")
                print("SAYFA: " + str(starting_page))
                website_url = f"{f_website_url}?page={str(starting_page)}"
                print(website_url)
                print("\n------------------------\n")

                r = requests.get(website_url, headers=headers)
                soup = BeautifulSoup(r.content, "lxml")

                adv_urls = soup.find_all("a", attrs={"class":"card-link"})
                for i in adv_urls:
                    adv_url = "https://www.hepsiemlak.com" + i.get("href")
                    urls.append(adv_url)
                    print(str(url_counter) + ") " + adv_url)
                    url_counter += 1
                    
                starting_page += 1
                website_url = f_website_url
                time.sleep(1.2)

            print("\nİLAN LİNKLERİ ALINDI, VERİ ÇEKMEYE BAŞLIYORUZ...\n")
            time.sleep(3)


            # ÇEKİLEN İLAN LİNKLERİNE TEKER TEKER GİDİP VERİSİNİ ÇEKECECEK KISIM
            counter = 1
            for url in urls:
                headers = {
                "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36", 
                "X-Amzn-Trace-Id": "Root=1-6209086d-6b68c17b4f73e9d6174b5736"
                }

                r = requests.get(url, headers=headers)
                soup = BeautifulSoup(r.content, "lxml")
                ilan_url = url

                print("\n-----------------------------------\n" + str(counter))
                print("Link: " + ilan_url)
                try:
                    name = soup.find("div", attrs={"class":"firm-link fontRB"}).getText().strip().replace("\n", " ").replace("               ", " ").split("Mesleki")
                    name = name[0]
                except:
                    name = soup.find("div", attrs={"class":"owner-firm-name fontRB mb10"}).getText().strip()
                print("Satıcı: " + name)

                title = soup.find("h1", attrs={"class":"fontRB"}).getText().strip()
                print("İlan Başlığı: " + title)

                try:
                    seller = soup.find("div", attrs={"class":"firm-link"}).getText().strip().replace("\n", " ").replace("               ", " ").split("Mesleki")
                    seller = seller[0]
                except:
                    seller = soup.find("span", attrs={"class":"owner-member-type mr10"}).getText().strip()
                print("Emlak Şirketi: " + seller)

                price = soup.find("p", attrs={"class":"fontRB fz24 price"}).getText().strip()
                print("Fiyat: " + price)

                try:
                    state1 = soup.find("ul", attrs={"class":"short-info-list"})
                    state2 = state1.find_all("li")
                    short_info_list = list()
                    for info in state2:
                        info = info.getText().strip()
                        short_info_list.append(info)

                    sehir = short_info_list[0]
                    ilce = short_info_list[1]
                    mahalle = short_info_list[2]
                except:
                    sehir = "-"
                    ilce = "-"
                    mahalle = "-"

                ilan_no = "-"
                ilan_durumu = "-"
                konut_sekli = "-"
                oda_salon_sayisi = "-"
                brut_net_m2 = "-"
                bulundugu_kat = "-"
                bina_yasi = "-"
                isinma_tipi = "-"
                kat_sayisi = "-"
                metrekare = "-"
                kredi_durumu = "-"
                esya_durumu  = "-"
                yapi_tipi = "-"
                yapi_durumu = "-"
                aidat  = "-"
                cephe = "-"
                tapu_durumu = "-"
                kira_getirisi = "-"
                depozito = "-"
                yakit_tipi = "-"

                st1 = soup.find_all("ul", attrs={"class":"adv-info-list"})
                for i in st1:
                    st2 = i.find_all("li", attrs={"class":"spec-item"})
                    for j in st2:
                        detail = j.getText().strip()

                        if("İlan no" in detail):
                            ilan_no = detail.lstrip("İlan no ")
                            
                        if("İlan Durumu" in detail):
                            ilan_durumu = detail.lstrip("İlan Durumu ")
                            
                        if("Konut Şekli" in detail):
                            konut_sekli = detail.lstrip("Konut Şekli ")
                            
                        if("Bulunduğu Kat" in detail):
                            bulundugu_kat = detail.lstrip("Bulunduğu Kat ")
                            
                        if("Bina Yaşı" in detail):
                            bina_yasi = detail.lstrip("Bina Yaşı ")
                            
                        if("Isınma Tipi" in detail):
                            isinma_tipi = detail.lstrip("Isınma Tipi ")
                            
                        if("Kat Sayısı" in detail):
                            kat_sayisi = detail.lstrip("Kat Sayısı ")
                            
                        if("Oda + Salon Sayısı" in detail):
                            oda_salon_sayisi = detail.lstrip("Oda + Salon Sayısı ")

                        if("Brüt / Net M2" in detail):
                            brut_net_m2 = detail.lstrip("Brüt / Net M2 ").strip()

                        if("Metrekare" in detail and "m2" in detail):
                            metrekare = detail.lstrip("Metrekare ")
                        
                        if("Krediye Uygunluk" in detail):
                            kredi_durumu = detail.split(" ")
                            kredi_durumu = kredi_durumu[2]
                            
                        if("Eşya Durumu" in detail):
                            esya_durumu = detail.split("Durumu ")
                            esya_durumu = esya_durumu[1]
                            
                        if("Yapı Tipi" in detail):
                            yapi_tipi = detail.lstrip("Yapı Tipi ")
                            
                        if("Yapının Durumu" in detail):
                            yapi_durumu = detail.lstrip("Yapının Durumu ")
                            
                        if("Aidat" in detail):
                            aidat = detail.strip("Aidat ")
                            
                        if("Cephe" in detail):
                            cephe = detail.lstrip("Cephe ")
                        
                        if("Tapu Durumu" in detail):
                            tapu_durumu = detail.lstrip("Tapu Durumu ")
                        
                        if("Kira Getirisi" in detail):
                            kira_getirisi = detail.lstrip("Kira Getirisi ")
                            
                        if("Depozito" in detail):
                            depozito = detail.lstrip("Depozito ")
                            
                        if("Yakıt Tipi" in detail):
                            yakit_tipi = detail.lstrip("Yakıt Tipi ")

                # İLAN VERİLERİ ÇEKİLİRKEN CMD ÜZERİNDE AKACAK OLAN VERİLER
                print("İlan no: " + ilan_no)
                print("Şehir: " + sehir)
                print("İlçe: " + ilce)
                print("Mahalle: " + mahalle)
                print("İlan Durumu: " + ilan_durumu)
                print("Konut Şekli: " + konut_sekli)
                print("Bulunduğu kat: " + bulundugu_kat)
                print("Bina Yaşı: " + bina_yasi)
                print("Isınma Tipi: " + isinma_tipi)
                print("Kat Sayısı: " + kat_sayisi)
                print("Oda + Salon Sayısı: " + oda_salon_sayisi)
                print("Brüt / Net M2: " + brut_net_m2)
                print("Metrekare: " + metrekare)
                print("Krediye Uygunluk: " + kredi_durumu)
                print("Eşya Durumu: " + esya_durumu)
                print("Yapı Tipi: " + yapi_tipi)
                print("Yapının Durumu: " + yapi_durumu)
                print("Aidat: " + aidat)
                print("Cephe: " + cephe)
                print("Tapu Durumu: " + tapu_durumu)
                print("Kira Getirisi: " + kira_getirisi)
                print("Depozito: " + depozito)
                print("Yakıt Tipi: " + yakit_tipi)

                # İLAN VERİLERİNİ DICTIONARY TİPİNDE TUTYORUZ
                advert_infos = {
                    "İlan no":ilan_no,
                    "Konut Şekli":konut_sekli,
                    "Satıcı":name,
                    "İlan Başlığı":title,
                    "Fiyat":price,
                    "Link":ilan_url,
                    "İlan Durumu":ilan_durumu,
                    "Şehir":sehir,
                    "İlçe":ilce,
                    "Mahalle":mahalle,
                    "Emlakçı":seller,         
                    "Bulunduğu kat":bulundugu_kat,
                    "Bina Yaşı":bina_yasi,
                    "Isınma Tipi":isinma_tipi,
                    "Kat Sayısı":kat_sayisi,
                    "Oda + Salon Sayısı":oda_salon_sayisi,
                    "Brüt / Net M2":brut_net_m2,
                    "Metrekare":metrekare,
                    "Krediye Uygunluk":kredi_durumu,
                    "Eşya Durumu":esya_durumu,
                    "Yapı Tipi":yapi_tipi,
                    "Yapının Durumu":yapi_durumu,
                    "Aidat":aidat,
                    "Cephe":cephe,
                    "Tapu Durumu":tapu_durumu,
                    "Kira Getirisi":kira_getirisi,
                    "Depozito":depozito,
                    "Yakıt Tipi":yakit_tipi,
                }
                list_for_excel.append(advert_infos)
                print("\n-------------------------------------\n")

                counter += 1
                time.sleep(1.2)
        except:
            print("HATA ALINDI PROGRAMDAN ÇIKILIYOR....")
        finally:
            # ÇEKİLEN VERİLERİ EXCEL DOSYASINA ÇEVİREN KISIM
            print("\nVeri çekme işlemi tamamlandı...\nÇekilen veriler Excel dosyasına dönüştürülüyor...")
            file_name = excel_file + ".xlsx"
            df_data = pd.DataFrame(list_for_excel)
            df_data.to_excel(file_name, index = False)
            print("\n******************************************\nVeriler Excel dosyasına dönüştürüldü...\n******************************************\n")
            print("PROGRAM SONLANDI")