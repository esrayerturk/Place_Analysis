import streamlit as st
import pandas as pd
import os
import numpy as np
from sklearn.neighbors import NearestNeighbors

# Veriyi yükleme
@st.cache_data
def load_data():
    data = pd.read_csv("PlacesAnalysis.csv")
    return data

data = load_data()

# Kullanıcı-Mekan Puanlama verisi
if "ratings_data" not in st.session_state:
    st.session_state["ratings_data"] = pd.DataFrame({
        "User ID": [],
        "Place Name": [],
        "Rating": []
    })

# Yeni mekanları saklamak için session_state
if "new_places" not in st.session_state:
    st.session_state["new_places"] = []

# Sidebar
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["Mekan Öneri", "Mekan Ekleme", "Puanlama Analizi", "Mekan Seçenekleri"])

# Mekan Öneri Page
if page == "Mekan Öneri":
    st.header("Mekan Öneri")
    
    # Başlık ve tanıtım
    st.title("Mekan Öneri Uygulaması")
    st.write("Fiyat, lokasyon ve etkinlik türüne göre mekan önerileri alın.")

    # Kullanıcı seçimleri
    event_type = st.selectbox("Etkinlik Türü Seçiniz", options=data["Event Type"].unique())
    location = st.selectbox("Lokasyon Seçiniz", options=data["Location"].unique())
    price_range = st.slider(
        "Maksimum Fiyat Aralığı",
        min_value=int(data["Price Range Unit"].min()),
        max_value=int(data["Price Range Unit"].max()),
    )

    # Yeni mekanları orijinal veri setine ekle
    if st.session_state["new_places"]:
        # Yeni mekanları bir DataFrame'e dönüştür
        new_places_df = pd.DataFrame(st.session_state["new_places"])
        # Orijinal veri seti ile birleştir
        full_data = pd.concat([data, new_places_df], ignore_index=True)
    else:
        full_data = data
    
    # Filtreleme
    filtered_data = full_data[
        (full_data["Event Type"] == event_type) &
        (full_data["Location"] == location) & 
        (full_data["Price Range Unit"] <= price_range)
    ]

    # Sonuçları gösterme
    st.write(f"Seçimlerinize göre bulunan mekanlar:")
    filtered_data["User Rating (1-5)"] = filtered_data["User Rating (1-5)"].round(1)
    st.dataframe(filtered_data[["Place Name", "Cuisine Type", "Price Range", "User Rating (1-5)"]])

    # Kullanıcı puanlarına göre sıralama
    if not filtered_data.empty:
        top_rated = filtered_data.sort_values(by="User Rating (1-5)", ascending=False).head(3)
        top_rated["User Rating (1-5)"] = top_rated["User Rating (1-5)"].round(1)
        st.subheader("En Yüksek Puanlı Mekanlar")
        st.table(
            top_rated[["Place Name", "User Rating (1-5)"]].style.format({"User Rating (1-5)": "{:.1f}"})
        )
    else:
        st.write("Maalesef, seçimlerinize uygun mekan bulunamadı.")

# Mekan Ekleme Page
elif page == "Mekan Ekleme":
    st.header("Mekan Ekleme")
    
    # Mekan ekleme formu
    with st.form("Yeni Mekan Ekle"):
        name = st.text_input("Mekan Adı")
        cuisine = st.selectbox("Mutfak Türü", options=data["Cuisine Type"].unique())
        event_type = st.selectbox("Event Type", options=data["Event Type"].unique())
        location = st.selectbox("Location", options=data["Location"].unique())
        price = st.slider("Fiyat Aralığı", 1, 5)
        rating = st.slider("Kullanıcı Puanı", 1.0, 5.0, step=0.1)
        submitted = st.form_submit_button("Ekle")

        if submitted:
            # Yeni mekan verisini session_state'e ekle
            new_place = {
                "Place Name": name,
                "Cuisine Type": cuisine,
                "Price Range": f"{price} - {price + 1}",
                "Price Range Unit": price,
                "User Rating (1-5)": rating,
                "Location": location,
                "Event Type": event_type
            }
            st.session_state["new_places"].append(new_place)
            st.success(f"{name} başarıyla eklendi!")      

