import streamlit as st
import pandas as pd
import yfinance as yf

st.set_page_config(page_title="المستشار المالي الذكي", page_icon="📈", layout="wide")

st.title("🛡️ نظام الاستثمار الذكي وعداد الحراسة اللحظي")
st.markdown("مؤسستك المالية المتكاملة: طاقة، مقاولات، تجارة، وصناعة.")

st.sidebar.header("🌐 رادار القطاعات الإقليمية")
market_choice = st.sidebar.selectbox("اختر القطاع أو السوق:", [
    "إدخال يدوي (رمز حُر)",
    "قطر (طاقة - قطر للغاز)",
    "المقاولات والبنية التحتية",
    "التجارة والصناعة (تصنيع وسلع)",
    "الأسواق الإقليمية (مصر/السعودية/الكويت/الإمارات)"
])

# تحديد الرمز الافتراضي بناءً على الاختيار
if "قطر" in market_choice: default_ticker = "IQCD.QA"
elif "المقاولات" in market_choice: default_ticker = "SWDY.CA"
elif "التجارة" in market_choice: default_ticker = "ORWE.CA"
elif "الإقليمية" in market_choice: default_ticker = "COMI.CA"
else: default_ticker = "NVDA"

ticker_symbol = st.text_input("رمز السهم:", value=default_ticker)
risk_threshold = st.slider("حد الأمان للذبذب:", 0.01, 0.10, 0.03)

if st.button("ابدأ تحليل الخبير 🚀"):
    try:
        stock = yf.Ticker(ticker_symbol)
        df = stock.history(period="1mo")
        if df.empty:
            st.error("تأكد من رمز السهم واللاحقة (مثل .CA, .QA, .DU).")
        else:
            c = df['Close'].iloc[-1]
            vol = df['Close'].pct_change().std()
            ma = df['Close'].rolling(20).mean().iloc[-1]
            
            c1, c2, c3 = st.columns(3)
            c1.metric("السعر", f"{c:.2f}")
            c2.metric("التقلب", f"{vol:.4f}")
            c3.metric("المتوسط", f"{ma:.2f}")
            
            if vol > risk_threshold:
                st.warning(f"⚠️ تنبيه مخاطر لسهم {ticker_symbol}")
                st.success(f"💡 البديل المقترح: توجه لقطاع أكثر استقراراً.")
            else:
                st.success(f"✅ سهم {ticker_symbol} في منطقة الأمان.")
    except Exception as e:
        st.error(f"خطأ: {e}")
