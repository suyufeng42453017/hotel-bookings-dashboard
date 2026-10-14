import pandas as pd
import streamlit as st

st.set_page_config(page_title="Hotel Bookings Dashboard", layout="wide")
st.title("Team Overbooked — Hotel Bookings Dashboard")
st.caption(
    "For the **revenue manager of one hotel**: watch cancellation risk and seasonal "
    "rate levels to set deposit rules and overbooking limits for the coming season."
)

MONTHS = ["January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]

@st.cache_data
def load():
    df = pd.read_csv("hotels.csv")
    df["arrival_month"] = pd.Categorical(df["arrival_date_month"], MONTHS, ordered=True)
    df["lead_time_bucket"] = pd.cut(
        df["lead_time"], [0, 7, 30, 90, 180, 1000],
        labels=["<= 1 week", "1 week – 1 month", "1–3 months", "3–6 months", "> 6 months"])
    return df

df = load()
hotel = st.radio("Hotel", ["City Hotel", "Resort Hotel"], horizontal=True)
d = df[df["hotel"] == hotel]

c1, c2, c3 = st.columns(3)
c1.metric("Bookings", f"{len(d):,}")
c2.metric("Cancellation rate", f"{d['is_canceled'].mean():.1%}")
c3.metric("Avg nightly rate (ADR)", f"${d['adr'].mean():.2f}")

left, right = st.columns(2)
with left:
    st.subheader("Cancellation rate by arrival month")
    st.line_chart(d.groupby("arrival_month", observed=True)["is_canceled"].mean(), y_label="share cancelled")
with right:
    st.subheader("Cancellation rate by booking lead time")
    st.bar_chart(d.groupby("lead_time_bucket", observed=True)["is_canceled"].mean(), y_label="share cancelled")

st.caption(
    "Data: Jul 2015 – Aug 2017 (Kaggle snapshot, *hotel-booking-demand*; 2015 and 2017 are partial years). "
    "In production: refreshed nightly from the property management system and reviewed every Monday "
    "before the weekly pricing meeting; a next-30-day cancellation rate above 45% triggers a same-day alert."
)