# Puanlama Analizi Sekmesi
elif page == "Puanlama Analizi":
    st.header("Puanlama Analizi")

    # Puanlama verileri için dosya yolu
    ratings_file = "user_ratings.csv"

    # Daha önceki puanlama verilerini yükleme
    if os.path.exists(ratings_file):
        ratings_df = pd.read_csv(ratings_file)
    else:
        ratings_df = pd.DataFrame(columns=["User ID", "Place Name", "Rating"])

    # Mekan seçimi
    place_to_rate = st.selectbox("Puanlamak istediğiniz mekanı seçin", data["Place Name"].unique())

    # Seçilen mekanın geçmiş puanlarının ortalamasını gösterme
    if not ratings_df.empty and place_to_rate in ratings_df["Place Name"].values:
        avg_rating = ratings_df[ratings_df["Place Name"] == place_to_rate]["Rating"].mean()
        st.write(f"**{place_to_rate}** mekanının ortalama puanı: **{avg_rating:.1f}**")
    else:
        st.write(f"**{place_to_rate}** mekanının henüz puanı bulunmamaktadır.")

    # Kullanıcı puanı ekleme
    with st.form("Puanlama Formu"):
        user_id = st.text_input("Kullanıcı ID", placeholder="Örneğin: user123")
        new_rating = st.slider("Puanınız", min_value=1, max_value=5, step=1)
        submitted_rating = st.form_submit_button("Puanı Kaydet")

        if submitted_rating:
            if user_id.strip() == "":
                st.warning("Lütfen geçerli bir kullanıcı ID giriniz.")
            else:
                # Yeni puanı DataFrame'e ekleme
                new_entry = {"User ID": user_id, "Place Name": place_to_rate, "Rating": new_rating}
                ratings_df = pd.concat([ratings_df, pd.DataFrame([new_entry])], ignore_index=True)

                # CSV dosyasına kaydetme
                ratings_df.to_csv(ratings_file, index=False)
                st.success(f"{place_to_rate} mekanına verdiğiniz puan kaydedildi!")
    
    # Mekanların ortalama puanlarını hesaplama
    if not ratings_df.empty:
        avg_ratings = ratings_df.groupby("Place Name")["Rating"].mean().round(1).sort_values(ascending=False)
        st.subheader("Mekanların Ortalama Puanları")
        st.table(avg_ratings.reset_index().rename(columns={"Place Name": "Mekan", "Rating": "Ortalama Puan"}))

# Mekan Seçenekleri Sekmesi
elif page == "Mekan Seçenekleri":
    st.header("Mekan Seçenekleri")

    # Kullanıcı puanlama verisini kontrol et
    ratings_file = "user_ratings.csv"
    if os.path.exists(ratings_file):
        ratings_df = pd.read_csv(ratings_file)
    else:
        ratings_df = pd.DataFrame(columns=["User ID", "Place Name", "Rating"])

    if ratings_df.empty:
        st.write("Lütfen önce 'Puanlama Analizi' sekmesinde mekanlarınızı puanlayınız.")
    else:
        # Kullanıcı ID'si al
        user_id = st.text_input("Kullanıcı ID'nizi girin", placeholder="Örneğin: user123")
        if user_id.strip() == "":
            st.warning("Lütfen geçerli bir kullanıcı ID giriniz.")
        else:
            # Kullanıcının en yüksek puanladığı mekanlar
            user_ratings = ratings_df[ratings_df["User ID"] == user_id]
            if user_ratings.empty:
                st.write("Bu kullanıcı ID ile henüz puanlama yapılmamış.")
            else:
                top_rated = user_ratings[user_ratings["Rating"] == user_ratings["Rating"].max()]
                st.write("En Yüksek Puanladığınız Mekanlar:")
                st.dataframe(top_rated)
    
                # KNN Modeli için Veri Hazırlığı
                try:
                    # Tüm veri setini KNN için hazırlayın
                    data_knn = pd.get_dummies(data.drop(columns=["Place Name", "User Rating (1-5)"]))
    
                    # Kullanıcı tarafından puanlanan mekanları hazırlayın
                    data_subset = data[data["Place Name"].isin(user_ratings["Place Name"])]
                    data_subset_knn = pd.get_dummies(data_subset.drop(columns=["Place Name", "User Rating (1-5)"]))
    
                    # Eksik sütunları doldur (Eğitim ve test verileri uyumlu hale getirilir)
                    data_subset_knn = data_subset_knn.reindex(columns=data_knn.columns, fill_value=0)

                    # KNN Modelini Eğit
                    knn = NearestNeighbors(n_neighbors=5, metric="euclidean")
                    knn.fit(data_knn)

                    # Öneriler oluştur
                    try:
                        recommendations = []
                        for _, row in data_subset_knn.iterrows():
                            distances, indices = knn.kneighbors([row])
                            recommended_places = data.iloc[indices[0]].copy()
                            recommendations.append(recommended_places)

                        # Tüm önerileri birleştir ve tekrarlayan satırları kaldır
                        recommendations_df = pd.concat(recommendations).drop_duplicates(subset=["Place Name"])

                        # Önerilen mekanların bilgilerini göster
                        st.write("Önerilen Mekanlar:")
                        st.dataframe(recommendations_df[["Place Name", "Cuisine Type", "Price Range", "Location"]])

                    except Exception as e:
                        # Hata durumunda mesaj göster
                        st.error(f"KNN modeli öneri oluştururken bir hata meydana geldi: {str(e)}")

                except Exception as e:
                    # Dış try bloğu için hata mesajı
                    st.error(f"Veri hazırlama veya model eğitimi sırasında bir hata meydana geldi: {str(e)}")