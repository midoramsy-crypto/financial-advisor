import streamlit as st
import yfinance as yf
import pandas as pd

# إعدادات الصفحة الأساسية
st.set_page_config(page_title="المستشار المالي الذكي", page_icon="📈", layout="centered")

st.title("🛠️ نظام الاستثمار الذكي وعداد الحراسة اللحظي")
st.write("أهلاً بك يا باشا في مؤسستك المالية. هنا يتم تحليل المخاطر، تقديم البدائل، ومتابعة العدادات الحية لأموالك.")

# تهيئة الذاكرة المؤقتة (RAM Session State) للعدادات
if 'portfolio_ram' not in st.session_state:
    st.session_state.portfolio_ram = {}  # لتخزين { 'Ticker': سعر_الشراء }

# نظام التبويب بين فحص الأسهم ومتابعة المحفظة الحية
tab1, tab2, tab3 = st.tabs(["🔍 فحص سهم جديد", "📊 عداد المحفظة الحية (RAM)", "💼 نموذج الشراكة والأرباح"])

with tab1:
    st.subheader("رادار فحص الأسهم والبدائل الذكية")
    user_ticker = st.text_input("أدخل رمز السهم للاستشارة (مثلاً: NVDA, AAPL, MSFT):", value="NVDA").upper()
    safe_limit = st.slider("حدد حد الأمان للتذبذب:", 0.01, 0.05, 0.03, 0.005)

    if st.button("🚀 ابدأ تحليل الخبير"):
        with st.spinner("جاري فحص الشاشات والأسواق..."):
            try:
                stock = yf.Ticker(user_ticker)
                data = stock.history(period="3mo")
                
                if data.empty:
                    st.error(f"❌ الرمز ({user_ticker}) غير صحيح أو البيانات غير متوفرة.")
                else:
                    volatility = data['Close'].pct_change().std()
                    latest_price = float(data['Close'].iloc[-1])
                    ma20 = float(data['Close'].rolling(window=20).mean().iloc[-1])
                    
                    col1, col2, col3 = st.columns(3)
                    col1.metric("السعر الحالي", f"${latest_price:.2f}")
                    col2.metric("مؤشر التقلب", f"{volatility:.4f}")
                    col3.metric("متوسط 20 يوم", f"${ma20:.2f}")
                    
                    st.markdown("---")
                    
                    if volatility <= safe_limit and latest_price >= ma20:
                        st.success(f"✅ **قرار الخبير:** سهم ({user_ticker}) مستقر ومناسب للاستثمار الآن!")
                        
                        # زر لإضافة السهم مباشرة للعداد الحي
                        buy_price_input = st.number_input("أدخل سعر الشراء الفعلي لتسجيله في العداد:", value=latest_price, key="direct_buy")
                        if st.button("➕ تسجيل في عداد الحراسة"):
                            st.session_state.portfolio_ram[user_ticker] = buy_price_input
                            st.success(f"تم إدراج سهم {user_ticker} في عداد المراقبة الحية بنجاح!")
                    else:
                        st.warning(f"⚠️ **تنبيه:** سهم ({user_ticker}) يحمل مخاطر عالية حالياً.")
                        st.info("🔍 جاري رصد البديل الذهبي في السوق...")
                        
                        watchlist = ["AAPL", "MSFT", "XOM", "CAT", "DE", "WMT", "KO", "PG"]
                        best_alt = None
                        min_vol = 999
                        
                        for alt in watchlist:
                            if alt == user_ticker: 
                                continue
                            alt_data = yf.Ticker(alt).history(period="3mo")
                            alt_vol = alt_data['Close'].pct_change().std()
                            if alt_vol < min_vol and alt_vol < safe_limit:
                                min_vol = alt_vol
                                best_alt = alt
                                
                        if best_alt:
                            st.markdown(f"💎 **البديل المقترح:** توجه فوراً لسهم (**{best_alt}**) لاستقرار ومخاطر أقل ({min_vol:.4f}).")
                        else:
                        
                            st.error("💡 نصيحة الخبير: السوق ككل غير مستقر، احتفظ بالسيولة كاش.")

            except Exception as e:
                st.error(f"حدث خطأ أثناء المعالجة: {e}")

with tab2:
    st.subheader("📊 لوحة الحراسة اللحظية (تعمل بكفاءة داخل الـ RAM)")
    st.write("هنا يتم تتبع الأرباح والخسائر للأسهم المسجلة بشكل لحظي بدون استهلاك هارد ديسك.")
    
    if st.session_state.portfolio_ram:
        for ticker, entry_price in list(st.session_state.portfolio_ram.items()):
            try:
                current_price = float(yf.Ticker(ticker).history(period="1d")['Close'].iloc[-1])
                profit_loss_pct = ((current_price - entry_price) / entry_price) * 100
                
                c1, c2, c3 = st.columns(3)
                c1.text(f"السهم: {ticker}")
                c2.text(f"شراء: {entry_price}$ | حالي: {current_price:.2f}$")
                
                if profit_loss_pct >= 0:
                    c3.success(f"الربح: +{profit_loss_pct:.2f}% 🟢 (وضع آمن)")
                else:
                    c3.error(f"الخسارة: {profit_loss_pct:.2f}% 🔴 (راقب وقف الخسارة)")
            except Exception as ex:
                st.warning(f"تعذر تحديث سهم {ticker}: {ex}")
                
        if st.button("🗑️ تصفية العداد (إفراغ الـ RAM)"):
            st.session_state.portfolio_ram.clear()
            st.rerun()
    else:
        st.info("الـ RAM فارغة. قم بفحص سهم وتسجيله لتبدأ المراقبة الحية.")

with tab3:
    st.subheader("💼 نموذج العمل وشراكة الأرباح")
    st.markdown("""
    * **الفترة التجريبية:** اشتراك رمزي بسيط لكسر حاجز الخوف وتجربة دقة المستشار.
    * **مرحلة الشراكة الحقيقية:** المنصة لا تأخذ شيئاً إن خسرت الصفقة؛ نحن **شركاؤك في النجاح** (نسبة بسيطة من صافي الربح المحقق فقط عند بيع الصفقة بربح).
    """)
