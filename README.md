# Hotel Bookings Dashboard — Team Overbooked

Streamlit dashboard for the Assignment 4 data-app exercise.

- **App:** `app.py` (run locally with `streamlit run app.py`)
- **Data:** `hotels.csv` (bundled, 16.9 MB)
- **EDA:** `hotel_eda.ipynb` (the Step 3 exploration, run on Kaggle with the dataset mounted; also runs locally)

## Step 1 — Dataset and decision-maker

**Dataset:** [Hotel booking demand](https://www.kaggle.com/datasets/jessemostipak/hotel-booking-demand) (Kaggle, mirror of the Science Direct repository of António et al., 2019). Real booking records of two European hotels (one city, one resort): 119,390 rows × 32 columns, **16.9 MB**, so no sampling was needed. **One row = one booking**, covering arrivals from July 2015 to August 2017.

**Decision-maker:** the **revenue manager of one hotel** — not "everyone". The first widget is a hotel selector (City / Resort) because everything else on the page changes with it.

## Step 2 — Why a dashboard

1. **Who, how often?** The revenue manager, once a week before the Monday pricing meeting, with a glance whenever a new alert fires.
2. **The decision it supports:** *"If the revenue manager sees the cancellation rate for upcoming months climbing past ~45%, they will tighten the deposit policy and raise the overbooking limit for those weeks."*
3. **What they do today without it:** pull ad-hoc booking reports from the property management system and eyeball them in Excel — slow, and easy to do inconsistently each week. Missed cancellation spikes mean empty rooms that could have been resold (overbooking too low) or turned-away guests and compensation (overbooking too high).
4. **Why a dashboard, not a report or alert?** The same question ("how risky are the next few weeks?") recurs every week with new data, and the answer needs context — seasonality and lead time — that a single number in an email can't show. The truly urgent condition is additionally covered by the alert in the caption line, so the dashboard is for review, not for watching in real time.

## Step 3 — What is on the page (and what is not)

The full exploration behind these decisions is in `hotel_eda.ipynb` (shape, dtypes, missing values, distributions, and the relationships that mattered). Findings that drove the page: bookings peak Jun–Aug while cancellation risk peaks Apr–Jun (~40–41% vs ~30% in winter); bookings made more than 6 months ahead cancel 57% of the time versus 11% for last-week bookings; the two hotels differ sharply (42% vs 28% cancellation); ADR is seasonal ($70 winter, $140 August).

Layout is top-to-bottom by importance; a manager who never scrolls still gets the whole story.

- **Top — three headline metrics:** total bookings, cancellation rate, average nightly rate (ADR). Five-second answer to "is anything wrong right now?"
- **Middle — two charts explaining the cancellation KPI:** cancellation rate by arrival month (seasonality: it peaks in April–June at ~40–41% overall vs ~30% in winter) and by booking lead time (bookings made more than 6 months ahead cancel at ~57% vs ~11% for last-week bookings). Together they tell the manager *which* weeks are at risk and *why* — far-ahead bookings drive the risk.
- **One filter:** the hotel selector. A manager only ever looks at their own hotel; anything else (year, country, segment sliders) would add clicks, not decisions.
- **Bottom — deliberately empty.** A raw bookings table would be used by nobody in this workflow, so it is cut ("if this disappeared, would anyone notice?" — no).

**Two things we chose not to show:**

1. **Cancellations by country** (a striking EDA chart — some source markets cancel several times more often) — interesting, but a revenue manager of one hotel cannot act on guest nationality in the weekly pricing meeting.
2. **ADR by month as a chart.** ADR belongs in the metrics row as a level; the *decision* on this page is about cancellation risk, and a third chart diluted the two that matter.

**What could mislead, and how we handle it:**

- **2015 and 2017 are partial years** (data starts 2015-07, ends 2017-08). Year-over-year comparisons would be wrong, so there is no YoY metric and the caption states the period.
- **ADR has 1,960 rows ≤ 0** (likely complimentary stays) and one extreme outlier (5,400). They barely move the average but we flag that ADR is a simple mean, not revenue-adjusted.
- **The deposit paradox:** bookings with "Non Refund" deposits cancel at 99.4% in this data — a known quirk of this dataset (mostly automatic/group bookings), which would badly mislead anyone reading it as "deposits cause cancellations". We left deposit type off the page rather than show a misleading relationship we cannot explain from this data.
- The two hotels have very different cancellation rates (42% city vs 28% resort); showing them mixed would be meaningless, hence the filter is required, not optional.

## Step 4 — Refresh frequency

- **Data refresh: nightly** from the property management system. Bookings change every day, but no pricing decision here is made intraday, so real-time refresh would add cost without changing any decision.
- **Review: every Monday**, before the weekly pricing meeting — a different rhythm from the refresh, since the decisions are made in that meeting.
- **What triggers action:** the cancellation rate of bookings **arriving in the next 30 days**. Above **45%** for the city hotel (~40% for the resort, whose baseline is lower) → the manager acts the same day: tighten deposits and raise the overbooking limit for the affected weeks. This one condition becomes an alert, not a dashboard check.
- **Cost of stale data:** moderate but real. Next season's rates are set months ahead from the lead-time chart; a week-old picture of a fast-rising cancellation trend means overbooking limits set too low — unsold rooms — or too high — walked guests and compensation fees.
