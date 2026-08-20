
import streamlit as st
import pandas as pd
import yfinance as yf

st.set_page_config(page_title="المستشار المالي الذكي", page_icon="📈", layout="wide")

st.title("🛡️ نظام الاستثمار الذكي وعداد الحراسة اللحظي")
st.markdown("منظومة تحليل الأسواق الإقليمية والعالمية: القطاعات ⬅️ الدول ⬅️ الأسهم مع تقرير تحليل خبير مفصل.")

# الهيكل الهرمي للقطاعات والدول والأسهم الأكثر دقة وثباتاً في جلب البيانات
st.sidebar.header("🌐 رادار الأسواق الإقليمية الهرمي")

sector_choice = st.sidebar.selectbox("1️⃣ اختر القطاع الرئيسي:", [
    "الأسهم العالمية والتكنولوجية",
    "طاقة وبتروكيماويات",
    "مقاولات وبنية تحتية",
    "تجارة وصناعة وبنوك (مصر والسعودية)"
])

database = {
    "الأسهم العالمية والتكنولوجية": {
        "أمريكا والعالم": {"إنفيديا (NVDA)": "NVDA", "أبل (AAPL)": "AAPL", "مايكروسوفت (MSFT)": "MSFT"}
    },
    "طاقة وبتروكيماويات": {
        "السعودية": {"أرامكو السعودية": "2222.SR", "سابك": "2010.SR"},
        "الولايات المتحدة (مؤشر طاقة)": {"إكسجون موبيل": "XOM"}
    },
    "مقاولات وبنية تحتية": {
        "مصر": {"السويدي إليكتريك": "SWDY.CA", "أوراسكوم للتنمية": "ORHD.CA"},
        "الإمارات": {"إعمار العقارية": "EMAAR.DU"}
    },
    "تجارة وصناعة وبنوك (مصر والسعودية)": {
        "مصر": {"البنك التجاري الدولي (CIB)": "COMI.CA", "النساجون الشرقيون": "ORWE.CA", "حديد عز": "ESRS.CA"},
        "السعودية": {"مصرف الراجحي": "1120.SR", "البنك الأهلي السعودي": "1180.SR"}
    }
}

available_countries = list(database[sector_choice].keys())
country_choice = st.sidebar.selectbox("2️⃣ اختر الدولة / السوق:", available_countries)

available_stocks = database[sector_choice][country_choice]
stock_name_choice = st.sidebar.selectbox("3️⃣ اختر السهم:", list(available_stocks.keys()))

selected_ticker = available_stocks[stock_name_choice]

st.sidebar.markdown("---")
risk_threshold = st.slider("حدد حد الأمان للذبذب:", 0.01, 0.10, 0.03)

st.markdown(f"### 📊 الرمز قيد التحليل حالياً: `{selected_ticker}` ({stock_name_choice})")

if st.button("🚀 ابدأ تحليل الخبير الشامل"):
    with st.spinner("جاري الاتصال بالأسواق وجلب البيانات اللحظية..."):
        try:
            stock = yf.Ticker(selected_ticker)
            df = stock.history(period="3mo")
            
            if df.empty or 'Close' not in df.columns or df['Close'].dropna().empty:
                st.error("⚠️ عذراً، تعذر جلب بيانات حية لهذا السهم حالياً من المصدر. يجدر التجربة بأسهم أخرى متاحة في القائمة.")
            else:
                current_price = df['Close'].iloc[-1]
                prev_price = df['Close'].iloc[-2] if len(df) > 1 else current_price
                price_change = ((current_price - prev_price) / prev_price) * 100 if prev_price else 0.0
                
                returns = df['Close'].pct_change().dropna()
                volatility = returns.std() if not returns.empty else 0.0
                ma_20 = df['Close'].rolling(window=20).mean().iloc[-1] if len(df) >= 20 else current_price
                ma_50 = df['Close'].rolling(window=50).mean().iloc[-1] if len(df) >= 50 else ma_20
                
                # لوحات المؤشرات الحية مع التحقق من القيم
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("السعر الحالي", f"${current_price:.2f}", f"{price_change:+.2f}%")
                col2.metric("مؤشر التقلب", f"{volatility:.4f}")
                col3.metric("متوسط 20 يوم", f"${ma_20:.2f}")
                col4.metric("متوسط 50 يوم", f"${ma_50:.2f}")
                
                st.markdown("---")
                st.subheader("🧐 تقرير تحليل الخبير الفني والمالي:")
                
                analysis_report = []
                
                if current_price > ma_20:
                    analysis_report.append(f"• **الاتجاه قصير الأجل:** السعر الحالي ({current_price:.2f}) يتداول **أعلى** متوسط الـ 20 يوم ({ma_20:.2f})، مما يعكس الزخم الإيجابي وزخم الشراء على المدى القصير.")
                else:
                    analysis_report.append(f"• **الاتجاه قصير الأجل:** السعر الحالي ({current_price:.2f}) يتداول **أسفل** متوسط الـ 20 يوم ({ma_20:.2f}), وهو مؤشر على ضغوط بيعية أو تصحيح هابط مؤقت.")
                
                if volatility > risk_threshold:
                    analysis_report.append(f"• **تقييم المخاطر:** معدل التقلب الحالي ({volatility:.4f}) **يتجاوز** حد الأمان المحدد ({risk_threshold}). السهم يُظهر تذبذبات عالية ومخاطر مرتفعة تتطلب إدارة رأس مال حذرة.")
                else:
                    analysis_report.append(f"• **تقييم المخاطر:** معدل التقلب ({volatility:.4f}) ضمن نطاق الأمان المستهدف ({risk_threshold}). الأداء السعري مستقر نسبياً ومناسب للمستثمرين متوسطي الحذر.")
                
                if ma_20 > ma_50:
                    analysis_report.append(f"• **هيكل الاتجاه العام:** المتوسط المتحرك لـ 20 يوماً أعلى من الـ 50 يوماً، مما يدعم استمرار الهيكل الإيجابي على المدى المتوسط.")
                else:
                    analysis_report.append(f"• **هيكل الاتجاه العام:** المتوسط المتحرك لـ 20 يوماً أدنى من الـ 50 يوماً، مما يشير إلى مسار عرضي هابط يستوجب الحذر والمراقبة اللحظية.")

                for line in analysis_report:
                    st.markdown(line)
                
                st.markdown("---")
                if volatility > risk_threshold:
                    st.warning("⚠️ **توصية الخبير:** السهم في منطقة عالية المخاطر. يُنصح بتفعيل أوامر وقف الخسارة أو تقليص المراكز المالية والبحث عن بدائل استثمارية أكثر تحوطاً.")
                else:
                    st.success("✅ **توصية الخبير:** الوضع الفني مستقر ومناسب للاحتفاظ أو بناء مراكز استثمارية تدريجية وفق خطة المحفظة.")
                
        except Exception as e:
            st.error(f"حدث خطأ تقني أثناء معالجة البيانات: {e}")
